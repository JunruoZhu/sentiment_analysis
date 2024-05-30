# Programming Project (3 CETS): Investigate the Differences in Sentiment of Articles Reporting Cryptocurrencies Before and After Their Collapses

Author: Junruo Zhu (20-728-101)

Supervisor: Dr. Sumit Kumar Ram

Date: May 24th, 2024


## Introduction
Blockchain coins sometimes face collapses, and it is important to detect if financial articles 
reporting a collapsed coin have different sentiments before and after the collapses. 
The results of this project could be used as a reference for investors.

In this project, I investigated three coins' prices and their sentiment values of the articles.
They are UST, LUNC, and FTX. (On around May 13, 2022 TerraUSD (UST) price met a collapse and 
after this collapse, it changed its name to TerraClassicUSD (USTC) which I will refer to as 
UST throughout this document.)

The project will return three plots for each coin, focusing on the 30 days before and after 
the period of maximum price change (price collapse).
1. Price vs. Negative Sentiment
2. Price vs. Positive Sentiment
3. Price vs. Daily Article Number reporting the coin

NOTE: This project uses CPU to compute the sentiment scores of articles. Please note that it will take you a lot of time.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/JunruoZhu/sentiment_analysis.git
    cd sentiment_analysis
    ```
2. Install Poetry (if you haven't already):
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
3. Install the project dependencies [poetry](https://python-poetry.org/docs/#installation):
    ```bash
    poetry install
    ```

## Usage
1. Run the main script to generate the graphs:
    ```bash
    poetry run python ./sentiment_analysis/main.py
    ```

2. The generated graphs will be saved in the `results` folder. The statistical test results
will be shown in the terminal.
    

## Data
The `datasets` directory contains three subdirectories: `ftx`, `lunc`, and `ust` represent 
three coins. Each folder consists of a price file and an article file.
(The price data are from January 1, 2022 to December 31, 2022 on Yahoo Finance and all of 
the text data are  collected from Coindesk.)


## Instructions for Running the Tests
Execute the tests using the following command:
	```bash
    poetry run pytest
    ```

After running the tests, the results will be displayed in the terminal. Review these to ensure 
there are no failures or errors.


## Examples

### Input Data Format
Ensure your data is in the correct format with columns: 
`coin_name_price.txt`: Date, Open, High, Low, Close, Adj Close, Volume
`coin_name_article.txt`: id, URL, Title, Subtitle, Date, Main_Content

### Running the Script
Ensure your data file is in the correct location (e.g., `datasets/coin_name/coin_name_price.txt`).
Ensure in line 20 in the `main.py`, the new coin folder's path is added. 
Run the main script:
	```bash
	poetry run python ./sentiment_analysis/main.py
	```
### Output Data Format
After running the script, the following graphs will be generated and saved in the results 
folder:

`coin_name_price_neg.png`

`coin_name_price_pos.png`

`coin_price_articles.png`

The results of statistical tests will be shown in the terminal.

