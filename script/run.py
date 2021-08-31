import os
import re
import subprocess
import shared


def main():
    shared.configure_python_path()

    print("Discover test directory: ")
    for test in os.listdir(shared.TEST):
        if re.match("test_\\w+.py", test):
            test_path = str(shared.TEST / test)
            print(" Exec unit test: ", test_path)
            subprocess.check_call([
                "python",
                "-m",
                "py.test",
                "-v",
                "--cache-clear",
                "--capture=no",
                test_path
            ])


if __name__ == "__main__":
    main()
