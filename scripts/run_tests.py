import subprocess
import shared
import project.graph_test as my_tests


def main():
    shared.configure_python_path()
    subprocess.check_call(["python", "-m", "pytest", "-vv", "-s", shared.TESTS])
    my_tests.test_info()
    my_tests.test_load()
    my_tests.test_build_two_cycles()


if __name__ == "__main__":
    main()
