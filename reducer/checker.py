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
            while True:
                result = subprocess.run(command, capture_output=True,
                                        text=False)
                # if "exit 1" in result.stdout.decode("utf-8"):
                #     breakpoint()
                if "exit 3" in result.stdout.decode("utf-8"):
                    print("exit 3")
                if "exit 4" in result.stdout.decode("utf-8"):
                    print("exit 4")
                if ("exit 3" not in result.stdout.decode("utf-8") or
                    "exit 4 " not in result.stdout.decode("utf-8")
                ):
                    break
            return result.returncode
        except subprocess.CalledProcessError:
            return None
