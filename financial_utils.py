import csv
from datetime import datetime

def load_transactions(filename='financial_transactions.csv'):
    """Load transactions from a CSV file into a list of dictionaries."""
    transactions = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            try:
                date = datetime.strptime(row[0], '%Y-%m-%d')  # Using correct format string
                amount = float(row[1])
                if row[2].lower() == 'debit':
                    amount = -amount
                transaction = {
                    'date': date,
                    'amount': amount,
                    'description': row[3]
                }
                transactions.append(transaction)
            except ValueError as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {e}")
                continue
        return transactions

def add_transaction(transactions, transaction):
    """Add a new transaction to the list."""
    try:
        print(f"\nProcessing transaction in add_transaction: {transaction}")
        print(f"Date type: {type(transaction['date'])}")
        print(f"Date value: {transaction['date']}")
        
        # Convert date string to datetime
        try:
            date = datetime.strptime(transaction['date'], '%Y-%m-%d')  # Using correct format string
            print(f"Date parsed successfully: {date}")
        except ValueError as e:
            print(f"Date parsing error: {str(e)}")
            print(f"Attempted to parse: {transaction['date']}")
            print(f"Expected format: 2024-03-20")
            return transactions
        
        transaction['date'] = date
        print(f"Transaction after date conversion: {transaction}")
        
        # Add transaction to list
        transactions.append(transaction)
        print(f"Transaction added to list. Total transactions: {len(transactions)}")
        
        # Print summary
        print(f"\nTransaction added: {date.strftime('%Y-%m-%d')} - ${transaction['amount']:.2f} - {transaction['description']}")
        print(f"Total transactions: {len(transactions)}")
        print(f"Total spent: ${sum(t['amount'] for t in transactions if t['amount'] < 0):.2f}")
        print(f"Total earned: ${sum(t['amount'] for t in transactions if t['amount'] > 0):.2f}")
        
        return transactions
    except Exception as e:
        print(f"Unexpected error in add_transaction: {str(e)}")
        print(f"Error type: {type(e)}")
        return transactions

def view_transactions(transactions):
    """Display transactions in a table."""
    if not transactions:
        print("\nNo transactions loaded. Please select option 1 to load transactions first.")
        return transactions
        
    print("\nTransaction List:")
    print("-" * 80)
    print(f"{'Date':<12} {'Amount':<10} {'Type':<8} {'Description'}")
    print("-" * 80)
    
    for t in transactions:
        print(f"{t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<9.2f} {t['type']:<8} {t['description']}")
    
    print("-" * 80)
    return transactions

def update_transaction(transactions):
    # TODO: Show list with indexes and ask user which one to update
    
    return transactions

def delete_transaction(transactions):
    # TODO: Show list with indexes and ask user which one to delete
    return transactions

def analyze_finances(transactions):
    # TODO: Calculate total spent, earned, by category/month
    pass

def save_transactions(transactions, filename='financial_transactions.csv'):
    # TODO: Write all current transactions to file (overwrite)
    pass

def generate_report(transactions):
    # TODO: Create a .txt or .csv report with summaries
    pass
