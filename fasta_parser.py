#!/usr/bin/env python3
"""
FASTA Parser for UniProt Gene Namer

This script parses UniProt FASTA files and extracts Accession and Gene Symbol information
to create a CSV database file that can be used with the main Gene Namer application.

Author: Süleyman Bozkurt
Email: sbozkurt.mbg@gmail.com
Version: 1.0
Date: July 31, 2025
"""

import re
import csv
import pandas as pd
import argparse
import os
from datetime import datetime

def parse_fasta_file(fasta_file_path, output_csv_path, output_excel_path=None):
    """
    Parse UniProt FASTA file and extract accession numbers and gene symbols
    
    Args:
        fasta_file_path (str): Path to the input FASTA file
        output_csv_path (str): Path for the output CSV file
        output_excel_path (str): Optional path for Excel output file
    
    Returns:
        tuple: (total_entries, entries_with_genes, entries_without_genes)
    """
    
    accession_gene_pairs = []
    
    try:
        with open(fasta_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Process only header lines (starting with >)
                if line.startswith('>'):
                    # Extract accession number (between first | and second |) for both sp| and tr| entries
                    accession_match = re.search(r'>(?:sp|tr)\|([^|]+)\|', line)
                    
                    # Extract gene symbol (after GN=)
                    gene_symbol_match = re.search(r'GN=([^\s]+)', line)
                    
                    if accession_match:
                        accession = accession_match.group(1)
                        gene_symbol = gene_symbol_match.group(1) if gene_symbol_match else "N/A"
                        
                        accession_gene_pairs.append([accession, gene_symbol])
    
    except FileNotFoundError:
        print(f"Error: Could not find the file {fasta_file_path}")
        return None, None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None, None
    
    # Create DataFrame for easier manipulation
    df = pd.DataFrame(accession_gene_pairs, columns=['Accession', 'Gene Symbol'])
    
    # Write to CSV file
    try:
        df.to_csv(output_csv_path, index=False)
        print(f"Successfully created CSV file: {output_csv_path}")
        
        # Write to Excel file if requested
        if output_excel_path:
            df.to_excel(output_excel_path, index=False)
            print(f"Successfully created Excel file: {output_excel_path}")
        
        # Calculate statistics
        total_entries = len(df)
        entries_with_genes = len(df[df['Gene Symbol'] != 'N/A'])
        entries_without_genes = total_entries - entries_with_genes
        
        print(f"Total entries processed: {total_entries}")
        print(f"Entries with gene symbols: {entries_with_genes}")
        print(f"Entries without gene symbols: {entries_without_genes}")
        
        # Display first few entries as preview
        if not df.empty:
            print("\nFirst 10 entries:")
            print("Accession\tGene Symbol")
            print("-" * 35)
            for _, row in df.head(10).iterrows():
                print(f"{row['Accession']}\t{row['Gene Symbol']}")
        
        return total_entries, entries_with_genes, entries_without_genes
                
    except Exception as e:
        print(f"Error writing output files: {e}")
        return None, None, None

def create_database_from_fasta(fasta_file_path, organism="human", output_dir="./files"):
    """
    Create a database file from FASTA that can be used with the main Gene Namer application
    
    Args:
        fasta_file_path (str): Path to the input FASTA file
        organism (str): Organism type (human/mouse)
        output_dir (str): Directory to save the database files
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output file names with current year
    current_year = datetime.now().year
    base_name = f"Uniprot_database_{organism}_{current_year}"
    csv_output = os.path.join(output_dir, f"{base_name}.csv")
    excel_output = os.path.join(output_dir, f"{base_name}.xlsx")
    
    print(f"UniProt FASTA to Database Converter")
    print("=" * 50)
    print(f"Input file: {fasta_file_path}")
    print(f"Organism: {organism.capitalize()}")
    print(f"Output CSV: {csv_output}")
    print(f"Output Excel: {excel_output}")
    print()
    
    # Check if input file exists
    if not os.path.exists(fasta_file_path):
        print(f"Error: Input file not found: {fasta_file_path}")
        return False
    
    # Parse the FASTA file and create database
    results = parse_fasta_file(fasta_file_path, csv_output, excel_output)
    
    if results[0] is not None:
        print(f"\n✅ Database creation completed successfully!")
        print(f"📊 Database Statistics:")
        print(f"   Total entries: {results[0]:,}")
        print(f"   With gene symbols: {results[1]:,} ({results[1]/results[0]*100:.1f}%)")
        print(f"   Without gene symbols: {results[2]:,} ({results[2]/results[0]*100:.1f}%)")
        return True
    else:
        print("❌ Database creation failed!")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="""
        UniProt FASTA Parser for Gene Namer

        This script parses UniProt FASTA files and extracts accession numbers and gene symbols
        to create database files (CSV and Excel) that can be used with the main Gene Namer application.

        The script reads FASTA format files and extracts:
        - Accession numbers (from >sp|ACCESSION|... format)
        - Gene symbols (from GN=SYMBOL fields)

        **Example Usage:**
            - To create a human protein database from a FASTA file:
            ```bash
            python fasta_parser.py --input UP000005640_9606.fasta --organism human
            ```
            
            - To create a mouse protein database:
            ```bash
            python fasta_parser.py --input mouse_proteome.fasta --organism mouse
            ```
            
            - To specify custom output directory:
            ```bash
            python fasta_parser.py --input proteome.fasta --output-dir ./databases
            ```

        The output files will be saved in the 'files' directory (or specified directory) 
        and can be used with the main CLI_app.py and main.py scripts.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--input", required=True, 
                       help="Path to the input FASTA file")
    parser.add_argument("--organism", choices=['human', 'mouse'], default='human',
                       help="Organism type (human or mouse). Defaults to 'human'")
    parser.add_argument("--output-dir", default="./files",
                       help="Directory to save output files. Defaults to './files'")
    
    args = parser.parse_args()
    
    success = create_database_from_fasta(args.input, args.organism, args.output_dir)
    
    if success:
        print(f"\n🎉 You can now use the generated database files with:")
        print(f"   - CLI_app.py --input your_data.xlsx --organism {args.organism}")
        print(f"   - main.py (GUI version)")
    else:
        print(f"\n💡 Please check the input file path and try again.")
        exit(1)

if __name__ == "__main__":
    main()
