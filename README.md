# Network Configuration Extractor

## Overview

This project is a simple Python-based network configuration parser developed for the Dialog Enterprise Network Automation Internship evaluation assignment.

It reads Cisco and Huawei router configuration files, extracts sub-interface details, identifies the router vendor from the configuration content, and exports the extracted information to an Excel file.

## Features

- Reads Cisco and Huawei configuration files from the `configs` directory.
- Automatically identifies the router vendor using configuration keywords.
- Extracts sub-interface names, descriptions, and VRF information.
- Combines the extracted information into a single Excel file.
- Handles empty files, missing configuration directories, and unidentified vendors gracefully.

## Technologies Used

- Python 3
- Regular Expressions (`re`)
- Pandas
- OpenPyXL
- File handling (`pathlib`)

## Project Structure

```text
network-configuration-extractor/
├── configs/
│   ├── router_a.txt
│   └── router_b.txt
├── output/
├── extract_config.py
├── troubleshooting_prompt.txt
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd network-configuration-extractor
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place the router configuration text files inside the `configs` directory.
2. Run the Python script:

```bash
python extract_config.py
```

3. The extracted information will be saved in:

```text
output/extracted_interfaces.xlsx
```

## Output

The Excel file contains the following columns:

- Main Interface
- Description
- VRF
- Vendor

## Assumptions

- The input files contain Cisco or Huawei router configurations.
- Interface configuration sections begin with the `interface` keyword.
- Sub-interfaces are identified by a dot in the interface name.
- Cisco VRFs are identified using `vrf forwarding`.
- Huawei VRFs are identified using `ip binding vpn-instance`.
- Vendor detection is based on configuration content rather than filenames.

## Task 02

A sample prompt for an ISP network troubleshooting AI agent is included in `troubleshooting_prompt.txt`.

The prompt defines the agent's role, technical expertise, troubleshooting methodology, device-specific guidance, safety considerations, and expected response format.