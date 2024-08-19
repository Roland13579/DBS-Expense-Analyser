from typing import Final
import numpy as np
import pandas as pd
import seaborn as sb
import re
from datetime import datetime
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackContext, CallbackQueryHandler , Updater

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

TOKEN:Final = '' #Enter your Telegram Bot Token here
BOT_USERNAME:Final = '@Roland_assist_bot'

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Loading CSV databases

#Load categories CSV into the global variable
categories_df = pd.read_csv(r"-", on_bad_lines='skip')
categories_dict = categories_df.groupby('Category')['Item'].apply(list).to_dict()
#groupby('Category') - to group all rows with the same 'Category'together
#['Item] - After grouping by category, we focus on the item column from the grouped dataframe
#.apply(list) - Convert items in each group into a list, .apply() allows application of function on a csv file
#to_dict() - Converts gruped anf listed data into dictionary
#Eg.
    #Item 1: Food
    #Item 2: Food
    #to
    #'Food': ['Item1', 'Item2']

#Load goals CSV into the global variable
goals_df = pd.read_csv(r"-", on_bad_lines='skip')
goals_dict = goals_df.groupby('Category')['Goal'].apply(list).to_dict()

#Load Bar Chart Data
bar_chart_df = pd.read_csv(r"-", on_bad_lines='skip')
grouped_df = bar_chart_df.groupby(['Month-Year', 'Category'])['Cost'].sum().reset_index()
stacked_bar_dict = grouped_df.pivot(index='Month-Year', columns='Category', values='Cost').fillna(0).to_dict(orient='index')
#Change the csv file with columns "Month-Year" and "Category" and "Cost" to a dictionary within a dictionary 
# Eg. 'Jul-24': {'Food': 200, 'Transport': 150, 'Entertainment': 100}
#pivot() - Reshape data (produce a “pivot” table) based on column values. Uses unique values from specified index / columns to form axes of the resulting DataFrame

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] #List of months

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Commands

#update.message.reply_text
    #update - This is an object that represents incoming message from the telegram API
    #.message - From the 'Update' attribute, .messgae ontain the message data sent by the user
    #reply_text - Used to send a text message in response to the user's message

