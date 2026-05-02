import subprocess


class SolidityPropertyChecker():

    def __init__(self, file_path: str, test_script: str):
        self.file_path = file_path
        self.test_script = test_script

    def run_test_script(self, file_path: str) -> int:
        print(self.test_script)
        print(file_path)
        command = ["bash", self.test_script, file_path or self.file_path]
        try:
            result = subprocess.run(command, capture_output=True,
                                    text=False)

            return result.returncode
        except subprocess.CalledProcessError:
            return None


class CPropertyChecker():

    def __init__(self, file_path: str, test_script: str):
        self.file_path = file_path
        self.test_script = test_script

    def run_test_script(self, file_path: str) -> int:
        print(self.test_script)
        print(file_path)
        command = ["bash", self.test_script, file_path or self.file_path]
        try:
            while True:
                result = subprocess.run(command, capture_output=True,
                                        text=False)
                if ("exit 3" not in result.stdout.decode("utf-8") or
                    "exit 4 " not in result.stdout.decode("utf-8")
                ):
                    break
            return result.returncode
        except subprocess.CalledProcessError:
            return None


PROPERTY_CHECKERS = {
    "solidity": SolidityPropertyChecker,
    "c": CPropertyChecker
}
