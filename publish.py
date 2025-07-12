import subprocess
import argparse
import os
import shutil

def run_command(command, cwd=None):
    """Runs a shell command and returns its output."""
    print(f"Executing: {' '.join(command)}")
    process = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    if process.returncode != 0:
        print(f"Error: {process.stderr}")
        raise RuntimeError(f"Command failed: {' '.join(command)}")
    print(process.stdout)
    return process.stdout

def clean_build_artifacts():
    """Removes existing build and dist directories."""
    print("Cleaning build artifacts...")
    for directory in ["build", "dist", "symb.egg-info"]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"Removed {directory}/")

def build_package():
    """Builds the sdist and wheel distributions using uv."""
    print("Building package...")
    run_command(["uv", "build"])

def publish_package(repository_url, username, password):
    """Publishes the package to the specified repository."""
    print(f"Publishing package to {repository_url}...")
    # uv currently does not have a direct 'publish' command like twine.
    # We will use twine for publishing, assuming it's installed.
    # If not, the user will need to install it: pip install twine
    dist_files = [f for f in os.listdir("dist") if f.endswith((".tar.gz", ".whl"))]
    if not dist_files:
        raise FileNotFoundError("No distribution files found in 'dist/' directory.")

    command = [
        "twine", "upload",
        "--repository-url", repository_url,
        "-u", username,
        "-p", password
    ] + [os.path.join("dist", f) for f in dist_files]

    run_command(command)

def main():
    parser = argparse.ArgumentParser(description="Build and publish the symb package.")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Publish to TestPyPI instead of PyPI."
    )
    parser.add_argument(
        "--username",
        default="__token__",
        help="Username for the PyPI repository (default: __token__)."
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Password or API token for the PyPI repository."
    )

    args = parser.parse_args()

    if args.test:
        repository_url = "https://test.pypi.org/legacy/"
    else:
        repository_url = "https://upload.pypi.org/legacy/"

    try:
        clean_build_artifacts()
        build_package()
        publish_package(repository_url, args.username, args.password)
        print("\nPackage published successfully!")
    except Exception as e:
        print(f"\nFailed to publish package: {repr(e)}")
        exit(1)

if __name__ == "__main__":
    main()
