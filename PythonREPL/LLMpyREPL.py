#Python REPL to execute code. taken and modified from NuminaMath Solution
#NuminaMath solution can be found here : https://www.kaggle.com/code/lewtun/numina-1st-place-solution
import os
import subprocess
import tempfile

class PythonREPL:
    def __init__(self, timeout=8):
        self.timeout = timeout

    def __call__(self, query):
        #The Sandbox (tempfile): When you call the class, it creates a temporary "bubble" (directory) on your computer. It saves the AI's code into a file named tmp.py inside this bubble.
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "tmp.py")
            with open(temp_file_path, "w", encoding="utf-8") as f:
                f.write(query)
            
            try:
                #Execution (subprocess): It starts a separate, independent Python process to run that file
                result = subprocess.run(
                    ["python3", temp_file_path],
                    capture_output=True,
                    check=False,
                    text=True,
                    timeout=self.timeout,
                )
            except subprocess.TimeoutExpired:
                return False, f"Execution timed out after {self.timeout} seconds."
            #Capturing Output: It "listens" to the execution.

            # Stdout: Anything the code print()s.

            # Stderr: Any error messages if the code fails.
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            #leaning Errors: If the code crashes, the REPL removes the messy file paths from the error message (e.g., /tmp/user/123/tmp.py) and replaces them with <temporary_file>. This makes the error easier for an AI to read and fix.
            if result.returncode == 0:
                return True, stdout
            else:
                # Process the error message to remove the temporary file path
                # This makes the error message cleaner and more user-friendly
                error_lines = stderr.split("\n")
                cleaned_errors = []
                for line in error_lines:
                    if temp_file_path in line:
                        # Remove the path from the error line
                        line = line.replace(temp_file_path, "<temporary_file>")
                    cleaned_errors.append(line)
                cleaned_error_msg = "\n".join(cleaned_errors)
                # Include stdout in the error case
                combined_output = f"{stdout}\n{cleaned_error_msg}" if stdout else cleaned_error_msg
                return False, combined_output
            


# 1. Initialize the REPL
repl = PythonREPL(timeout=5)

# 2. Example: Successful Math Calculation
code_success = """
def solve_math():
    x = 512 * 2
    print(x)

solve_math()
"""

success, result = repl(code_success)
print(f"Success: {success}") # Output: True
print(f"Result: {result}")   # Output: 1024

print("-" * 20)

# 3. Example: Handling a Crash (Error)
code_error = """
# This will cause a ZeroDivisionError
print(10 / 0)
"""

success, result = repl(code_error)
print(f"Success: {success}") # Output: False
print(f"Result:\n{result}")   
# Output: Traceback (most recent call last):
#   File "<temporary_file>", line 3, in <module>
#     print(10 / 0)
# ZeroDivisionError: division by zero