import os
import subprocess
import tempfile
from pathlib import Path


DEFAULT_REMOTE = (
    "https://github.com/"
    "themubasshir/ids2018-validation-safe-ablation.git"
)


def _github_token(secret_name="GITHUB_TOKEN"):
    """
    Obtain GitHub PAT without writing it into repository configuration.
    """

    token = (
        os.environ.get(secret_name)
        or os.environ.get("GH_TOKEN")
    )

    if token:
        return token.strip()

    try:
        from kaggle_secrets import UserSecretsClient

        token = UserSecretsClient().get_secret(
            secret_name
        )

    except Exception as exc:
        raise RuntimeError(
            f"GitHub token unavailable. "
            f"Create Kaggle Secret {secret_name!r}."
        ) from exc

    if not token:
        raise RuntimeError(
            f"Kaggle Secret {secret_name!r} is empty."
        )

    return token.strip()


def _authenticated_git_env(token):
    """
    Temporary GIT_ASKPASS authentication.

    The PAT never enters:
      - command arguments
      - git remote URL
      - git config
      - committed files
    """

    tempdir = tempfile.TemporaryDirectory()

    askpass = Path(tempdir.name) / "git_askpass.py"

    askpass.write_text(
        """#!/usr/bin/env python3
import os
import sys

prompt = sys.argv[1] if len(sys.argv) > 1 else ""

if "Username" in prompt:
    print("x-access-token")
else:
    print(os.environ["STAGE20_GITHUB_PAT"])
""",
        encoding="utf-8",
    )

    askpass.chmod(0o700)

    env = os.environ.copy()

    env["GIT_ASKPASS"] = str(askpass)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["STAGE20_GITHUB_PAT"] = token

    return tempdir, env


def stage20_checkpoint_push(
    repo,
    paths,
    message,
    *,
    branch="main",
    remote_url=DEFAULT_REMOTE,
    secret_name="GITHUB_TOKEN",
):
    """
    Stage specified paths, commit if changed, push using PAT,
    then verify refs/heads/<branch> equals local HEAD.
    """

    repo = Path(repo)

    if not repo.is_dir():
        raise RuntimeError(
            f"Repository missing: {repo}"
        )

    # --------------------------------------------------------------
    # Add only explicitly authorized checkpoint files.
    # --------------------------------------------------------------

    subprocess.run(
        ["git", "add", "--", *[str(p) for p in paths]],
        cwd=repo,
        check=True,
    )

    staged_diff = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo,
    )

    if staged_diff.returncode == 1:

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                message,
            ],
            cwd=repo,
            check=True,
        )

    elif staged_diff.returncode != 0:

        raise RuntimeError(
            "Unable to inspect staged git diff."
        )

    else:

        print(
            "No new staged diff; pushing current HEAD."
        )

    local_head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        text=True,
    ).strip()

    # --------------------------------------------------------------
    # Token-authenticated push.
    # --------------------------------------------------------------

    token = _github_token(secret_name)

    tempdir, auth_env = (
        _authenticated_git_env(token)
    )

    try:

        subprocess.run(
            [
                "git",
                "push",
                remote_url,
                f"HEAD:{branch}",
            ],
            cwd=repo,
            env=auth_env,
            check=True,
        )

        # ----------------------------------------------------------
        # Verify actual remote branch SHA.
        # ----------------------------------------------------------

        result = subprocess.check_output(
            [
                "git",
                "ls-remote",
                remote_url,
                f"refs/heads/{branch}",
            ],
            cwd=repo,
            env=auth_env,
            text=True,
        ).strip()

    finally:

        # Remove token from process environment copy and destroy
        # temporary askpass file.
        auth_env.pop(
            "STAGE20_GITHUB_PAT",
            None,
        )

        tempdir.cleanup()

    if not result:
        raise RuntimeError(
            "Remote branch verification returned no SHA."
        )

    remote_head = result.split()[0]

    if remote_head != local_head:
        raise RuntimeError(
            "REMOTE SHA VERIFICATION FAILED: "
            f"local={local_head} "
            f"remote={remote_head}"
        )

    print()
    print("Git checkpoint pushed and verified.")
    print("  commit:", local_head)
    print("  branch:", branch)
    print("  remote:", remote_url)
    print("  verified:", remote_head == local_head)

    return local_head
