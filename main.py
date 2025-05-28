#main.py
import csv
from datetime import datetime
from logger_config import logger

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
    logger.info("Starting Smart Personal Finance Analyzer")
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
            logger.info("Loading transactions from file")
            transactions = load_transactions('financial_transactions.csv')
        elif choice == '2':
            try:
                logger.info("Starting new transaction entry")
                print("\nAdding new transaction...")
                date_str = input("Enter date (format: 2024-03-20): ")
                # Validate date format
                if not (len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-'):
                    logger.error(f"Invalid date format: {date_str}")
                    print("Error: Date must be in format YYYY-MM-DD (e.g., 2024-03-20)")
                    print("Make sure to use hyphens (-) between year, month, and day")
                    continue
                logger.debug(f"Date entered: {date_str}")
                
                amount = float(input("Enter amount: "))
                logger.debug(f"Amount entered: {amount}")
                
                trans_type = input("Enter type (credit/debit): ")
                logger.debug(f"Type entered: {trans_type}")
                
                description = input("Enter description: ")
                logger.debug(f"Description entered: {description}")
                
                new_transaction = {
                    'date': date_str,
                    'amount': amount,
                    'type': trans_type,
                    'description': description
                }
                logger.debug(f"Transaction object created: {new_transaction}")
                
                transactions = add_transaction(transactions, new_transaction)
            except ValueError as e:
                logger.error(f"Value error in transaction entry: {str(e)}")
                print(f"Error in main: {str(e)}")
                print("Please enter date in format: 2024-03-20")
            except Exception as e:
                logger.error(f"Unexpected error in transaction entry: {str(e)}", exc_info=True)
                print(f"Unexpected error in main: {str(e)}")
                print(f"Error type: {type(e)}")
        elif choice == '3':
            logger.info("Viewing transactions")
            view_transactions(transactions)
        elif choice == '4':
            logger.info("Updating transaction")
            transactions = update_transaction(transactions)
        elif choice == '5':
            logger.info("Deleting transaction")
            transactions = delete_transaction(transactions)
        elif choice == '6':
            logger.info("Analyzing finances")
            analyze_finances(transactions)
        elif choice == '7':
            logger.info("Saving transactions to file")
            save_transactions(transactions, 'financial_transactions.csv')
        elif choice == '8':
            logger.info("Generating report")
            generate_report(transactions)
        elif choice == '9':
            logger.info("Exiting application")
            print("Goodbye!")
            break
        else:
            logger.warning(f"Invalid menu choice: {choice}")
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error in main program: {str(e)}", exc_info=True)
        print("A critical error occurred. Please check the logs for details.")
