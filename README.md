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

## Tutorial

https://github.com/user-attachments/assets/4fdd9169-ee10-4828-a2c8-70920d1d2ada

## 5. Functions and Analysis

### Expense Pie Chart
<img width="304" alt="Expense Pie Chart" src="https://github.com/user-attachments/assets/909d8651-7750-4a76-802c-ced3586b45f5">

* Purpose: Pie chart helps you to quickly visualise the distribution of your expenses by analysing the proportion size of each category
* Aid in Analysis:
  * Immediate Visual Feedback: The pie chart will allow you to instantly see which categories have larger slices, indicating areas where you've overspent.
  * Focus Areas: Categories with the largest slices can be easily spotted, allowing you to prioritize them for potential cost-cutting.

### Expense Breakdown
<img width="441" alt="Expense Breakdown" src="https://github.com/user-attachments/assets/8e0b03ac-be12-4f95-85e4-cf321b2d5f57">

* Purpose: This provides a detailed breakdown of your spending in each category.
* Aid in Analysis:
  * Detailed Insight: You can see exactly how much you spent in each category.
  * Exclusion of Certain Categories: By excluding Transfers, Investment, and Uncategorized expenses, the focus is kept on essential or expenses which are more controllable.
  
### Goal vs Actual Comparison
<img width="314" alt="Budget Difference" src="https://github.com/user-attachments/assets/fb8f2335-ccf5-450f-b3d3-6cafc103d2f0">

* Purpose: This analysis shows whether you are within or over your budget for different categories.
* Aid in Analysis:
  * Immediate Feedback: It gives you immediate feedback on which categories you're over or under budget.
  * Focus Areas: Highlight categories with significant overspending.

### Top 3 Expenses
<img width="323" alt="Top 3 Expense" src="https://github.com/user-attachments/assets/9ee7ffdb-c276-417e-be5e-93dd1b514e58">

* Purpose: This highlights your top three expenses within specific categories.
* Aid in Analysis:
  * Priority Focus: It identifies the biggest spending items that could be prioritized for cost-cutting.
  * Targeted Action: By knowing exactly where the bulk of your money is going (e.g., GRAB for Transport), you can decide if these are necessary or if adjustments can be made (e.g., using public transport more often).
  * Immediate Impact: Addressing these top expenses can have an immediate and noticeable impact on your overall budget.

 ### Stacked Bar Chart
<img width="596" alt="Stacked bar Chart" src="https://github.com/user-attachments/assets/15c338af-4059-4a5b-897c-217ce88eb7d1">

* Purpose: This visualizes the monthly breakdown of your expenses across various categories.
* Aid in Analysis:
  * Trend Identification: You can easily spot trends in your spending over time. For example, the spike in July might prompt you to investigate why expenses were higher that month.
  * Category Comparison: Different colors represent different categories, making it easy to compare how much you spent on each category month over month.
  * Visual Representation: The visual nature of this chart helps in quickly assessing which categories consistently take up the largest portions of your budget.

## Additional notes
Unfortunately, I have yet find a way to automate the manual entries of categorizing, so I have provided some of the categorisations in the `category.csv` based on my past expenses.

### Example
<img width="1500" alt="Final" src="https://github.com/user-attachments/assets/4f7b2c50-d44f-4877-a305-9548139ad56a">

If MCDONALDS is "Uncategorized" in the `category.csv` as seen here, please add the highlighted keyword "MCDONALD" into `category.csv` so the bot will categorise any reference with the word "MCDONALDS" as category FOOD


*Author: Gong Yuelong*
