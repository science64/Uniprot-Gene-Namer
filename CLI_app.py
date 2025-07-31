import pandas as pd
import requests
import argparse
import os

def GeneNameEngine(Data, database):
    accessionDatabase = list(database['Accession'])
    geneNameDatabase = list(database['Gene Symbol'])

    try:
        accession = list(Data['Master Protein Accessions'])
    except:
        accession = list(Data['Accession'])
    j = 0

    for i in accession:
        if ';' in i:
            final = i.split(';')[0]
        elif ' ' in i:
            final = i.split(' ')[0]
        else:
            final = i

        if final in accessionDatabase:
            index = accessionDatabase.index(final)
            geneSymbol = geneNameDatabase[index]

        else:
            try:
                url = f'https://www.ebi.ac.uk/proteins/api/proteins/{final}'
                req = requests.get(url)
                result = req.json()
                geneSymbol = result['gene'][0]['name']['value']
            except:
                geneSymbol = ''

        print(f'{i} : {geneSymbol}')
        Data.loc[j, 'Gene Symbol'] = geneSymbol
        j += 1

    return Data

def main():
    parser = argparse.ArgumentParser(
        description="""
        Uniprot Gene Namer CLI

        This script converts UniProt accession numbers to gene symbols for human or mouse proteins.
        It reads an Excel file containing UniProt accession numbers, looks them up in a local database,
        and if not found, queries the UniProt API to retrieve the corresponding gene symbol.
        The output is saved to a new Excel file with an added 'Gene Symbol' column.

        **Note:** This script requires the 'pandas' and 'requests' libraries.
        You can install them using pip:
        ```bash
        pip install pandas requests
        ```

        **Database Files:**
        This script requires database files to function correctly. Please make sure you have the following files in the 'files' folder:
            - `Uniprot_database_human_2025.xlsx` (for human proteins)
            - `Uniprot_database_mouse_2025.xlsx` (for mouse proteins)
        
        You can generate these databases using the fasta_parser.py script from UniProt FASTA files.

        **Example Usage:**
            - To process an Excel file named 'data.xlsx' for human proteins:
            ```bash
            python CLI_app.py --input data.xlsx
            ```
            - To process an Excel file named 'mouse_data.xlsx' for mouse proteins:
            ```bash
            python CLI_app.py --input mouse_data.xlsx --organism mouse
            ```
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter  # Preserve line breaks in the description
    )

    parser.add_argument("--input", required=True, help="Path to the input Excel file containing UniProt accession numbers. The file should have either an 'Accession' or 'Master Protein Accessions' column.")
    parser.add_argument("--organism", choices=['human', 'mouse'], default='human', help="The organism for which to perform the conversion (human or mouse). Defaults to 'human'.")
    args = parser.parse_args()
    input_file = args.input
    organism = args.organism

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    try:
        input_data = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Load the appropriate database based on the selected organism
    try:
        if organism == 'human':
            database = pd.read_excel('./files/Uniprot_database_human_2025.xlsx')
        else:  # organism == 'mouse'
            database = pd.read_excel('./files/Uniprot_database_mouse_2025.xlsx')
    except Exception as e:
        print(f"Error loading database: {e}")
        print(f"Please ensure that the database file is present in the 'files' folder and that you have selected the correct organism.")
        return

    output_data = GeneNameEngine(input_data, database)

    output_file = input_file.replace(".xlsx", "_output.xlsx")
    try:
        output_data.to_excel(output_file, index=False)
        print(f"Output saved to {output_file}")
    except Exception as e:
        print(f"Error saving output file: {e}")

if __name__ == "__main__":
    main()