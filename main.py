#!/usr/bin/env python3
"""Simple student expense tracker. Data is saved in expenses.csv."""
import csv
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "amount", "category", "note"]

def read_expenses():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_expenses(rows):
    with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def add_expense():
    raw_amount = input("Amount (₹): ").strip()
    try:
        amount = float(raw_amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Enter an amount greater than zero.")
        return
    category = input("Category (food/travel/books/etc.): ").strip() or "Other"
    note = input("Note: ").strip()
    rows = read_expenses()
    rows.append({
        "date": date.today().isoformat(),
        "amount": f"{amount:.2f}",
        "category": category,
        "note": note,
    })
    write_expenses(rows)
    print("Expense saved.")

def list_expenses(rows=None):
    rows = read_expenses() if rows is None else rows
    if not rows:
        print("No expenses recorded yet.")
        return
    print(f"\n{'DATE':<12} {'AMOUNT':>10}  {'CATEGORY':<15} NOTE")
    print("-" * 62)
    for row in rows:
        print(f"{row['date']:<12} ₹{float(row['amount']):>9.2f}  {row['category'][:15]:<15} {row['note']}")
    print(f"\nTotal: ₹{sum(float(r['amount']) for r in rows):.2f}")

def category_summary():
    rows = read_expenses()
    if not rows:
        print("No expenses recorded yet.")
        return
    totals = {}
    for row in rows:
        key = row["category"] or "Other"
        totals[key] = totals.get(key, 0) + float(row["amount"])
    print("\nSpending by category")
    for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"  {category}: ₹{amount:.2f}")

def main():
    while True:
        print("\n=== Student Expense Tracker ===")
        print("1. Add expense\n2. View expenses\n3. Category summary\n4. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
