import csv
from datetime import datetime

#Load Transactions  
def load_transactions(filename='financial_transactions.csv'):
    """Load transactions from a CSV file into a list of dictionaries."""
    transactions = []
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                try:
                    date = datetime.strptime(row[0], '%Y-%m-%d')
                    amount = float(row[1])
                    transaction_type = row[2].lower()
                    transaction = {
                        'date': date,
                        'amount': amount,
                        'type': transaction_type,
                        'description': row[3]
                    }
                    transactions.append(transaction)
                except (ValueError, IndexError):
                    # Silently skip invalid rows
                    continue
        
        # Display loaded transactions
        if transactions:
            print("\nLoaded Transactions:")
            print("-" * 80)
            print(f"{'Date':<12} {'Amount':<10} {'Type':<8} {'Description'}")
            print("-" * 80)
            for t in transactions:
                print(f"{t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<9.2f} {t['type']:<8} {t['description']}")
            print("-" * 80)
            print(f"Total transactions loaded: {len(transactions)}")
        else:
            print("\nNo transactions found in the file.")
            
        return transactions
    except FileNotFoundError:
        print("\nNo transaction file found. Starting with an empty list.")
        return []

#Add Transaction
def add_transaction(transactions, transaction):
    """Add a new transaction to the list."""
    try:
        print(f"\nProcessing transaction in add_transaction: {transaction}")
        print(f"Date type: {type(transaction['date'])}")
        print(f"Date value: {transaction['date']}")
        
        # Convert date string to datetime
        try:
            date = datetime.strptime(transaction['date'], '%Y-%m-%d')
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
        print(f"Total debits: ${sum(t['amount'] for t in transactions if t['type'] == 'debit'):.2f}")
        print(f"Total credits: ${sum(t['amount'] for t in transactions if t['type'] == 'credit'):.2f}")
        print("\nNote: Changes are not saved to file until you choose option 7 (Save Transactions)")
        
        return transactions
    except Exception as e:
        print(f"Unexpected error in add_transaction: {str(e)}")
        print(f"Error type: {type(e)}")
        return transactions

#View transactions
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
    """Analyze finances with detailed breakdowns and percentages."""
    if not transactions:
        print("\nNo transactions to analyze. Please add some transactions first.")
        return transactions

    # Calculate totals
    total_debits = abs(sum(t['amount'] for t in transactions if t['amount'] < 0))
    total_credits = sum(t['amount'] for t in transactions if t['amount'] > 0)

    # Get unique categories from descriptions
    categories = set(t['description'].lower() for t in transactions)

    print("\nFINANCIAL ANALYSIS")
    print("=" * 80)
    
    # Overall Summary
    print("\nOVERALL SUMMARY")
    print("-" * 80)
    print(f"Total Debits:  ${total_debits:.2f}")
    print(f"Total Credits: ${total_credits:.2f}")
    print(f"Net Balance:   ${(total_credits - total_debits):.2f}")
    print(f"Total Transactions: {len(transactions)}")
    
    # Category Breakdown
    print("\nCATEGORY BREAKDOWN")
    print("-" * 80)
    print(f"{'Category':<20} {'Debits':<15} {'% of Debits':<15} {'Credits':<15} {'% of Credits':<15}")
    print("-" * 80)
    
    for category in sorted(categories):
        # Calculate category totals
        category_debits = sum(t['amount'] for t in transactions 
                            if t['amount'] < 0 and t['description'].lower() == category)
        category_credits = sum(t['amount'] for t in transactions 
                             if t['amount'] > 0 and t['description'].lower() == category)
        
        # Calculate percentages
        debit_percentage = (abs(category_debits) / total_debits * 100) if total_debits > 0 else 0
        credit_percentage = (category_credits / total_credits * 100) if total_credits > 0 else 0
        
        # Print category row
        print(f"{category[:20]:<20} ${abs(category_debits):<14.2f} {debit_percentage:<14.1f}% ${category_credits:<14.2f} {credit_percentage:<14.1f}%")
    
    # Monthly Analysis
    print("\nMONTHLY ANALYSIS")
    print("-" * 80)
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    month_debits = abs(sum(t['amount'] for t in transactions 
                          if t['amount'] < 0 and t['date'].month == current_month 
                          and t['date'].year == current_year))
    month_credits = sum(t['amount'] for t in transactions 
                       if t['amount'] > 0 and t['date'].month == current_month 
                       and t['date'].year == current_year)
    
    print(f"Current Month ({current_month}/{current_year}):")
    print(f"Debits:  ${month_debits:.2f}")
    print(f"Credits: ${month_credits:.2f}")
    print(f"Net:     ${(month_credits - month_debits):.2f}")
    
    # Spending Patterns
    print("\nSPENDING PATTERNS")
    print("-" * 80)
    if total_debits > 0:
        print("Top Spending Categories:")
        # Get top 3 spending categories
        spending_categories = [(t['description'].lower(), abs(t['amount'])) 
                             for t in transactions if t['amount'] < 0]
        category_totals = {}
        for category, amount in spending_categories:
            category_totals[category] = category_totals.get(category, 0) + amount
        
        # Sort and display top 3
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        for category, amount in top_categories:
            percentage = (amount / total_debits * 100)
            print(f"{category[:20]:<20} ${amount:<14.2f} {percentage:<14.1f}%")
    
    print("\n" + "=" * 80)
    return transactions

