# LinkedIn Data Extraction and Analysis

## Description

This project automates the collection and analysis of LinkedIn profile data, focusing on alumni of ENSAM Rabat. The extracted information is used to explore professional trajectories, industries, and skills trends among graduates.

## Features

- **Automated Data Scraping**: Collect profile information from LinkedIn using Selenium and BeautifulSoup.
- **Data Structuring**: Organize the collected data into structured formats (CSV/Excel).
- **Exploratory Analysis**: Prepare the data for trend visualization and further analysis.

## Technologies Used

- **Programming Language**: Python
- **Libraries**: 
  - `pandas` for data manipulation.
  - `selenium` and `BeautifulSoup` for web scraping.
  - `numpy` for efficient data processing.
  - `dotenv` for secure environment variable management.
- **Environment**: Jupyter Notebook

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kamaLc73/Data-Mining-Project.git
   cd Data-Mining-Project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure LinkedIn credentials:
   - Create a `.env` file in the root directory with the following:
     ```plaintext
     LINKEDIN_USERNAME="your_email"
     LINKEDIN_PASSWORD="your_password"
     ```

## Usage

### Step 1: Start the LinkedIn Scraper
Run `Main.ipynb` in Jupyter Notebook. It performs the following:
- Logs into LinkedIn using credentials from `.env`.
- Searches profiles using specified queries.
- Extracts and saves profile information to a CSV/Excel file.

### Step 2: Data Processing
- Use the saved data (`profiles_data.csv`) for exploratory data analysis and visualization.
- Extend the scripts to include additional data processing or modeling tasks.

### Example Queries
- **Included Queries**:
  - "Lauréat ENSAM Rabat"
  - "Alumni ENSAM Rabat"
  - "Diplômé ENSAM Rabat"

## Project Status

### Completed:
- Initial data extraction from LinkedIn.
- Basic structure for scraping and data organization.

### Next Steps:
- Perform data cleaning and advanced analysis.
- Visualize career and skill trends.
- Expand the dataset with additional queries.

## Directory Structure

```plaintext
.
├── Main.ipynb               # Main automation script
├── profiles_data.csv        # Collected LinkedIn data
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignored files and directories
```

## Note on Usage

**Important**: Ensure compliance with LinkedIn's Terms of Service when using web scraping methods. This project is intended for educational purposes.
