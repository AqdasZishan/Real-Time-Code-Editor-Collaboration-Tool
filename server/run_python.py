import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_python.py <filename>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            code = file.read()
            exec(code)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error executing code: {e}")

if __name__ == "__main__":
    main()
