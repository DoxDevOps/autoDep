import sys
import csv
from datetime import datetime
import asyncio
import os

def redirect_output_to_file(file_path):
    sys.stdout = open(file_path, 'w')

def restore_output():
    sys.stdout.close()
    sys.stdout = sys.__stdout__


async def insert_data_to_csv(ip_address, facility_name, cluster_id, cluster_name, status):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [current_date, ip_address, facility_name, cluster_id, cluster_name, status]
    updated_rows = []

    # Check if the file exists, create it if it doesn't
    file_path = 'update_status.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "IP Address", "Facility Name", "Cluster ID", "Cluster Name", "Status"])


    # Read existing rows
    with open('update_status.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] != ip_address:
                updated_rows.append(row)

    updated_rows.append(data)

    # Write updated rows
    with open('update_status.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    print("Data inserted successfully.")

def read_csv_contents():
    with open('update_status.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        data = list(reader)  # Read the remaining data rows
    
    # Print the header
    print('\t'.join(header))
    
    # Print the data rows
    for row in data:
        print('\t'.join(row))
