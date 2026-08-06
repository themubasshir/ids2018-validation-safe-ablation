
from pathlib import Path
from datetime import datetime, timezone
import importlib.util
import json
import math
import os
import sys

import torch
from torch import nn


MODEL_MODULE_PATH = Path(
    os.environ["STAGE15_MODEL_MODULE"]
)

RESULT_PATH = Path(
    os.environ["STAGE15_VERIFICATION_RESULT"]
)

EXPECTED_VERSION_PREFIX = "2.7.1"
EXPECTED_DEVICE_CAPABILITY = (6, 0)
EXPECTED_ARCHITECTURE = "sm_60"


def fail(message):
    raise RuntimeError(message)


print("=" * 100)
print("STAGE 15.2-G — P100 CUDA EXECUTION VERIFICATION")
print("=" * 100)

print("\nImported PyTorch:")
print("  Module:", torch.__file__)
print("  Version:", torch.__version__)
print("  CUDA runtime:", torch.version.cuda)

if not torch.__version__.startswith(
    EXPECTED_VERSION_PREFIX
):
    fail(
        "Unexpected PyTorch version: "
        + torch.__version__
    )

if not torch.cuda.is_available():
    fail(
        "CUDA is not available in the isolated environment."
    )

device = torch.device("cuda:0")

device_name = torch.cuda.get_device_name(0)
device_capability = tuple(
    torch.cuda.get_device_capability(0)
)

compiled_architectures = list(
    torch.cuda.get_arch_list()
)

print("\nCUDA device:")
print("  Name:", device_name)
print("  Capability:", device_capability)
print(
    "  Compiled architectures:",
    compiled_architectures,
)

if device_capability != EXPECTED_DEVICE_CAPABILITY:
    fail(
        "Expected a Tesla P100-class capability of (6, 0), "
        f"found {device_capability}."
    )

if EXPECTED_ARCHITECTURE not in compiled_architectures:
    fail(
        "The isolated PyTorch build does not contain sm_60."
    )


# --------------------------------------------------------
# Basic CUDA kernel execution
# --------------------------------------------------------

torch.manual_seed(42)
torch.cuda.manual_seed_all(42)

a = torch.randn(
    512,
    512,
    device=device,
)

b = torch.randn(
    512,
    512,
    device=device,
)

c = a @ b

torch.cuda.synchronize()

if not torch.isfinite(c).all():
    fail(
        "Basic CUDA matrix multiplication produced "
        "non-finite values."
    )

basic_cuda_result = float(
    c.abs().mean().item()
)

print("\nBasic CUDA kernel:")
print("  Matrix multiplication: PASSED")
print(
    "  Mean absolute result:",
    basic_cuda_result,
)


# --------------------------------------------------------
# Import FT-Transformer module
# --------------------------------------------------------

module_spec = importlib.util.spec_from_file_location(
    "ft_transformer_numeric",
    MODEL_MODULE_PATH,
)

if (
    module_spec is None
    or module_spec.loader is None
):
    fail(
        "Unable to import FT-Transformer module."
    )

model_module = importlib.util.module_from_spec(
    module_spec
)

module_spec.loader.exec_module(
    model_module
)

NumericFTTransformer = (
    model_module.NumericFTTransformer
)


# --------------------------------------------------------
# GPU forward/backward/optimizer test
# --------------------------------------------------------

model = NumericFTTransformer(
    n_features=70,
    d_token=64,
    n_heads=8,
    n_layers=3,
    d_ff=256,
    dropout=0.10,
).to(device)

parameter_count = int(
    sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )
)

x = torch.randn(
    256,
    70,
    device=device,
)

y = torch.cat(
    [
        torch.zeros(
            128,
            device=device,
        ),
        torch.ones(
            128,
            device=device,
        ),
    ]
)

criterion = nn.BCEWithLogitsLoss(
    pos_weight=torch.tensor(
        2.4741381246490737,
        device=device,
    )
)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-3,
    weight_decay=1e-5,
)

torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()

model.train()

optimizer.zero_grad(
    set_to_none=True
)

first_parameter = next(
    model.parameters()
)

parameter_before = (
    first_parameter
    .detach()
    .clone()
)

logits = model(x)

if tuple(logits.shape) != (256,):
    fail(
        "Unexpected FT-Transformer output shape: "
        f"{tuple(logits.shape)}"
    )

if not torch.isfinite(logits).all():
    fail(
        "FT-Transformer generated non-finite logits."
    )

loss = criterion(
    logits,
    y,
)

if not torch.isfinite(loss):
    fail(
        "FT-Transformer loss is non-finite."
    )

loss.backward()

gradient_tensors = [
    parameter.grad
    for parameter in model.parameters()
    if parameter.grad is not None
]

if not gradient_tensors:
    fail(
        "No model gradients were generated."
    )

if not all(
    torch.isfinite(
        gradient
    ).all().item()
    for gradient in gradient_tensors
):
    fail(
        "Non-finite gradients were detected."
    )

gradient_norm_squared = 0.0

for gradient in gradient_tensors:
    gradient_norm_squared += float(
        torch.sum(
            gradient.detach() ** 2
        ).item()
    )

global_gradient_norm = math.sqrt(
    gradient_norm_squared
)

optimizer.step()

parameter_update_maximum = float(
    torch.max(
        torch.abs(
            first_parameter.detach()
            -
            parameter_before
        )
    ).item()
)

torch.cuda.synchronize()

if parameter_update_maximum <= 0:
    fail(
        "Optimizer did not update the model parameters."
    )

peak_gpu_memory_mb = float(
    torch.cuda.max_memory_allocated()
    /
    (1024 ** 2)
)


# --------------------------------------------------------
# Save verification result
# --------------------------------------------------------

result = {
    "stage": "15.2-G",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "python_executable": sys.executable,
    "torch_module_path": torch.__file__,
    "torch_version": torch.__version__,
    "torch_cuda_version": torch.version.cuda,
    "cuda_available": True,
    "device_name": device_name,
    "device_capability": list(
        device_capability
    ),
    "compiled_cuda_architectures": (
        compiled_architectures
    ),
    "required_architecture": (
        EXPECTED_ARCHITECTURE
    ),
    "required_architecture_present": True,
    "basic_cuda_matrix_multiplication": "PASSED",
    "basic_cuda_result_mean_absolute": (
        basic_cuda_result
    ),
    "ft_transformer_parameter_count": (
        parameter_count
    ),
    "ft_transformer_input_shape": list(
        x.shape
    ),
    "ft_transformer_output_shape": list(
        logits.shape
    ),
    "initial_loss": float(
        loss.detach().item()
    ),
    "global_gradient_norm": float(
        global_gradient_norm
    ),
    "parameter_update_maximum": (
        parameter_update_maximum
    ),
    "peak_gpu_memory_mb": (
        peak_gpu_memory_mb
    ),
    "forward_pass": "PASSED",
    "backward_pass": "PASSED",
    "optimizer_step": "PASSED",
    "gpu_training_readiness": "PASSED",
    "holdout_status": "UNTOUCHED",
}

RESULT_PATH.write_text(
    json.dumps(
        result,
        indent=2,
    ),
    encoding="utf-8",
)

print("\nFT-Transformer CUDA smoke test:")
print("  Parameters:", f"{parameter_count:,}")
print("  Input shape:", tuple(x.shape))
print("  Output shape:", tuple(logits.shape))
print("  Loss:", float(loss.detach().item()))
print(
    "  Global gradient norm:",
    global_gradient_norm,
)
print(
    "  Parameter update maximum:",
    parameter_update_maximum,
)
print(
    "  Peak GPU memory:",
    peak_gpu_memory_mb,
    "MB",
)
print("  Forward pass: PASSED")
print("  Backward pass: PASSED")
print("  Optimizer step: PASSED")

print("\nGPU TRAINING READINESS: PASSED")
