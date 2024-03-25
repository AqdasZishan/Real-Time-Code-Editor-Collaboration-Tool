import sys
import subprocess
import os

def extract_class_name(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            # Check for both valid main method signatures
            if 'public static void main(String[] args)' in line or 'public static void main(String args[])' in line:
                # Look for the class declaration line before the main method
                for j in range(i-1, -1, -1): # Reverse search from the current line
                    class_line = lines[j].strip()
                    if class_line.startswith('class '):
                        # Split the line by spaces and take the second element as the class name
                        # This handles cases where the opening brace is on the same line or on a new line
                        class_name = class_line.split()[1]
                        # Check if the class name ends with a brace and remove it if so
                        if class_name.endswith('{'):
                            class_name = class_name[:-1]
                        print(class_name)
                        return class_name
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

    except Exception as e:
        print(f"Error executing code: {e}")
    
    # executes only when the classpath is found
    if(classpath):
        # Remove all .class files in the directory and its subdirectories
        for root, dirs, files in os.walk(classpath):
            for file in files:
                if file.endswith('.class'):
                    os.remove(os.path.join(root, file))

if __name__ == "__main__":
    main()
