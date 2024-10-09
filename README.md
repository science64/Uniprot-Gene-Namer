# Uniprot Gene Namer

Uniprot Gene Namer is a Python application that automates the process of converting UniProt accession numbers to gene symbols for both human and mouse proteins. It provides a user-friendly graphical interface for easy interaction.

## Features

- Convert UniProt accession numbers to gene symbols
- Support for both human and mouse proteins
- User-friendly GUI built with tkinter
- Reads and writes Excel files
- Utilizes local databases and the UniProt API for gene symbol lookups

## Requirements

- Python 3.9+
- pandas
- requests
- tkinter (usually comes with Python)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/science64/Uniprot-Gene-Namer.git
   cd Uniprot-Gene-Namer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have the necessary database files in the `files` folder:
   - `Uniprot_database_2021.xlsx`
   - `Mus musculus Gene Symbol Database Uniprot Verified.xlsx`

## Usage

1. Run the main script:
   ```
   python main.py
   ```

2. Use the GUI to:
   - Select your input Excel file containing UniProt accession numbers
   - Choose between human or mouse proteins
   - Run the conversion process
   - Save the output with added gene symbols with same name of your excel file

**Important:** Ensure your input Excel file has either an 'Accession' or 'Master Protein Accessions' column containing the UniProt IDs. The application will look for these column names to process the data.

## How it works

1. The application reads the input Excel file containing UniProt accession numbers.
2. It first attempts to match the accession numbers with a local database.
3. If a match is not found locally, it queries the UniProt API to fetch the gene symbol.
4. The results are compiled and saved to a new Excel file, preserving the original data and adding a new column for gene symbols.

## Contributing

Contributions to improve Uniprot Gene Namer are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Süleyman Bozkurt
- Email: sbozkurt.mbg@gmail.com

## Version History

- v3.1 (Last updated: 09.10.2024)

## Acknowledgments

- UniProt for providing the API and database
- The pandas and requests libraries for making data manipulation and API requests straightforward