# Changelog

## [4.1.0] - 2025-07-31

### Added
- **Mouse proteome support** - Added complete mouse database generation from UP000000589_10090.fasta
- Enhanced FASTA parser to handle both SwissProt (`sp|`) and TrEMBL (`tr|`) entries
- Automatic database fallback logic in CLI_app.py (prefers 2025 databases, falls back to older versions)
- Comprehensive testing for both human and mouse databases

### Enhanced
- **Improved FASTA parsing** - Now captures both SwissProt and TrEMBL entries for complete coverage
- **Mouse database statistics**: 21,803 entries with 98.6% gene symbol coverage
- **Human database statistics**: 20,663 entries with 98.9% gene symbol coverage  
- Updated CLI_app.py documentation to reflect new database options

### Removed
- **Removed outdated executable** - Deleted "GeneNamer GUI v3.0.exe" (no longer maintained)
- **Removed old database files** - Cleaned up outdated database files:
  - `Uniprot_database_2021.xlsx` (replaced by `Uniprot_database_human_2025.xlsx`)
  - `Mus musculus Gene Symbol Database Uniprot Verified.xlsx` (replaced by `Uniprot_database_mouse_2025.xlsx`)
- **Simplified CLI logic** - Removed fallback database logic since only current databases are maintained

### Database Updates
- Generated fresh mouse proteome database from UniProt (21,803 entries)
- Regenerated human proteome database with improved parser (20,663 entries)
- Both databases now include TrEMBL entries for comprehensive coverage

## [4.0.0] - 2025-07-31

### Added
- **NEW: FASTA Parser (`fasta_parser.py`)** - Complete functionality to create custom databases from UniProt FASTA files
- Support for parsing UniProt FASTA format files to extract accession numbers and gene symbols
- Automatic creation of both CSV and Excel database files for use with existing CLI and GUI tools
- Comprehensive command-line interface for FASTA parsing with organism selection
- Database statistics reporting (entries with/without gene symbols)
- Updated 2025 human proteome database generated from UP000005640_9606.fasta

### Enhanced
- Updated README.md with comprehensive FASTA parser documentation
- Added workflow diagram showing FASTA → Database → Results pipeline
- Enhanced requirements.txt to include openpyxl for Excel support
- Improved documentation with better examples and usage instructions

### Technical Improvements
- Added pandas DataFrame support for better data manipulation
- Enhanced error handling and user feedback
- Progress reporting and preview functionality
- Support for custom output directories
- Year-based database file naming (e.g., Uniprot_database_human_2025.xlsx)

### Database Updates
- Generated fresh human proteome database from UniProt (20,326 entries)
- 99.4% coverage with gene symbols (20,214 entries)
- Compatible with existing CLI_app.py and main.py workflows

## [3.1.0] - 2024-12-19

### Added
- Command-line interface (CLI) functionality
- CLI_app.py for scripting and automation

## [3.0.0] - 2024-10-09

### Added
- Initial release with GUI functionality
- UniProt accession to gene symbol conversion
- Support for human and mouse proteins
- Excel file processing
- UniProt API integration
