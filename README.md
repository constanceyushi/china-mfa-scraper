# China MFA Document Scraper

Automated scraper to collect bilateral policy documents from China's Ministry of Foreign Affairs website, customized for research on "One China Policy" with translation capabilities and analysis tools.

## Features
-  Scrapes documents from all regions and countries
-  Extracts title, year, full text, and document links
-  Identifies mentions of "One China Policy" and "One China Principle"
-  Includes translator script for processing Chinese text
-  Jupyter notebook with detailed data analysis

## Requirements
```bash
pip install selenium pandas jupyter
```
- Chrome browser + ChromeDriver

## Usage

### 1. Scrape Documents
```bash
python scraper.py
```
Outputs: `mfa_YYYY-MM-DD.csv`

### 2. Translate Documents
```bash
python translator.py
```

### 3. Analyze Data
Open `analysis.ipynb` in Jupyter

## Output Format
| Column | Description |
|--------|-------------|
| region | Geographic region |
| country | Country name |
| title | Document title |
| year | Publication year |
| text | Full document text |
| policy | Contains "One China Policy" (Yes/No) |
| principle | Contains "One China Principle" (Yes/No) |
| link | Source URL |

## Notes
- Script takes under 1 hour to complete (estimate based on your experience)
- Some countries may not have document sections
- Respects website structure as of 2025

## License
GPL-3.0 License

## Citation
If you use this data in research, please cite:
```
[Constance Chang]. (2025). China MFA Scraper. 
GitHub: https://github.com/constanceyushi/china-mfa-scraper
```
