import re

def convert_linux_to_windows_commands(text: str) -> str:
    """
    Convert common Linux shell commands to Windows equivalents in the given text.
    """
    # Replace python3 with python
    text = re.sub(r'python3(\s+-m\s+http\.server)', r'python\1', text)
    text = re.sub(r'python3', 'python', text)
    # Replace bash run.sh with run.bat
    text = re.sub(r'bash\s+run\.sh', 'run.bat', text)
    # Replace .sh scripts with .bat
    text = re.sub(r'(\w+)\.sh', r'\1.bat', text)
    # Remove WSL/Unix-specific instructions
    text = re.sub(r'Use WSL.*?\n', '', text, flags=re.IGNORECASE)
    # Replace Linux path separators with Windows
    text = text.replace('/', '\\')
    return text

# Example usage:
if __name__ == "__main__":
    with open("output.txt", "r", encoding="utf-8") as f:
        content = f.read()
    converted = convert_linux_to_windows_commands(content)
    with open("output_windows.txt", "w", encoding="utf-8") as f:
        f.write(converted)
    print("Conversion complete. See output_windows.txt.")
