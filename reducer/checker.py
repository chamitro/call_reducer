from abc import ABC, abstractmethod
import subprocess
import re


class PropertyChecker(ABC):

    def __init__(self, file_path: str, patterns: str):
        self.file_path = file_path
        self.patterns = patterns

    @abstractmethod
    def run_test_script(self, file_path: str):
        pass

    @abstractmethod
    def parse_output(self, output: str):
        pass

    @abstractmethod
    def compare_property(self, old_output: str, new_output: str) -> bool:
        pass


class SolidityPropertyChecker(PropertyChecker):
    def __init__(self, file_path: str, patterns: dict, external_cmd: str, script_path: str):
        super().__init__(file_path, patterns)
        self.external_cmd = external_cmd
        self.script_path = script_path

    def run_test_script(self, file_path: str):
        if self.external_cmd == "slither":
            return self.run_slither_analysis(file_path)
        else:
            raise NotImplementedError(
                f"Test script invocation is not supported for {self.external_cmd}")

    def parse_output(self, output: str):
        if self.external_cmd == "slither":
            return self.parse_slither_output(output)
        else:
            raise NotImplementedError(
                f"Parsing output of {self.external_cmd} is not supported"
            )

    def compare_property(self, old_output: str, new_output: str) -> bool:
        if self.external_cmd == "slither":
            return self.compare_slither_outputs(old_output, new_output)
        else:
            raise NotImplementedError(
                f"Comparison of outputs for {self.external_cmd} is not supported"
            )

    def compare_slither_outputs(self, old_output: str,
                                new_output: str) -> bool:
        """Compares Slither findings, considering specified findings."""
        for finding, threshold in self.patterns.items():
            original_count = old_output.get(finding, 0)
            modified_count = new_output.get(finding, 0)
            if (original_count != modified_count or
                    original_count > threshold or modified_count > threshold):
                return False
        return True

    def parse_slither_output(self, slither_output: str):
        """
        Parses the Slither output to only count occurrences of specified
        patterns.
        """
        findings = {}
        for key in self.patterns.keys():
            pattern = re.compile(re.escape(key))
            findings_count = sum(1 for _ in pattern.findall(slither_output))
            if findings_count > 0:
                findings[key] = findings_count
        return findings

    def run_slither_analysis(self, file_path: str):
        """Runs the solidity2.sh script and captures the output."""
        command = [self.script_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            # Capture both stdout and stderr
            print(f"result is:", result.returncode)
#            output = result.stdout + result.stderr
            if result.returncode != 0:
                print("Script execution failed.")
                print(f"Command: {' '.join(command)}")
                print(f"Return Code: {result.returncode}")
                print(f"Error Output: {result.stderr}")
            return result.returncode
        except subprocess.CalledProcessError as e:
            print("Script execution failed.")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Return Code: {e.returncode}")
            print(f"Error Output: {e.stderr}")
            return None


PROPERTY_CHECKERS = {
    "solidity": SolidityPropertyChecker,
}
