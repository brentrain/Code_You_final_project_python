## Main Menu ##
if __name__ == "__main__":
    transactions = []
    while True:
        print("\nSmart Personal Finance Analyzer")
        print("1. Load Transactions")
        print("2. Add Transaction")
        print("3. View Transactions")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Analyze Finances")
        print("7. Save Transactions")
        print("8. Generate Report")
        print("9. Exit")
        choice = input("Select an option: ")
        # Call functions based on choice
        if choice==1:
            load_transactions(transactions)
        elif choice==2:
            add_transaction(transactions)
        elif choice==3:
            view_transaction(transactions)
        elif choice==4:
            update_transaction(transactions)
        elif choice==5:
            delete_transaction(transactions)
        elif choice==6:
            analyze_finances(transactions)
        elif choice==7:
            save_transactions(transactions)
        elif choice==8:
            generate_report(transactions)
        else:
            if choice == '9':
                break


## 1. Loading Transactions from a .CSV file

import csv
from datetime import datetime

def load_transactions(finacial_transactions):
    """Load transactions from a CSV file."""
    transactions = []
    with open(finacial_transactions, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            transaction = {
                'transaction_id': int(row['transaction_id']),
                'customer_id': int(row['customer_id']),
                'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                'amount': float(row['amount']),
                'type': row['type'],
                'description': row['description']
            }
            transactions.append(transaction)
    return transactions
with open('financial_transactions.csv','r') as file:
    csv.reader = csv.DictReader(file)
    header = next(csv.reader)
    print("header:", header)
    for row in csv.reader:
        print("row:", row)
    
 ## 2. Adding and viewing the transactions
def add_transaction(transactions, date, amount, description):
    """Add a new transaction from user input."""
    # Prompt for date, customer_id, amount, type, description
    transaction_date = input("Enter transaction date (YYYY-MM-DD): ")
    transaction_amount = float(input("Enter transaction amount: "))
    transaction_type = input("Enter transaction type (credit/debit): ")
    transaction_description = input("Enter transaction description: ")
    # Validate date, amount, type
    if not transaction_date or not transaction_amount or not transaction_type:
        print("Invalid input. Please try again.")
        return
    # Generate new transaction_id
    transaction_id = len(transactions) + 1
    # Create dictionary and append  
    pass   

## viewing the transactions

def view_transactions(transactions):
    """Display transactions in a table."""
    # Print header
    # Loop through transactions
    # Format each row
    pass