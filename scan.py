import yara
import sys

YARA_RULES_PATH = "yara_rules/malware.yar"

def load_yara_rules():
    return yara.compile(filepath=YARA_RULES_PATH)

def scan_file(file_path):
    rules = load_yara_rules()
    matches = rules.match(file_path)
    if matches:
        print(f"Malicious: {matches}")
    else:
        print("Clean")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scan.py <file_path>")
        sys.exit(1)
    
    scan_file(sys.argv[1])

