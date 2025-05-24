# Smart Personal Finance Analyzer

The **Smart Personal Finance Analyzer** is a command-line Python application that helps users track, manage, and analyze personal financial transactions. It provides simple tools to log expenses and income, generate savings reports, and view spending patterns—all stored in a CSV file.

## Features

- Load transactions from a CSV file
- Add new transactions
- View all recorded transactions
- Update or delete entries
- Analyze spending habits
- Generate basic financial reports
- Error handling and date validation

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/brentrain/Code_You_final_project_python.git
cd Code_You_final_project_python
```

2. **Run the program using Python 3:**

```bash
python main.py
```

No external dependencies required.

## Usage

When the program starts, you’ll see a simple menu:

```
Smart Personal Finance Analyzer
1. Load Transactions
2. Add Transaction
3. View Transactions
4. Update Transaction
5. Delete Transaction
6. Analyze Finances
7. Save Transactions
8. Generate Report
9. Exit
```

Navigate by entering the number of the action you want to perform.

## CSV Format

The app reads from and writes to a file named `financial_transactions.csv` in this format:

| date       | description       | amount | category     |
|------------|-------------------|--------|--------------|
| 2025-05-01 | Grocery Store     | 45.67  | Groceries    |
| 2025-05-02 | Gas Station       | 30.00  | Transportation |

## Technologies Used

- Python 3.x
- Built-in modules: `csv`, `datetime`, `os`

## License

MIT License © 2025 Brent Rainwater
