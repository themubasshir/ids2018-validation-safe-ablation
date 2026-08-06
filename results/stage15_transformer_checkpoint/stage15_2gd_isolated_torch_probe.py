
from pathlib import Path
import importlib.util
import json
import os
import sys
import traceback


result = {
    "python_executable": sys.executable,
    "python_version": sys.version,
    "python_path_first_entries": sys.path[:8],
    "status": "STARTED",
}


try:
    import torch

    result.update(
        {
            "torch_import": "PASSED",
            "torch_module_path": torch.__file__,
            "torch_version": torch.__version__,
            "torch_cuda_version": torch.version.cuda,
            "cuda_available": bool(
                torch.cuda.is_available()
            ),
            "compiled_architectures": list(
                torch.cuda.get_arch_list()
            ),
        }
    )

    print("Torch import: PASSED")
    print("Torch module:", torch.__file__)
    print("Torch version:", torch.__version__)
    print("Torch CUDA:", torch.version.cuda)
    print(
        "Compiled architectures:",
        torch.cuda.get_arch_list(),
    )
    print(
        "CUDA available:",
        torch.cuda.is_available(),
    )

    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        capability = tuple(
            torch.cuda.get_device_capability(0)
        )

        result[
            "device_name"
        ] = device_name

        result[
            "device_capability"
        ] = list(capability)

        print("Device:", device_name)
        print("Capability:", capability)

        x = torch.tensor(
            [1.0, 2.0, 3.0],
            device="cuda",
        )

        y = x * x + 1.0

        torch.cuda.synchronize()

        result[
            "basic_cuda_tensor_result"
        ] = y.detach().cpu().tolist()

        print(
            "Basic CUDA tensor result:",
            y.detach().cpu().tolist(),
        )

    model_path = Path(
        os.environ["STAGE15_MODEL_MODULE"]
    )

    module_spec = importlib.util.spec_from_file_location(
        "ft_transformer_numeric",
        model_path,
    )

    if (
        module_spec is None
        or module_spec.loader is None
    ):
        raise ImportError(
            "Could not construct model module specification."
        )

    module = importlib.util.module_from_spec(
        module_spec
    )

    module_spec.loader.exec_module(
        module
    )

    result[
        "model_module_import"
    ] = "PASSED"

    print("FT-Transformer module import: PASSED")

    if torch.cuda.is_available():
        model = module.NumericFTTransformer(
            n_features=70,
            d_token=64,
            n_heads=8,
            n_layers=3,
            d_ff=256,
            dropout=0.10,
        ).cuda()

        test_input = torch.randn(
            8,
            70,
            device="cuda",
        )

        output = model(
            test_input
        )

        torch.cuda.synchronize()

        result[
            "model_forward_shape"
        ] = list(output.shape)

        result[
            "model_forward_finite"
        ] = bool(
            torch.isfinite(
                output
            ).all().item()
        )

        print(
            "FT-Transformer GPU output shape:",
            tuple(output.shape),
        )
        print(
            "FT-Transformer GPU output finite:",
            result[
                "model_forward_finite"
            ],
        )

    result["status"] = "PASSED"


except Exception as error:
    result["status"] = "FAILED"
    result["error_type"] = type(error).__name__
    result["error_message"] = str(error)
    result["traceback"] = traceback.format_exc()

    print("\nPROBE FAILURE")
    print("Type:", type(error).__name__)
    print("Message:", str(error))
    print(result["traceback"])


print("\nPROBE_JSON_BEGIN")
print(
    json.dumps(
        result,
        indent=2,
    )
)
print("PROBE_JSON_END")

sys.exit(
    0
    if result["status"] == "PASSED"
    else 1
)
