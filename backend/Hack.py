import yara
import time

def process_file(file_path):
    print(f"Processing file: {file_path}")
    start = time.time()
    def scan_file(rule_file, target_file):
        try:
            # Compile the YARA rule from the specified file
            rules = yara.compile(filepath=rule_file)
            # Scan the target file with the compiled YARA rules
            matches = rules.match(target_file)
            if matches:
                print(f"Matches found in file: {target_file}")
                for match in matches:
                    print(f"Rule: {match.rule}, Tags: {match.tags}, Strings: {match.strings}")
            else:
                pass
        except yara.SyntaxError as e:
            print(f"Syntax error in YARA rule file {rule_file}: {e}")
        except Exception as e:
            print(f"Error scanning file {target_file}: {e}")


    # Open the file in read mode
    with open('file_paths.txt', 'r') as file:
        # Read all lines in the file
        lines = file.readlines()

    # Process each line
    with open('file_paths.txt', 'r') as file:
        rule_files = [line.strip() for line in file if line.strip()]

    # For each rule file, scan the uploaded file (file_path)
    for rule_file in rule_files:
        scan_file(rule_file, file_path)

    #         # Path to the file you want to scan
    # target_file = "/home/mint/Downloads/512f7ddfb27baa17319d733d8e117e2844ae99591deb5068edd5e3062cdc0057.xapk"

    #         # Scan the file
    # scan_file(rule_file, target_file)


    end = time.time()
    print(f"Processing completed in {end - start:.2f} seconds")
    return f"File {file_path} processed successfully!"


