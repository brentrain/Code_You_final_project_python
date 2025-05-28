import csv
from datetime import datetime
from logger_config import logger

# Global counter for transaction IDs
transaction_counter = 0

def get_next_transaction_id():
    """Get the next available transaction ID."""
    global transaction_counter
    transaction_counter += 1
    return transaction_counter

#Load Transactions  
def load_transactions(filename='financial_transactions.csv'):
    """Load transactions from a CSV file into a list of dictionaries."""
    transactions = []
    global transaction_counter
    try:
        logger.info(f"Attempting to load transactions from {filename}")
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                try:
                    date = datetime.strptime(row[0], '%Y-%m-%d')
                    amount = float(row[1])
                    transaction_type = row[2].lower()
                    if transaction_type == 'debit':
                        amount = -amount
                    transaction = {
                        'id': get_next_transaction_id(),
                        'date': date,
                        'amount': amount,
                        'type': transaction_type,
                        'description': row[3]
                    }
                    transactions.append(transaction)
                except (ValueError, IndexError) as e:
                    logger.warning(f"Error parsing row: {row}, Error: {str(e)}")
                    continue
        
        # Display loaded transactions
        if transactions:
            logger.info(f"Successfully loaded {len(transactions)} transactions")
            print("\nLoaded Transactions:")
            print("-" * 100)
            print(f"{'ID':<6} {'Date':<12} {'Amount':<10} {'Type':<8} {'Description'}")
            print("-" * 100)
            for t in transactions:
                print(f"{t['id']:<6} {t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<9.2f} {t['type']:<8} {t['description']}")
            print("-" * 100)
            print(f"Total transactions loaded: {len(transactions)}")
        else:
            logger.info("No transactions found in the file")
            print("\nNo transactions found in the file.")
            
        return transactions
    except FileNotFoundError:
        logger.warning(f"Transaction file not found: {filename}")
        print("\nNo transaction file found. Starting with an empty list.")
        return []
    except Exception as e:
        logger.error(f"Unexpected error loading transactions: {str(e)}", exc_info=True)
        print(f"\nError loading transactions: {str(e)}")
        return []

#Add Transaction
"""
    Adds a new transaction to the list of transactions.

    Parameters:
    transactions (list): The current list of transactions.
    new_transaction (dict): The transaction to be added.

    Returns:
    list: Updated list of transactions.
    """
def add_transaction(transactions, transaction):
    try:
        logger.debug(f"Processing transaction: {transaction}")
        
        # Convert date string to datetime
        try:
            date = datetime.strptime(transaction['date'], '%Y-%m-%d')
            logger.debug(f"Date parsed successfully: {date}")
        except ValueError as e:
            logger.error(f"Date parsing error: {str(e)}")
            print(f"Date parsing error: {str(e)}")
            print(f"Attempted to parse: {transaction['date']}")
            print(f"Expected format: 2024-03-20")
            return transactions
        
        # Add ID to transaction
        transaction['id'] = get_next_transaction_id()
        transaction['date'] = date
        logger.debug(f"Transaction after date conversion: {transaction}")
        
        # Add transaction to list
        transactions.append(transaction)
        logger.info(f"Transaction added successfully. New total: {len(transactions)}")
        
        # Print summary
        print(f"\nTransaction added: ID {transaction['id']} - {date.strftime('%Y-%m-%d')} - ${transaction['amount']:.2f} - {transaction['description']}")
        print(f"Total transactions: {len(transactions)}")
        print(f"Total spent: ${sum(t['amount'] for t in transactions if t['amount'] < 0):.2f}")
        print(f"Total earned: ${sum(t['amount'] for t in transactions if t['amount'] > 0):.2f}")
        print("\nNote: Changes are not saved to file until you choose option 7 (Save Transactions)")
        
        return transactions
    except Exception as e:
        logger.error(f"Unexpected error in add_transaction: {str(e)}", exc_info=True)
        print(f"Unexpected error: {str(e)}")
        return transactions

#View transactions
"""
Example:
To view all transactions, call the view_transactions function with a list of transactions:
    transactions = [
        {"date": "2024-03-20", "amount": 100.0, "description": "Groceries"},
        {"date": "2024-03-21", "amount": 50.0, "description": "Gas"}
    ]
    view_transactions(transactions)
"""
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



