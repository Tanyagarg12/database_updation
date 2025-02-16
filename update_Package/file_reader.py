import os
import re
import pandas as pd

# Specify directory and filenames
directory_path = r"C:\Users\manoj\Downloads"  # Replace with actual path
csv_file_name = "output.csv"  # Your CSV with extraction rules
output_file_name = "finalOuput.csv"  # Output CSV file

# Step 1: Find the file that starts with 'cd121'
file_name = None
for file in os.listdir(directory_path):
    if file.startswith('cd121'):
        file_name = file
        break

if file_name:
    full_file_path = os.path.join(directory_path, file_name)
    csv_file_path = os.path.join(csv_file_name)
    output_file_path = os.path.join(output_file_name)
    print(f"Found file: {file_name}")

    try:
        # Load CSV file with reading rules
        df = pd.read_csv(csv_file_path)

        # Convert necessary columns to numeric
        df["Page"] = pd.to_numeric(df["Page"], errors="coerce")
        df["Line Number"] = pd.to_numeric(df["Line Number"], errors="coerce")
        df["Stop Column"] = pd.to_numeric(df["Stop Column"], errors="coerce")
        df["Size"] = pd.to_numeric(df["Size"], errors="coerce")

        # Read the text file
        with open(full_file_path, "r") as file:
            lines = file.readlines()

        page_pattern = re.compile(r"PAGE\s+\d+")  # Match "PAGE X"
        san_pattern = re.compile(r"\bSAN\b", re.IGNORECASE)  # Match "SAN"
        minneapolis_pattern = re.compile(r"\bMINNEAPOLIS\b", re.IGNORECASE)  # Match "MINNEAPOLIS"

        current_page = None  
        relative_line = 0  # Reset for each page
        sysid = None  # Store SYSID
        last_sysid = None  # Store last known SYSID
        extracted_data = []  # Store extracted data for CSV
        capture_sysid = False  # Flag to capture SYSID
        sysid_text = []  # Capture SYSID lines until "SAN" or "MINNEAPOLIS"

        for index, line in enumerate(lines):
            match = page_pattern.search(line)

            if match:
                # Print total lines of the previous page before resetting
                if current_page is not None:
                    print(f"Total lines in {current_page}: {relative_line}")

                # Start a new page, reset relative line count
                current_page = int(re.search(r"\d+", match.group()).group())  # Extract page number
                relative_line = 1
                capture_sysid = True  # Enable SYSID capture for next line
                sysid_text = []  # Reset SYSID text capture
                print(f"\n{match.group()} starts at absolute line {index + 1} (Marked as line 1)")

            elif capture_sysid:
                # The first line after "PAGE X" is SYSID
                sysid = line.strip()
                capture_sysid = False
                sysid_text.append(sysid)  # Start capturing SYSID text
                print(f"Captured SYSID: {sysid}")

                # Join SYSID lines into one string
                sysid = " ".join(sysid_text).strip()
                print(f"SYSID before cleaning: {sysid}")  # Debugging

                # Handle SAN or MINNEAPOLIS cases
                if "SAN" in sysid:
                    sysid = re.split(r"\bSAN\b", sysid, maxsplit=1)[0].strip()
                elif "MINNEAPOLIS" in sysid:
                    sysid = re.split(r"\bMINNEAPOLIS\b", sysid, maxsplit=1)[0].strip()

                # Remove trailing "TS"
                sysid = re.sub(r"\bTS\b", "", sysid).strip()

                last_sysid = sysid  # Save for later reference
                sysid_text = []  # Reset SYSID text collection
                print(f"Final SYSID after cleaning: {sysid}") 

            elif sysid and not (san_pattern.search(line) or minneapolis_pattern.search(line)):
                # Capture SYSID-related lines until "SAN" or "MINNEAPOLIS" appears
                sysid_text.append(line.strip())

            # Check if the current relative line is in the CSV rules for this page
            if current_page is not None:
                page_instructions = df[df["Page"] == current_page]
                if relative_line in page_instructions["Line Number"].values:
                    for _, row in page_instructions[page_instructions["Line Number"] == relative_line].iterrows():
                        field_name = row["Field Name"]
                        line_item = row["Line Item"]
                        stop_col = int(row["Stop Column"])
                        size = int(row["Size"])
                        
                        # Extract value from the line using column boundaries
                        extracted_value = line[stop_col - size : stop_col].strip()

                        # **Ensure SYSID is properly assigned and cleaned**
                        clean_sysid = sysid if sysid else last_sysid

                        extracted_data.append([
                            current_page, relative_line, line_item, field_name, clean_sysid, extracted_value
                        ])

            relative_line += 1  # Continue counting lines

        # Convert extracted data to a Pandas DataFrame
        output_df = pd.DataFrame(extracted_data, columns=["Page", "Line Number", "Line Item", "Field Name", "SYSID" ,"Extracted Value"])

        # Save to CSV
        output_df.to_csv(output_file_path, index=False)
        print(f"\nData successfully saved to: {output_file_path}")

    except Exception as e:
        print(f"Error processing the file: {e}")

else:
    print(f"No file starting with 'cd121' found in the directory: {directory_path}")

