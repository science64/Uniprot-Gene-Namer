# Uniprot Gene Namer

Uniprot Gene Namer is a comprehensive Python application suite that automates the process of converting UniProt accession numbers to gene symbols for both human and mouse proteins. It now provides both a command-line interface (CLI) and a user-friendly graphical interface (GUI) for easy interaction, plus a new FASTA parser to create custom databases.

## Features

- Convert UniProt accession numbers to gene symbols
- Support for both human and mouse proteins
- **Command-line interface (CLI) for scripting and automation**
- User-friendly GUI built with tkinter (see original `main.py` for GUI version)
- **NEW: FASTA parser to create custom databases from UniProt FASTA files**
- Reads and writes Excel files and CSV files
- Utilizes local databases and the UniProt API for gene symbol lookups
- Generate up-to-date protein databases from FASTA downloads

## Requirements

- Python 3.9+
- pandas
- requests
- tkinter (usually comes with Python) - _Only required for the GUI version (`main.py`)_

## Installation

1. Clone this repository:
   content_copy
   download
   Use code with caution.
   Markdown

git clone https://github.com/science64/Uniprot-Gene-Namer.git
cd Uniprot-Gene-Namer

2. Install the required packages:
   content_copy
   download
   Use code with caution.

pip install -r requirements.txt

3. Ensure you have the necessary database files in the `files` folder:

- `Uniprot_database_2021.xlsx`
- `Mus musculus Gene Symbol Database Uniprot Verified.xlsx`

## Usage

### FASTA Parser (`fasta_parser.py`) - NEW!

Create custom databases from UniProt FASTA files:

```bash
python fasta_parser.py --input <fasta_file> [--organism human|mouse] [--output-dir ./files]
```

**Arguments:**
- `--input`: (Required) Path to the UniProt FASTA file
- `--organism`: (Optional) Organism type (human or mouse). Defaults to human
- `--output-dir`: (Optional) Directory to save database files. Defaults to ./files

**Examples:**
```bash
# Create human protein database from FASTA
python fasta_parser.py --input UP000005640_9606.fasta --organism human

# Create mouse protein database
python fasta_parser.py --input mouse_proteome.fasta --organism mouse

# Save to custom directory
python fasta_parser.py --input proteome.fasta --output-dir ./custom_databases
```

This will create both CSV and Excel database files that can be used with the CLI and GUI versions.

### CLI Version (`CLI_app.py`)

1. Run the CLI script with the following command:

```bash
python CLI_app.py --input <input_file.xlsx> [--organism human|mouse]

Arguments:
--input: (Required) Path to the input Excel file containing UniProt accession numbers. The file should have either an 'Accession' or 'Master Protein Accessions' column.
--organism: (Optional) The organism for which to perform the conversion. Can be either human or mouse. Defaults to human.

Example:
For human proteins:
python CLI_app.py --input data.xlsx

For mouse proteins:
python CLI_app.py --input data.xlsx --organism mouse

The output will be saved to a new Excel file with the same name as the input file, but with _output appended (e.g., data_output.xlsx).
```

For Help

```
python CLI_app.py -h
```

or

```
python CLI_app.py --help
```

### GUI Version (main.py)

Run the main script:

```
python main.py
```

Use the GUI to:
Select your input Excel file containing UniProt accession numbers
Choose between human or mouse proteins
Run the conversion process
Save the output with added gene symbols with same name of your excel file

#### Important: Ensure your input Excel file (for both CLI and GUI versions) has either an 'Accession' or 'Master Protein Accessions' column containing the UniProt IDs. The application will look for these column names to process the data.

### How it works

#### Gene Symbol Conversion (CLI_app.py & main.py):
1. The application reads the input Excel file containing UniProt accession numbers.
2. It first attempts to match the accession numbers with a local database.
3. If a match is not found locally, it queries the UniProt API to fetch the gene symbol.
4. The results are compiled and saved to a new Excel file, preserving the original data and adding a new column for gene symbols.

#### FASTA Database Creation (fasta_parser.py):
1. Reads UniProt FASTA format files downloaded from UniProt
2. Extracts accession numbers from the header lines (>sp|ACCESSION|...)
3. Extracts gene symbols from the GN= fields in the headers
4. Creates both CSV and Excel database files that can be used by the main application
5. Provides statistics on the number of entries with and without gene symbols

#### Database File Workflow:
```
FASTA File → fasta_parser.py → Database Files → CLI_app.py/main.py → Results
```

## Contributing

Contributions to improve Uniprot Gene Namer are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Süleyman Bozkurt

### Email: sbozkurt.mbg@gmail.com

## Version History

v4.0 (31.07.2025) - Added FASTA parser functionality for creating custom databases
v3.1 (09.10.2024) - Added CLI functionality (19.12.2024)

## Acknowledgments

UniProt for providing the API and database
The pandas and requests libraries for making data manipulation and API requests straightforward
