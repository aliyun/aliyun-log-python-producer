"""Decide whether a CI run needs the wheel build and runtime test matrix."""

import json
import os
from pathlib import Path
import subprocess


def needs_build(paths):
    prefixes = ("src/", "python/", "tests/", "ci/", ".github/workflows/")
    manifests = {"Cargo.toml", "Cargo.lock", "pyproject.toml"}
    return any(path in manifests or path.startswith(prefixes) for path in paths)


def main():
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    if event_name == "pull_request":
        before = event["pull_request"]["base"]["sha"]
    elif event_name == "push":
        before = event.get("before", "")
    else:
        before = ""
    if not before or set(before) == {"0"}:
        build = True
    else:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "-z", before, "HEAD"],
            text=True, capture_output=True,
        )
        # A force-push can leave the previous commit unavailable. Build conservatively.
        build = diff.returncode != 0 or needs_build(diff.stdout.split("\0"))
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write("build={}\n".format(str(build).lower()))


if __name__ == "__main__":
    main()