#update transactions
def update_transaction(transactions):
    """Update an existing transaction in the list."""
    if not transactions:
        print("\nNo transactions to update. Please add some transactions first.")
        return transactions
        
    # Show list with indexes
    print("\nCurrent Transactions:")
    print("-" * 80)
    print(f"{'Index':<8} {'Date':<12} {'Amount':<10} {'Type':<8} {'Description'}")
    print("-" * 80)
    for i, t in enumerate(transactions):
        print(f"{i:<8} {t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<9.2f} {t['type']:<8} {t['description']}")
    print("-" * 80)
    
    # Get and validate index
    try:
        index = int(input("\nEnter the index of the transaction to update: "))
        if index < 0 or index >= len(transactions):
            print("Invalid index. Please try again.")
            return transactions
    except ValueError:
        print("Please enter a valid number.")
        return transactions
    
    # Get new transaction details
    try:
        date_str = input("Enter new date (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        amount = float(input("Enter new amount: "))
        transaction_type = input("Enter transaction type (credit/debit): ").lower()
        if transaction_type == 'debit':
            amount = -amount
            
        description = input("Enter new description: ")
        
        # Update the transaction
        transactions[index] = {
            'date': date,
            'amount': amount,
            'type': transaction_type,
            'description': description
        }
        
        print("\nTransaction updated successfully!")
        print("Note: Changes are not saved to file until you choose option 7 (Save Transactions)")
        return transactions
        
    except ValueError as e:
        print(f"Error updating transaction: {str(e)}")
        return transactions

#delete transactions
def delete_transaction(transactions, transaction_id):
    """
    Delete a transaction from the list of transactions.

    Parameters:
    transactions (list): A list of transaction dictionaries.
    transaction_id (int): The unique identifier of the transaction to be deleted.

    Returns:
    list: The updated list of transactions after the specified transaction is removed.

    Example:
    transactions = [
        {"id": 1, "date": "2024-03-20", "amount": 100.0, "description": "Groceries"},
        {"id": 2, "date": "2024-03-21", "amount": -50.0, "description": "Gas"}
    ]
    updated_transactions = delete_transaction(transactions, 2)
    """
    # Function implementation...
def delete_transaction(transactions):
    """Delete a transaction from the list."""
    if not transactions:
        print("\nNo transactions to delete. Please add some transactions first.")
        return transactions
        
    # Show list with indexes
    print("\nCurrent Transactions:")
    print("-" * 80)
    print(f"{'Index':<8} {'Date':<12} {'Amount':<10} {'Type':<8} {'Description'}")
    print("-" * 80)
    
    for i, t in enumerate(transactions):
        try:
            # Get transaction type, defaulting to 'unknown' if not present
            transaction_type = t.get('type', 'unknown')
            print(f"{i:<8} {t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<9.2f} {transaction_type:<8} {t['description']}")
        except KeyError as e:
            print(f"Error displaying transaction {i}: Missing field {e}")
            continue
    
    print("-" * 80)
    
    # Get and validate index
    try:
        index = int(input("\nEnter the index of the transaction to delete: "))
        if index < 0 or index >= len(transactions):
            print("Invalid index. Please try again.")
            return transactions
            
        # Delete the transaction
        deleted_transaction = transactions.pop(index)
        print(f"\nTransaction deleted successfully!")
        print("Note: Changes are not saved to file until you choose option 7 (Save Transactions)")
        return transactions
        
    except ValueError:
        print("Please enter a valid number.")
        return transactions

#analyze finances
def analyze_finances(transactions):
    """
    Analyze financial transactions with detailed breakdowns and percentages.

    Parameters:
    transactions (list): A list of transaction dictionaries, where each dictionary contains:
        - 'id' (int): Unique identifier for the transaction.
        - 'date' (str): Date of the transaction in YYYY-MM-DD format.
        - 'amount' (float): Transaction amount (positive for credits, negative for debits).
        - 'description' (str): Description of the transaction.

    Returns:
    None: This function outputs the financial analysis directly to the console, including:
        - Total debits and credits
        - Percentage breakdown of each transaction relative to the total amount
    """
    # Function implementation...
def analyze_finances(transactions):
    """Analyze finances with detailed breakdowns and percentages."""
    if not transactions:
        print("\nNo transactions to analyze. Please add some transactions first.")
        return transactions

    # Calculate totals
    total_debits = abs(sum(t['amount'] for t in transactions if t['amount'] < 0))
    total_credits = sum(t['amount'] for t in transactions if t['amount'] > 0)
    total_amount = total_debits + total_credits

    print("\nFINANCIAL ANALYSIS")
    print("=" * 100)
    
    # Transaction List with Percentages
    print("\nTRANSACTION LIST WITH PERCENTAGES")
    print("-" * 100)
    print(f"{'ID':<6} {'Date':<12} {'Amount':<10} {'Type':<8} {'Description':<30} {'% of Total':<10}")
    print("-" * 100)
    
    # Sort transactions by ID
    sorted_transactions = sorted(transactions, key=lambda x: x['id'])
    
    for t in sorted_transactions:
        percentage = (abs(t['amount']) / total_amount * 100) if total_amount > 0 else 0
        print(f"{t['id']:<6} {t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<9.2f} {t['type']:<8} {t['description'][:30]:<30} {percentage:<9.1f}%")
    
    print("-" * 100)
    
    # Category Analysis
    print("\nCATEGORY ANALYSIS")
    print("-" * 100)
    print(f"{'Category':<30} {'Amount':<12} {'Type':<8} {'% of Total':<10}")
    print("-" * 100)
    
    # Get unique categories
    categories = set(t['description'].lower() for t in transactions)
    
    for category in sorted(categories):
        category_transactions = [t for t in transactions if t['description'].lower() == category]
        category_amount = sum(t['amount'] for t in category_transactions)
        category_percentage = (abs(category_amount) / total_amount * 100) if total_amount > 0 else 0
        transaction_type = 'debit' if category_amount < 0 else 'credit'
        
        print(f"{category[:30]:<30} ${abs(category_amount):<11.2f} {transaction_type:<8} {category_percentage:<9.1f}%")
    
    print("-" * 100)
    
    # Summary Statistics
    print("\nSUMMARY STATISTICS")
    print("-" * 100)
    print(f"Total Transactions: {len(transactions)}")
    print(f"Total Debits:  ${total_debits:.2f} ({(total_debits/total_amount*100):.1f}% of total)")
    print(f"Total Credits: ${total_credits:.2f} ({(total_credits/total_amount*100):.1f}% of total)")
    print(f"Net Balance:   ${(total_credits - total_debits):.2f}")
    
    print("\n" + "=" * 100)
    return transactions

#save transactions
def save_transactions(transactions, filename='financial_transactions.csv'):
    """Save transactions to a CSV file."""
    try:
        logger.info(f"Attempting to save {len(transactions)} transactions to {filename}")
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Amount', 'Type', 'Description'])
            for t in transactions:
                amount = abs(t['amount'])
                trans_type = 'debit' if t['amount'] < 0 else 'credit'
                writer.writerow([
                    t['date'].strftime('%Y-%m-%d'),
                    amount,
                    trans_type,
                    t['description']
                ])
        logger.info("Transactions saved successfully")
        print("\nTransactions saved successfully!")
    except Exception as e:
        logger.error(f"Error saving transactions: {str(e)}", exc_info=True)
        print(f"\nError saving transactions: {str(e)}")

#generate report
def generate_report(transactions):
    # TODO: Create a .txt or .csv report with summaries
    for t in transactions:
        print(f"{t['date'].strftime('%Y-%m-%d')} - ${t['amount']:<9.2f} {t['type']:<8} {t['description']}")
    # TODO: Include total spent, earned, by category/month
    print(f"Total spent: ${sum(t['amount'] for t in transactions if t['amount'] < 0):.2f}")
    print(f"Total earned: ${sum(t['amount'] for t in transactions if t['amount'] > 0):.2f}")
    print(f"Total transactions: {len(transactions)}")
    print(f"Total spent by category: {sum(t['amount'] for t in transactions if t['amount'] < 0 and t['type'] == 'debit'):.2f}")
    print(f"Total earned by category: {sum(t['amount'] for t in transactions if t['amount'] > 0 and t['type'] == 'credit'):.2f}")
    print(f"Total spent by month: {sum(t['amount'] for t in transactions if t['amount'] < 0 and t['date'].month == datetime.now().month):.2f}")
    pass
