import subprocess


class BasicPropertyChecker():

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
            print(result.returncode)
            return result.returncode
        except subprocess.CalledProcessError:
            return None


PROPERTY_CHECKERS = {
    "solidity": BasicPropertyChecker,
    "c": BasicPropertyChecker
}
