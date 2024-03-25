import sys
import subprocess
import os
import re

def extract_class_name(filename):
    with open(filename, 'r') as file:
        fileContent = file.read()
        # Use a regular expression to match the main method signature across multiple lines
        match = re.search(r'public\s+static\s+void\s+main\s*\(\s*String\s*\[\s*\]\s*args\s*\)', fileContent, re.DOTALL) or re.search(r'public\s+static\s+void\s+main\s*\(\s*String\s*args\s*\[\s*\]\s*\)', fileContent, re.DOTALL)
        if match:
            # Find the class name by searching backwards from the match position
            class_name_match = re.search(r'class\s+(\w+)', fileContent[:match.start()], re.DOTALL)
            if class_name_match:
                return class_name_match.group(1)
    return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_java.py <filename>")
        return

    filename = sys.argv[1]
    try:
        # Convert the filename to an absolute path
        absolute_filename = os.path.abspath(filename)
        
        # Compile the Java file
        compile_result = subprocess.run(['javac', absolute_filename], capture_output=True, text=True)
        if compile_result.returncode != 0:
            print(f"Compilation error: {compile_result.stderr}")
            return
        
        # Extract the class name from the Java file
        class_name = extract_class_name(absolute_filename)
        if class_name is None:
            print("Error: Main method not found in the Java file.")
            return
        
        # Set the classpath to the directory containing the compiled .class files
        classpath = os.path.dirname(absolute_filename)
        
        # Run the compiled Java class
        run_result = subprocess.run(['java', '-cp', classpath, class_name], capture_output=True, text=True)
        if run_result.returncode != 0:
            print(f"Runtime error: {run_result.stderr}")
            return
        
        print(run_result.stdout)

        # Remove all .class files in the directory and its subdirectories
        for root, dirs, files in os.walk(classpath):
            for file in files:
                if file.endswith('.class'):
                    os.remove(os.path.join(root, file))

    except Exception as e:
        print(f"Error executing code: {e}")

if __name__ == "__main__":
    main()