#/start command
async def start_command(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am Bob, your expense manager. Hope you are having a wonderful day. How may I help you today?")
#/help command
async def help_command(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Instructions to upload bank statement CSV file:\n1. Log in to DBS ibanking\n2.Authenticate login using DBS mobile app\n3. Click on 'My Accounts' tab\n4. Click on 'View Transaction History' tab\n5. Select the account you want to download the CSV for and select the date range\n6. Click 'Go'\n8. Click 'Download' to download the CSV file")

#Error Command
async def error(update : Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Udpdate {update} caused error {context.error}')

#See Budget Goals Command
async def seegoals_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    message_text2='Here are your expense budgets:\n'
    for category, goal in goals_dict.items():
        #Since goal is in a list format, extract element, or else it will print a list and not a number, eg. BILL : $[1000]
        goal_value = goal[0] if isinstance(goal, list) and goal else goal
        message_text2 += f"{category} : ${goal_value}\n"
    message_text2 += f"Your total budget is ${goals_df['Goal'].sum()}"
    await update.message.reply_text(message_text2)

#Edit goals command
CATEGORY, GOAL = range(2) #States of conversaion
#Define conversation handler functions
async def start_editgoals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("No problem! Please enter your new sacins budgets for each of the following categories:")
    context.user_data['categories'] = list(goals_dict.keys()) # Turn the dictionary of categories into a list ['Food', 'Investment', 'Shopping', 'Transport', 'Travel']
    return await ask_goal(update, context)

async def ask_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = context.user_data['categories']
    if not categories: #Check if the list is empty
             await update.message.reply_text("All budgets updated successfully!")
             await seegoals_command(update, context) #Show the updated budgets
             return ConversationHandler.END

    category = categories.pop(0) #Remove and returns first element of the list
    context.user_data['current_category'] = category #Store the current category in the user data 'current_category'
    await update.message.reply_text(f"{category}: ")
    return GOAL

async def save_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    goal = update.message.text
    category = context.user_data['current_category']
    if not re.match(r'^\d+(?:\.\d+)?$', goal): #Check if the goal is a number or a decimal number
        await update.message.reply_text("Please enter a valid number")
        return GOAL
    goal = float(goal)# Cast goal to float
    #Update the CSV file with the updated values
    goals_df.loc[goals_df['Category'] == category, 'Goal'] = goal #.loc accessor used to select columns and rows by label. It selects the rows where the 'Category' column matches category and the 'Goal' columnand assign the goal to the goal column
    goals_df.to_csv(r"-", index=False)
    goals_dict[category] = goal
    if context.user_data['categories']:# Check if there are more categories to process
        return await ask_goal(update, context)
    else:
        await update.message.reply_text("All budgets updated successfully!")
        await seegoals_command(update, context)
        return ConversationHandler.END

#Command to see the stacked bar chart
async def see_stacked_bar_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create and send the stacked bar chart
    bar_chart_path = create_stacked_bar_chart(bar_chart_df)
    await update.message.reply_photo(photo=open(bar_chart_path, 'rb'))

# /cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. Let's restart a new conversation.")
    return ConversationHandler.END
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Functions for responses

#Collection of response replies
def handle_response(text: str) ->str: #Takes in a parameter named 'text' of type string and output a string
    processed: str = text.lower() #Parameter name 'processed' of type string is text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good'
    return 'I am not smart enough to understand what you wrote. Please upload your bank statemenr CSV file for me to help you.'

async def handle_message(update : Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #This will inform us if it is a grp chat or priv chat
    text: str = update.message.text
    print(f'User({update.message.chat.id}) in {message_type}: "{text}"') # Debugging stt
    if message_type == 'group': #Only in group setting
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip #Create new_text of type dtring and replace bot username as empty space
            response: str = handle_response(new_text)
        else:
            return #Bot will not respond unless we are explicitely calling its username
    else:
        response: str = handle_response(text)
    print('Bot: ', response)#Debugging stt
    await update.message.reply_text(response)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Functions to handle document uploads
def classify_transaction(ref1:str) ->str:
    for category, items in categories_dict.items():
        for item in items:
            print(f'Proessiong item of type:{type(item)} with value: {item}')
            if isinstance(item,str):
                try:
                    if item.strip().lower() in ref1.lower():
                        return category
                except:
                    print(f'Error processing item: {item} - {e}')
    return 'Uncategorized'

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stacked_bar_dict
    document = update.message.document
    if document.mime_type == 'text/csv':
        file = await document.get_file()
        file_path = await file.download_to_drive()
        col_names = ["Transaction Date", "Reference", "Debit Amount", "Credit Amount", "Transaction Ref1", "Transaction Ref2", "Transaction Ref3"]
        data = pd.read_csv(file_path, skiprows=6, names=col_names, usecols=[0,1,2,3,4,5,6])

        #Create new column to combine all transaction references
        data['Transaction Ref'] = data['Transaction Ref1'].fillna('') + ' ' + \
                                  data['Transaction Ref2'].fillna('') + ' ' + \
                                  data['Transaction Ref3'].fillna('')
        
        data['Debit Amount'] = pd.to_numeric(data['Debit Amount'], errors='coerce') #Convert Debit Amount to numeric, 'errors=coerce' cprevents error raised when passing a non time value
        #New Column Category
        data['Category'] = data['Transaction Ref'].apply(classify_transaction)

        #For Debugging and Checking
        classified_file_path = 'Classified_Transactions_Reference.csv'
        data.to_csv(classified_file_path, index=False)

        await update.message.reply_document(document=open(classified_file_path, 'rb')) #sends a document as a reply in binary read mode

        #Extract Dates
        data['Transaction Date'] = pd.to_datetime(data['Transaction Date'], errors='coerce') #Extract "Transaction Date" column, ignore errors
        data['Month-Year'] = data['Transaction Date'].dt.strftime('%b-%y') # Converts to MMM-YY format
        month_year_count = data['Month-Year'].value_counts()
        month_with_most_rows = month_year_count.idxmax()# Extract the month from the month-year with the most rows in case 2 consecutive months are mixed inside
        if month_with_most_rows not in stacked_bar_dict: #if month-year does not exist in dictionary, add it
            stacked_bar_dict[month_with_most_rows] = {category: 0 for category in goals_dict.keys()}

        
        #Create a pie chart for the expenses
        category_sums = data.groupby('Category')['Debit Amount'].sum() #Sum the cost of items in each category
        colors = ['#C9190B','#5752D1','#F0AB00','#009596','#F9E0A2','#F0AB00','#C9190B','#F0F0F0']
        #Filter out "Uncategorized" and "Transfers" categories
        filtered_category_sums = category_sums.drop(['Uncategorized', 'Transfer'], errors='ignore')
        plt.figure(figsize=(8, 8))
        filtered_category_sums.plot.pie(autopct='%1.1f%%', startangle=90, title='', ylabel='', colors=colors, fontsize=10)
        plt.title('Expense Pie Chart', fontsize=30, fontweight='bold')  # Remove the title
        plt.tight_layout()  # Adjust the layout to make sure everything fits well
        pie_chart_path = 'pie_chart.png' # Save the pie chart
        plt.savefig(pie_chart_path, bbox_inches='tight')  # Save the figure with tight bounding box
        await update.message.reply_photo(photo=open(pie_chart_path, 'rb'))# Send the pie chart as a photo

        #Send a breakdown of expenses
        message_text ="Here is a breakdown of your expenses:\n\n"
        message_text_x = ""
        total = 0
        for category, amount in category_sums.items():
            # Ensure amount is a scalar
            if isinstance(amount, np.ndarray):
                amount = amount.item()
            #push "Transfer" and "Uncategorized" to the end of the message
            if category == 'Uncategorized' or category == 'Transfer':
                message_text_x += f'- {category}: ${amount:.2f}\n'
            else:
                message_text += f'- {category}: ${amount:.2f}\n'
                total += amount
                #update stacked_bar_dict
                stacked_bar_dict[month_with_most_rows][category] = f'{amount:.2f}'
        message_text += message_text_x
        message_text += f'\nTotal expenses excluding Transfers and uncategorized expenses: ${total:.2f}'
        await update.message.reply_text(message_text)

        message_text1 ="Let's analyse if you are within budget or not!\n\n"
        #Calculate the difference between the goal and the sum of the category
        categories_overspent = [] #List to store categories that are overspent by a large margin, $50 as a threshold
        for category, goal in goals_dict.items():
            #Extract the first element as goal is a list
            goal_value = goal[0] if isinstance(goal, list) and goal else goal
            if category in category_sums:
                difference = goal_value - category_sums[category]
                if isinstance(difference, np.ndarray):  # Ensure difference is a scalar
                    difference = difference.item()
                if difference < -50:
                        categories_overspent.append(category)
                if difference >= 0:
                    message_text1 += f'- {category} : Within budget of ${difference:.2f}\n'
                else:
                    message_text1 +=f'- {category} : Overbudget by ${difference:.2f}\n'
            else:
                message_text1 += f'- {category}: Not found.\n'
        
        #Calculate the total budget deficit or surplus
        if total > goals_df['Goal'].sum():
            message_text1 += f'\nYou are over budget by ${total - goals_df["Goal"].sum():.2f}'
        else:
            message_text1 += f'\nYou are within budget by ${goals_df["Goal"].sum() - total:.2f}'

        if categories_overspent:
            message_text1 += "\n\nPlease focus on mainly cutting down on:\n"
            for category in categories_overspent:
                message_text1 += f'- {category}\n'
        await update.message.reply_text(message_text1)

        #Top 3 expenses apart from Transfer, Uncategorized and Investment categories and items that have "Paynow" in the transaction reference
        data_filtered = data[(data['Category'] != 'Transfer') & (data['Category'] != 'Uncategorized') & (data['Category'] != 'Investment') & (~data['Transaction Ref'].str.contains('Paynow', case=False))] 
        sorted_data = data_filtered.sort_values('Debit Amount', ascending=False) #Sort data in descending order
        top_3_expenses = sorted_data.head(3)
        message_text3 = "Here are your TOP 3 expenses excluding Transfers, Investments and Uncategorized and your Paynow Transactions:\n\n"

        #Access the item keynames of the top 3 expenses to be sent to the user
        for index, row in top_3_expenses.iterrows():
            # Check each item in categories_dict to find a match in 'Transaction Ref'
            for category, items in categories_dict.items():
                for item in items:
                    if isinstance(item, str) and item.strip().lower() in row['Transaction Ref'].lower():
                        message_text3 += f"- {item} ({category}) : ${row['Debit Amount']:.2f}\n"
                        break  # Exit the inner loop once a match is found
        await update.message.reply_text(message_text3)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Give user 2 options, yes or no on telegram
        # Defining and adding buttons 
        yes = InlineKeyboardButton(text="Yes", callback_data="In_First_button") 
        no = InlineKeyboardButton( text="No", callback_data="In_Second_button")

        # Create an inline keyboard markup and add the buttons
        keyboard_inline = InlineKeyboardMarkup([[yes, no]])
        await update.message.reply_text(f"Would you like to save your expenses under the month of {month_with_most_rows}?", reply_markup=keyboard_inline)
    else:
        await update.message.reply_text("Please upload a CSV file")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create Stacked Bar Chart
def create_stacked_bar_chart(stacked_bar_df):
    # Ensure 'Cost' column is numeric
    stacked_bar_df['Cost'] = pd.to_numeric(stacked_bar_df['Cost'], errors='coerce')

    # Convert 'Month-Year' to datetime to ensure proper sorting
    stacked_bar_df['Month-Year'] = pd.to_datetime(stacked_bar_df['Month-Year'], format='%b-%y')

    # Pivot the DataFrame to get 'Month-Year' as the index and 'Category' as columns
    pivot_df = stacked_bar_df.pivot(index='Month-Year', columns='Category', values='Cost').fillna(0)

    # Sort the index to ensure the x-axis is in the correct order
    pivot_df = pivot_df.sort_index()

    #convert the index to a string in the format 'MMM-YY'
    pivot_df.index = pivot_df.index.strftime('%b-%y')

    # Define a color map for categories
    category_colors = {
        'Food': '#1f77b4',  # Blue
        'Transport': '#ff7f0e',  # Orange
        'Shopping': '#d62728',  # Red
        'Travel': '#9467bd',  # Purple
        'Investment': '#8c564b',  # Brown
        'Bills': '#e377c2',  # Pink
        # Add more categories and colors as needed
    }

    # Create a list of colors for the plot
    colors = [category_colors.get(category, '#333333') for category in pivot_df.columns]
    # Plot the DataFrame
    plt.figure(figsize=(12, 8))
    pivot_df.plot(kind='bar', stacked=True, color=colors)
    plt.title('Monthly Expenses Breakdown', fontsize=20, fontweight='bold')
    plt.ylabel('Cost', fontsize=15)
    plt.xlabel('Month-Year', fontsize=15)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the bar chart
    bar_chart_path = 'bar_chart.png'
    plt.savefig(bar_chart_path, bbox_inches='tight')
    plt.close()  # Close the plot to avoid displaying it in non-interactive environments
    return bar_chart_path

# In your handle_callback_query function, call the create_stacked_bar_chart function
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stacked_bar_dict
    query = update.callback_query
    await query.answer()
    if query.data == 'In_First_button':
        # Sort the dictionary by year then month
        sorted_items = sorted(stacked_bar_dict.items(), key=lambda x: datetime.strptime(x[0], '%b-%y'))
        stacked_bar_dict = dict(sorted_items)

        rows = []
        # Rewrite data into the CSV file in the right format where column 1 is "Month-Year" and column 2 is "Category" and column 3 is "Cost" from the dictionary
        for month_year, category_costs in stacked_bar_dict.items():
            for category, cost in category_costs.items():
                rows.append([month_year, category, cost])
        stacked_bar_df = pd.DataFrame(rows, columns=['Month-Year', 'Category', 'Cost'])

        # Save the data into a CSV file
        stacked_bar_df.to_csv(r"-", index=False)
        await query.edit_message_text(text="Data saved successfully!")

        # Create and send the stacked bar chart
        bar_chart_path = create_stacked_bar_chart(stacked_bar_df)
        await query.message.reply_photo(photo=open(bar_chart_path, 'rb'))
    else:
        await query.edit_message_text(text="Data not saved. Hope to hear from you again soon!")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Main Function
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Conversation handler for editing goals
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('edit_goals', start_editgoals)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_goal)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_goal)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('see_goals', seegoals_command))
    app.add_handler(CommandHandler('show_chart', see_stacked_bar_chart))
    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Document (CSV) handler
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3) # App checks the app for new messages every 3 seconds
