import yara
import time

def scan_file(rule_file, target_file):
    try:
        rules = yara.compile(filepath=rule_file)
        matches = rules.match(target_file)
        matches_data = []
        for match in matches:
            strings = []
            for s in match.strings:
                strings.append({
                    "offset": s[0],
                    "identifier": s[1],
                    "data": str(s[2])
                })
            matches_data.append({
                "rule": match.rule,
                "tags": match.tags,
                "strings": strings
            })
        return matches_data
    except yara.SyntaxError as e:
        return {"error": f"YARA syntax error: {str(e)}"}
    except Exception as e:
        return {"error": f"Scan error: {str(e)}"}

def process_file(file_path):
    results = []
    with open('file_paths.txt', 'r') as file:
        rule_files = [line.strip() for line in file if line.strip()]

    for rule_file in rule_files:
        rule_result = {
            "rule_file": rule_file,
            "matches": scan_file(rule_file, file_path)
        }
        results.append(rule_result)

    return results
