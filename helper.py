# helpers.py

import csv
from datetime import datetime, timedelta

DATE_FILE = "date.txt"
BOUGHT_CSV = "bought.csv"
SELL_CSV = "sell.csv"

def init_date():
    with open(DATE_FILE, "w") as file:
        file.write("20-11-2023")

def read_date():
    with open(DATE_FILE, "r") as file:
        date_str = file.read().strip()
        return datetime.strptime(date_str, "%d-%m-%Y")

def update_date(new_date):
    with open(DATE_FILE, "w") as file:
        file.write(new_date.strftime("%d-%m-%Y"))

def record_purchase(product_name, buy_price, expiration_date):
    current_date = read_date()

    with open(BOUGHT_CSV, mode="a", newline="") as csvfile:
        fieldnames = ["buy_id", "buy_date", "buy_name", "buy_amount", "buy_price", "expire_date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        with open(BOUGHT_CSV, mode="r") as csv_file:
            last_id = sum(1 for _ in csv.reader(csv_file)) + 1

        writer.writerow({
            "buy_id": last_id,
            "buy_date": current_date.strftime("%d.%m.%Y"),
            "buy_name": product_name,
            "buy_amount": 0,  # Initialize with 0, will be updated during sales
            "buy_price": buy_price,
            "expire_date": expiration_date
        })

def record_sale(product_name, sell_price):
    current_date = read_date()
    sell_data = []

    with open(BOUGHT_CSV, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["buy_name"] == product_name and int(row["buy_amount"]) > 0:
                sell_data.append({
                    "sell_id": len(sell_data) + 1,
                    "sell_date": current_date.strftime("%d.%m.%Y"),
                    "buy_name": product_name,
                    "sell_amount": 1,  # Selling 1 unit at a time for simplicity
                    "sell_price": sell_price,
                    "Buy_ID": row["buy_id"]
                })
                # Update the bought amount
                row["buy_amount"] = str(int(row["buy_amount"]) - 1)

    # Update the bought CSV
    with open(BOUGHT_CSV, mode="w", newline="") as csvfile:
        fieldnames = ["buy_id", "buy_date", "buy_name", "buy_amount", "buy_price", "expire_date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row for row in reader)

    # Append the sale data to the sell CSV
    with open(SELL_CSV, mode="a", newline="") as csvfile:
        fieldnames = ["sell_id", "sell_date", "buy_name", "sell_amount", "sell_price", "Buy_ID"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(sell_data)

def generate_inventory_report(date):
    bought_data = []

    with open(BOUGHT_CSV, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bought_data.append({
                "Product Name": row["buy_name"],
                "Count": int(row["buy_amount"]),
                "Buy Price": float(row["buy_price"]),
                "Expiration Date": row["expire_date"]
            })

    return bought_data

def generate_revenue_report(date):
    sell_data = []

    with open(SELL_CSV, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sell_data.append({
                "Product Name": row["buy_name"],
                "Sell Amount": int(row["sell_amount"]),
                "Sell Price": float(row["sell_price"]),
                "Revenue": int(row["sell_amount"]) * float(row["sell_price"])
            })

    return sell_data
