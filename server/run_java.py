import sys
import subprocess
import os

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
        
        # Determine the class name, excluding the file path
        class_name = os.path.splitext(os.path.basename(absolute_filename))[0]
        # If the class is part of a package, include the package name in the class name
        if '.' in class_name:
            class_name = class_name.replace('.', '/')
        
        # Compile the Java file
        compile_result = subprocess.run(['javac', absolute_filename], capture_output=True, text=True)
        if compile_result.returncode != 0:
            print(f"Compilation error: {compile_result.stderr}")
            return
        
        # Determine the class name, excluding the file path
        class_name = os.path.splitext(os.path.basename(absolute_filename))[0]
        # If the class is part of a package, include the package name in the class name
        if '.' in class_name:
            class_name = class_name.replace('.', '/')
        
        # Set the classpath to the directory containing the compiled .class files
        classpath = os.path.dirname(absolute_filename)
        
        # Run the compiled Java class
        run_result = subprocess.run(['java', '-cp', classpath, 'Main'], capture_output=True, text=True)
        if run_result.returncode != 0:
            print(f"Runtime error: {run_result.stderr}")
            return
        
        print(run_result.stdout)
    except Exception as e:
        print(f"Error executing code: {e}")

if __name__ == "__main__":
    main()
