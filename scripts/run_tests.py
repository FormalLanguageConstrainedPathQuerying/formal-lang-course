import subprocess
import shared


def main():
    shared.configure_python_path()
    subprocess.check_call(
        [
            "python",
            "-m",
            "pytest",
            "-vv",
            "-s",
            "--cov=project",
            "--no-cov-on-fail",
            "--cov-branch",
            # "--cov-report=html", # Uncomment if you html reports
            "--cov-fail-under=50",
            shared.TESTS,
        ]
    )


if __name__ == "__main__":
    main()
