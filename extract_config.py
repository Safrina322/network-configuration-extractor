
import re
from pathlib import Path

import pandas as pd

# Project directories
BASE_DIR = Path(__file__).parent
CONFIG_DIR = BASE_DIR / "configs"
OUTPUT_DIR = BASE_DIR / "output"

def detect_vendor(config_text):
    """Identify the router vendor using configuration keywords."""

    text = config_text.lower()

    if "ip binding vpn-instance" in text or "sysname huawei" in text:
        return "Huawei"

    if "vrf forwarding" in text or "vrf definition" in text:
        return "Cisco"

    return "Unknown"

def extract_interfaces(config_text, vendor):
    """Extract interface, description and VRF information."""

    records = []

    # Find each interface configuration block
    blocks = re.split(r"(?m)^\s*interface\s+", config_text)

    for block in blocks[1:]:
        lines = block.strip().splitlines()

        if not lines:
            continue

        # The first line contains the interface name
        interface_name = lines[0].strip()

        # Only process sub-interfaces
        if "." not in interface_name:
            continue

        description = ""
        vrf = ""

        # Examine the commands inside this interface
        for line in lines[1:]:
            line = line.strip()

            if line.startswith("description "):
                description = line.replace("description ", "", 1).strip()

            if vendor == "Cisco" and line.startswith("vrf forwarding "):
                vrf = line.replace("vrf forwarding ", "", 1).strip()

            elif vendor == "Huawei" and line.startswith("ip binding vpn-instance "):
                vrf = line.replace("ip binding vpn-instance ", "", 1).strip()

        records.append({
            "Main Interface": interface_name,
            "Description": description,
            "VRF": vrf,
            "Vendor": vendor
        })

    return records

def process_config_file(file_path):
    """Read one configuration file and extract its records."""

    try:
        config_text = file_path.read_text(
            encoding="utf-8",
            errors="replace"
        )
    except OSError as error:
        print(f"Could not read {file_path.name}: {error}")
        return []

    if not config_text.strip():
        print(f"{file_path.name} is empty.")
        return []

    vendor = detect_vendor(config_text)

    if vendor == "Unknown":
        print(f"Could not identify vendor in {file_path.name}.")
        return []

    records = extract_interfaces(config_text, vendor)

    if not records:
        print(f"No sub-interface records found in {file_path.name}.")

    return records

def main():
    all_records = []

    # Read all .txt configuration files from the configs folder
    if not CONFIG_DIR.exists():
        print("The configs folder does not exist.")
        return

    config_files = list(CONFIG_DIR.glob("*.txt"))

    if not config_files:
        print("No configuration files found.")
        return

    for config_file in config_files:
        print(f"Processing {config_file.name}...")

        records = process_config_file(config_file)
        all_records.extend(records)

    if not all_records:
        print("No data was extracted. Excel file was not created.")
        return

    # Create a DataFrame using the required column order
    columns = ["Main Interface", "Description", "VRF", "Vendor"]
    df = pd.DataFrame(all_records, columns=columns)

    # Create the output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save the extracted data into an Excel file
    output_file = OUTPUT_DIR / "extracted_interfaces.xlsx"

    try:
        df.to_excel(output_file, index=False)
        print("\nExtraction completed successfully!")
        print(f"Excel file saved to: {output_file}")
        print(f"Total interfaces extracted: {len(df)}")
    except Exception as error:
        print(f"Could not create Excel file: {error}")

if __name__ == "__main__":
    main()