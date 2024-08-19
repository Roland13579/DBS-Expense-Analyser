<p align="center">
 <h1 align="center">Telegram Bot: DBS Expense Analysis</h1>
</p>

## Introduction
This is a Telegram bot used to analyse DBS transaction history. 

## Get started

### 1. Requirements
Install requiremental package:
* `pip install python-telegram-bot`
* `pip install telegram`
* `pip install numpy`
* `pip install seaborn`
* `pip install matplotlib`

### 2. Get Telegram Bot Token
**Telegram Bot Token:**

* <p>Opening Telegram app &#8594; Access Bot Father &#8594; Create new bot &#8594; Get Bot Token.</p>
* Paste your Bot Token into `TOKEN:Final = '-'` 
* <p>You can also customize your bot with the command provided by Bot Father.</p>

### 3. Download CSV Files
**Ensure that you have these 3 CSV files downloaded:**
* `category.csv`: user has to manually categorize key words from their Transaction Ref column with the respective category
* `goals.csv` : Contains the monthly goal budget</p>
* `bar_chart_data.csv` : Contains distributions of monthly expenses to be plotted into a stacked bar diagram.

### 4. Update File Paths into the code
**For each of the files, copy the file paths and pase them in their respectives areas in the code**
* Fill in file path for category.csv
  * `categories_df = pd.read_csv(r"-", on_bad_lines='skip')`
* Fill in file path for goals.csv
  * `goals_df = pd.read_csv(r"-", on_bad_lines='skip')`
  * `goals_df.to_csv(r"-", index=False)`
* Fill in file path for bar_chart_data.csv
  * `bar_chart_df = pd.read_csv(r"-", on_bad_lines='skip')`
  * `stacked_bar_df.to_csv(r"-", index=False)`

## Turorial

https://github.com/user-attachments/assets/4fdd9169-ee10-4828-a2c8-70920d1d2ada


*Author: Gong Yuelong*
