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

# Extend the listener to include functionality for removing specific statements
class CollectAssignmentsListener(SolidityListener):
    def __init__(self):
        super().__init__()
        self.removals = []

    def enterStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
        print("STATE VARIABLES")
        print(ctx.getText())
        expr = ctx.expression() if hasattr(ctx, 'expression') else None
        if expr:
            self.removals.append((ctx.start.start, ctx.stop.stop))
            self._replaceWithConstant(ctx, expr)
        elif hasattr(ctx, 'init') and ctx.init():
            expr = ctx.init().expression()
            if expr:
                self.removals.append((ctx.start.start, ctx.stop.stop))
                self._replaceWithConstant(ctx, expr)

    def enterIfStatement(self, ctx: SolidityParser.IfStatementContext):
#        print(ctx.getText())
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterStructDefinition(self, ctx: SolidityParser.StructDefinitionContext):
#        print(ctx.getText())
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterReturnStatement(self, ctx: SolidityParser.ReturnStatementContext):
        print(ctx.getText())
        self.removals.append((ctx.start.start, ctx.stop.stop))
        
    def enterEventDefinition(self, ctx: SolidityParser.EventDefinitionContext):
#        print(ctx.getText())
        self.removals.append((ctx.start.start, ctx.stop.stop))
    
    def enterEnumDefinition(self, ctx: SolidityParser.EnumDefinitionContext):
#        print(ctx.getText())
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterWhileStatement(self, ctx: SolidityParser.WhileStatementContext):
        print(ctx.getText())
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterForStatement(self, ctx: SolidityParser.ForStatementContext):
        self.removals.append((ctx.start.start, ctx.stop.stop))
    
    def enterSimpleStatement(self, ctx: SolidityParser.SimpleStatementContext):
        print(ctx.getText())
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterEmitStatement(self, ctx: SolidityParser.EmitStatementContext):
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterExpressionStatement(self, ctx: SolidityParser.ExpressionStatementContext):
        print("EXPRESSIONS")
        print(ctx.getText())
        expr = ctx.expression()
#        print(expr.getText())
        if expr:
            if 'require' in expr.getText() or 'assert' in expr.getText():
                print("BIKAME SE ERROR HANDLING")
                self.removals.append((ctx.start.start, ctx.stop.stop))
            elif expr.getChildCount() == 3 and expr.getChild(1).getText() in ['=', '+=', '-=']:
                if re.search(r'"([^"]+)"', expr.getChild(2).getText()):
                    self.removals.append((expr.getChild(2).start.start, expr.getChild(2).stop.stop, '""'))
                elif 'true' in expr.getChild(2).getText() or 'false' in expr.getChild(2).getText():
                    self.removals.append((expr.getChild(2).start.start, expr.getChild(2).stop.stop, 'true'))
                else:
                    print("THA ADIKATASTISOUME ME 1")
                    self.removals.append((expr.getChild(2).start.start, expr.getChild(2).stop.stop, '1'))
            elif isinstance(expr, SolidityParser.FunctionCallContext):
                function_name = expr.expression().getText()
                if function_name in ['require', 'assert']:
                    self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterVariableDeclarationStatement(self, ctx: SolidityParser.VariableDeclarationStatementContext):
        print("VARIABLE DECLARATIONS")
        print(ctx.getText())
        expr = ctx.expression() if hasattr(ctx, 'expression') else None
        if expr:
            self.removals.append((ctx.start.start, ctx.stop.stop))
            self._replaceWithConstant(ctx, expr)
        elif hasattr(ctx, 'init') and ctx.init():
            expr = ctx.init().expression()
            if expr:
                self.removals.append((ctx.start.start, ctx.stop.stop))
                self._replaceWithConstant(ctx, expr)

    def _replaceWithConstant(self, ctx, expr):
        type_name = ctx.getText()
        replacement = '1'  # Default replacement for uint and int

        if 'bool' in type_name:
            replacement = 'true'
        elif 'string' in type_name:
            replacement = '""'
        
        if expr and expr.start and expr.stop:
            self.removals.append((expr.start.start, expr.stop.stop, replacement))

def apply_modifications(source_code, modifications, file_path, consider_findings):
    """Applies modifications and validates each using Slither."""
    modified_code = source_code
    original_output = run_slither_analysis(file_path)
    original_findings = parse_slither_findings(original_output, consider_findings)

    for mod in sorted(modifications, key=lambda x: x[0], reverse=True):
        if len(mod) == 2:
            start, stop = mod
            replacement = ''
        elif len(mod) == 3:
            start, stop, replacement = mod

        # Tentatively apply the modification by deleting or replacing
        tentative_code = modified_code[:start] + replacement + modified_code[stop+1:]
        print(tentative_code)
        
        # Write tentative code to a temporary file
        with open(file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(tentative_code)
        
        # Run Slither on the temporary file
        modified_output = run_slither_analysis(file_path)
        modified_findings = parse_slither_findings(modified_output, consider_findings)

        # Check if the modification meets the criteria
        if compare_slither_outputs(original_findings, modified_findings, consider_findings):
            modified_code = tentative_code  # Accept the modification
            original_findings = modified_findings  # Update findings for next comparison
        else:
            print(f"Modification at {start}-{stop} rejected by Slither analysis.")
    
    return modified_code

def main(argv):
    if len(argv) < 2:
        print("Usage: python script.py <path_to_solidity_file> --consider <slither_property>")
        return

    args = parse_arguments()

    file_path = args.file_path
    consider = args.consider

    # Convert the consider argument into a dictionary of findings and thresholds
    consider_findings = {}
    for item in consider.split(','):
        finding, threshold = item.split('=')
        consider_findings[finding.strip()] = int(threshold.strip())

    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()

    lexer = SolidityLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    parser = SolidityParser(stream)
    tree = parser.sourceUnit()

    listener = CollectAssignmentsListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    modified_code = apply_modifications(source_code, listener.removals, file_path, consider_findings)

    # Write the final modified code back to the file
    with open(file_path, 'w', encoding='utf-8') as out_file:
        out_file.write(modified_code)
    print(f"Final code after modifications saved to {file_path}")

if __name__ == "__main__":
    main(sys.argv)

