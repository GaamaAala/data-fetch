import requests
import csv
import os
from datetime import datetime

# API details
URL = "https://imgametransit.com/api/webapi/GetNoaverageEmerdList"
HEADERS = {
    "Content-Type": "application/json"
}

# CSV file setup
CSV_FILE = "data.csv"
CSV_HEADERS = ["Period", "Number", "Premium"]

# Function to fetch data (all rows)
def fetch_data():
    payload = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 1,
        "language": 0,
        "random": "4f7eb2c47c0641c2be6b62053f2f3f53",  # May need dynamic generation
        "signature": "E3D7840D7D96C459DD2074174CD5A9A5",  # May need dynamic generation
        "timestamp": int(datetime.now().timestamp())  # Dynamic timestamp
    }

    response = requests.post(URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "list" in data["data"]:
            return data["data"]["list"]  # Return all rows in the "list" field
    
    return None

# Function to check if period already exists in CSV
def is_new_period(period):
    if not os.path.exists(CSV_FILE):
        return True  # If file doesn't exist, consider all periods new

    with open(CSV_FILE, "r") as file:
        existing_periods = {line.split(",")[0] for line in file.readlines()[1:]}  # Read existing periods
    return period not in existing_periods

# Function to write data to CSV
def write_to_csv(items):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if os.stat(CSV_FILE).st_size == 0:
            writer.writerow(CSV_HEADERS)  # Write headers if file is empty
        
        for item in items:
            period = item["issueNumber"]
            number = item["number"]
            premium = item["premium"]
            
            if is_new_period(period):  # Only write if it's a new period
                writer.writerow([period, number, premium])
                print(f"✅ New period added: {period}")
            else:
                print(f"⚠️ Duplicate period skipped: {period}")

# Main function to fetch data
def main():
    print("Fetching data...")
    data = fetch_data()
    if data:
        write_to_csv(data)
    else:
        print("No new data found.")

if __name__ == "__main__":
    main()
