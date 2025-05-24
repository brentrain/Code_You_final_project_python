#main.py
import csv
from datetime import datetime

CSV_FILE = 'financial_transactions.csv'

from financial_utils import (
    load_transactions,
    add_transaction,
    view_transactions,
    update_transaction,
    delete_transaction,
    analyze_finances,
    save_transactions,
    generate_report
)

def main():
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

        if choice == '1':
            transactions = load_transactions('financial_transactions.csv')
        elif choice == '2':
            try:
                print("\nAdding new transaction...")
                date_str = input("Enter date (format: 2024-03-20): ")
                # Validate date format
                if not (len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-'):
                    print("Error: Date must be in format YYYY-MM-DD (e.g., 2024-03-20)")
                    print("Make sure to use hyphens (-) between year, month, and day")
                    continue
                print(f"Date entered: {date_str}")
                
                amount = float(input("Enter amount: "))
                print(f"Amount entered: {amount}")
                
                trans_type = input("Enter type (credit/debit): ")
                print(f"Type entered: {trans_type}")
                
                description = input("Enter description: ")
                print(f"Description entered: {description}")
                
                new_transaction = {
                    'date': date_str,
                    'amount': amount,
                    'type': trans_type,
                    'description': description
                }
                print(f"\nTransaction object created: {new_transaction}")
                
                transactions = add_transaction(transactions, new_transaction)
            except ValueError as e:
                print(f"Error in main: {str(e)}")
                print("Please enter date in format: 2024-03-20")
            except Exception as e:
                print(f"Unexpected error in main: {str(e)}")
                print(f"Error type: {type(e)}")
        elif choice == '3':
            view_transactions(transactions)
        elif choice == '4':
            transactions = update_transaction(transactions)
        elif choice == '5':
            transactions = delete_transaction(transactions)
        elif choice == '6':
            analyze_finances(transactions)
        elif choice == '7':
            save_transactions(transactions, 'financial_transactions.csv')
        elif choice == '8':
            generate_report(transactions)
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
