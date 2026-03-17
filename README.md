# FactSage Equilib H₂ Output Parser & Table Generator

## Overview

This Python tool processes thermodynamic output from **FactSage (Equilib module)** to extract and organize hydrogen production data across a range of temperatures.

It is designed primarily for studying **serpentinization reactions**, but can be easily adapted for other geochemical or thermodynamic systems.

The script:

* Reads temperature inputs from a text file (`sample.txt`)
* Parses corresponding Equilib output data
* Extracts species quantities (e.g., H₂, serpentine, magnetite, etc.)
* Generates a structured table
* Exports results to **CSV** and **Excel (XLSX)** for easy analysis and visualization

---

## Features

* 🔹 Automated parsing of FactSage Equilib outputs
* 🔹 Batch processing of multiple temperatures
* 🔹 Clean tabular output for quick interpretation
* 🔹 Export formats:

  * `.csv`
  * `.xlsx`
* 🔹 Customizable for different reactions and species
* 🔹 Designed for hydrogen yield analysis in geological systems

---

## Example Output Format

| T (°C) | mol H₂(g) | mol Serpentine | mol Magnetite (Fe₃O₄) | mol Brucite (Mg(OH)₂) | mol Talc | mol SiO₂ | mol H₂O remaining | mol Olivine remaining | H₂ yield (mL/g rock) |
| ------ | --------- | -------------- | --------------------- | --------------------- | -------- | -------- | ----------------- | --------------------- | -------------------- |

---

## Input Requirements

### 1. FactSage (Required)

This tool relies on output generated from **FactSage 8.4 Equilib**.

You must:

* Have FactSage installed on your system
* Run Equilib calculations separately
* Export the results in a consistent text format

> ⚠️ This repository does **not** include FactSage. A valid license is required.

---

### 2. Temperature File

Provide a text file (`sample.txt`) containing temperatures, for example:

```
100
150
200
250
300
```

---

### 3. Equilib Output Files

Ensure your FactSage output files:

* Correspond to the temperatures listed
* Contain species data in a consistent format
* Are accessible to the script

---

## Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

Outputs:

* `output.csv`
* `output.xlsx`

---

## Dependencies

Typical libraries used:

* `pandas`
* `numpy`
* `openpyxl`

(Adjust based on your actual code)

---

## Customization

You can easily adapt this tool to:

* Different thermodynamic reactions
* Alternative mineral systems
* Additional chemical species
* Custom output metrics (e.g., gas yields, ratios)

---

## Contributing

Contributions are welcome!

Ideas for contributions:

* Support for more FactSage output formats
* Direct parsing of raw Equilib files
* Visualization tools (plots of H₂ vs temperature)
* Integration with other geochemical models

---

## Disclaimer

This tool is intended to assist with data processing and does not replace proper thermodynamic modeling. Users are responsible for verifying results from FactSage.

---

## Acknowledgments

* FactSage developers for thermodynamic modeling tools
* Open-source Python ecosystem

---

## License

MIT License (or specify your choice)