#save transactions
def save_transactions(transactions, filename='financial_transactions.csv'):
    """Save transactions to a CSV file and generate a report."""
    try:
        # Save to CSV
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Amount', 'Type', 'Description'])
            for t in transactions:
                writer.writerow([
                    t['date'].strftime('%Y-%m-%d'),
                    t['amount'],
                    t['type'],
                    t['description']
                ])
        
        # Generate report
        with open('report.txt', 'w') as report:
            # Calculate totals
            total_debits = sum(t['amount'] for t in transactions if t['type'] == 'debit')
            total_credits = sum(t['amount'] for t in transactions if t['type'] == 'credit')
            net_balance = total_credits - total_debits
            total_amount = total_debits + total_credits
            
            # Write header
            report.write("FINANCIAL TRANSACTION REPORT\n")
            report.write("=" * 80 + "\n\n")
            
            # Write summary
            report.write("SUMMARY\n")
            report.write("-" * 80 + "\n")
            report.write(f"Total Transactions: {len(transactions)}\n")
            report.write(f"Total Amount: ${total_amount:.2f}\n\n")
            
            # Write totals with percentages
            report.write("TOTALS AND PERCENTAGES\n")
            report.write("-" * 80 + "\n")
            report.write(f"{'Category':<15} {'Amount':<15} {'Percentage':<15}\n")
            report.write("-" * 80 + "\n")
            report.write(f"{'Debits':<15} ${total_debits:<14.2f} {(total_debits/total_amount*100):<14.1f}%\n")
            report.write(f"{'Credits':<15} ${total_credits:<14.2f} {(total_credits/total_amount*100):<14.1f}%\n")
            report.write(f"{'Net Balance':<15} ${net_balance:<14.2f} {(net_balance/total_amount*100):<14.1f}%\n\n")
            
            # Write transactions by type
            report.write("TRANSACTIONS BY TYPE\n")
            report.write("-" * 80 + "\n")
            
            # Credit transactions
            report.write("\nCREDIT TRANSACTIONS (Money In):\n")
            report.write("-" * 80 + "\n")
            report.write(f"{'Date':<12} {'Amount':<15} {'Description':<40}\n")
            report.write("-" * 80 + "\n")
            credit_transactions = [t for t in transactions if t['type'] == 'credit']
            for t in sorted(credit_transactions, key=lambda x: x['date']):
                report.write(f"{t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<14.2f} {t['description']:<40}\n")
            
            # Debit transactions
            report.write("\nDEBIT TRANSACTIONS (Money Out):\n")
            report.write("-" * 80 + "\n")
            report.write(f"{'Date':<12} {'Amount':<15} {'Description':<40}\n")
            report.write("-" * 80 + "\n")
            debit_transactions = [t for t in transactions if t['type'] == 'debit']
            for t in sorted(debit_transactions, key=lambda x: x['date']):
                report.write(f"{t['date'].strftime('%Y-%m-%d'):<12} ${t['amount']:<14.2f} {t['description']:<40}\n")
            
            # Write monthly summary
            report.write("\nMONTHLY SUMMARY\n")
            report.write("-" * 80 + "\n")
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            month_debits = sum(t['amount'] for t in transactions 
                             if t['type'] == 'debit' and t['date'].month == current_month 
                             and t['date'].year == current_year)
            month_credits = sum(t['amount'] for t in transactions 
                              if t['type'] == 'credit' and t['date'].month == current_month 
                              and t['date'].year == current_year)
            month_total = month_debits + month_credits
            month_net = month_credits - month_debits
            
            report.write(f"Current Month ({current_month}/{current_year}):\n")
            report.write("-" * 80 + "\n")
            report.write(f"{'Category':<15} {'Amount':<15} {'Percentage':<15}\n")
            report.write("-" * 80 + "\n")
            report.write(f"{'Debits':<15} ${month_debits:<14.2f} {(month_debits/month_total*100):<14.1f}%\n")
            report.write(f"{'Credits':<15} ${month_credits:<14.2f} {(month_credits/month_total*100):<14.1f}%\n")
            report.write(f"{'Net':<15} ${month_net:<14.2f} {(month_net/month_total*100):<14.1f}%\n")
            
            # Write footer
            report.write("\n" + "=" * 80 + "\n")
            report.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print("\nTransactions saved successfully!")
        print(f"Total transactions saved: {len(transactions)}")
        print("Report generated in report.txt")
        return True
    except Exception as e:
        print(f"\nError saving transactions: {str(e)}")
        return False


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
    # TODO: Include a list of transactions
    # TODO: Include a list of categories
    # TODO: Include a list of months
    # TODO: Include a list of years
    # TODO: Include a list of days
    # TODO: Include a list of hours
    # TODO: Include a list of minutes
    pass
