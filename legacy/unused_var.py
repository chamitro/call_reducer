import sys
import re
import argparse
import subprocess
from antlr4 import *
from SolidityLexer import SolidityLexer
from SolidityParser import SolidityParser
from SolidityListener import SolidityListener

def parse_arguments():
    parser = argparse.ArgumentParser(description='Modify Solidity files based on Slither analysis.')
    parser.add_argument('file_path', type=str, help='Path to the Solidity file.')
    parser.add_argument('--consider', type=str, help='Slither property to consider in the format "property=threshold".', default="is never used and should be removed=5")
    args = parser.parse_args()
    return args

def run_slither_analysis(file_path):
    """Runs Slither on a given Solidity file and captures the output."""
    command = ["slither", file_path]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stderr  # Assuming the relevant output is in stderr
    except subprocess.CalledProcessError as e:
        print("Slither analysis failed.")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"Error Output: {e.stderr}")
        return None

def parse_slither_findings(slither_output, consider_findings):
    """Parses the Slither output to count occurrences of specified patterns."""
    findings_count = {}
    for property in consider_findings.keys():
        pattern = re.compile(re.escape(property))
        findings_count[property] = sum(1 for _ in pattern.findall(slither_output))
    return findings_count

def compare_slither_outputs(original_findings, modified_findings, consider_findings):
    """Compares Slither findings, considering specified findings."""
    print("COMPARISONS")
    print(f"Original findings: {original_findings}")
    print(f"Modified findings: {modified_findings}")
    for finding, threshold in consider_findings.items():
        original_count = original_findings.get(finding, 0)
        modified_count = modified_findings.get(finding, 0)
        if original_count != modified_count or original_count > threshold or modified_count > threshold:
            print("Findings do not match criteria. Not replacing the original file.")
            return False
    print("Findings match criteria. Replacing the original file.")
    return True

class UnusedVariableListener(SolidityListener):
    def __init__(self):
        self.unused_params = []  # To store potentially unused variables
        self.current_function_params = []

    def enterFunctionDefinition(self, ctx:SolidityParser.FunctionDefinitionContext):
        self.current_function_params = []  # Reset for each new function

    def enterParameterList(self, ctx:SolidityParser.ParameterListContext):
        for param in ctx.parameter():
            type_ = param.typeName().getText()
            print(type_)
            name = param.identifier().getText() if param.identifier() else None
            print(name)
            if name:
                start_index = param.identifier().start.start
                stop_index = param.identifier().stop.stop
                self.current_function_params.append((name, start_index, stop_index))

    def enterReturnParameters(self, ctx:SolidityParser.ReturnParametersContext):
        for param in ctx.parameterList().parameter():
            name = param.identifier().getText() if param.identifier() else None
            if name:
                start_index = param.identifier().start.start
                stop_index = param.identifier().stop.stop
                self.current_function_params.append((name, start_index, stop_index))

    def exitFunctionDefinition(self, ctx:SolidityParser.FunctionDefinitionContext):
        block_text = ctx.block().getText() if ctx.block() else ""
        for name, start_idx, stop_idx in self.current_function_params:
            if name not in block_text:
                self.unused_params.append((name, start_idx, stop_idx))

def apply_modifications(source_code, unused_vars, file_path, consider_findings):
    modified_code = source_code
    original_output = run_slither_analysis(file_path)
    original_findings = parse_slither_findings(original_output, consider_findings)

    for name, start_idx, stop_idx in sorted(unused_vars, key=lambda x: x[1], reverse=True):
        # Attempt to remove the variable
        temporary_code = modified_code[:start_idx] + modified_code[stop_idx+1:]
        with open(file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(temporary_code)

        # Check Slither output to confirm the change is safe
        new_output = run_slither_analysis(file_path)
        new_findings = parse_slither_findings(new_output, consider_findings)

        if compare_slither_outputs(original_findings, new_findings, consider_findings):
            modified_code = temporary_code  # Accept the modification
            original_findings = new_findings  # Update the original findings for next comparison
        else:
            print(f"Modification for variable '{name}' rejected by Slither analysis.")

    return modified_code

def main():
    args = parse_arguments()

    file_path = args.file_path
    consider = args.consider

    # Convert the consider argument into a dictionary of findings and thresholds
    consider_findings = {}
    for item in consider.split(','):
        finding, threshold = item.split('=')
        consider_findings[finding.strip()] = int(threshold.strip())

    with open(file_path, 'r') as file:
        source_code = file.read()

    lexer = SolidityLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    parser = SolidityParser(stream)
    tree = parser.sourceUnit()

    listener = UnusedVariableListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    modified_code = apply_modifications(source_code, listener.unused_params, file_path, consider_findings)

    # Write the finally accepted modifications back to the file
    with open(file_path, 'w', encoding='utf-8') as out_file:
        out_file.write(modified_code)

    print(f"Modifications applied and verified with Slither. Updated file saved to {file_path}")

if __name__ == "__main__":
    main()

