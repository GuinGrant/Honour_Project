import re

def extract_alert_with_unique_sid(input_file, output_file):
    # Clear the output file at the beginning of the run
    with open(output_file, "w", encoding="utf-8") as out:
        pass  # Clears file

    # Pattern to capture from "alert"/"Alert" onward, with -> and ()
    pattern = r'(?i)(alert\b.*?->.*?\(.*?\))'

    # Keep track of used SIDs
    used_sids = set()

    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            match = re.search(pattern, line)
            if match:
                alert_part = match.group(1).strip()

                # Normalize alert
                alert_part = re.sub(r'(?i)^alert', 'alert', alert_part)

                # Extract SID
                sid_match = re.search(r'sid\s*:\s*(\d+)', alert_part)
                if sid_match:
                    original_sid = int(sid_match.group(1))
                    new_sid = original_sid

                    # Increment SID if already used
                    while new_sid in used_sids:
                        new_sid += 1

                    # Replace old SID with new one
                    alert_part = re.sub(r'sid\s*:\s*\d+', f'sid:{new_sid}', alert_part)
                    used_sids.add(new_sid)
                else:
                    # No SID? Add one starting from 1000000+
                    new_sid = 1000000
                    while new_sid in used_sids:
                        new_sid += 1
                    alert_part = alert_part.rstrip(')') + f'; sid:{new_sid};)'
                    used_sids.add(new_sid)

                # Write to output
                with open(output_file, "a", encoding="utf-8") as outfile:
                    outfile.write(alert_part + '\n')

# Example usage
extract_alert_with_unique_sid("conversation_log_final.txt", "filtered_alerts.txt")
