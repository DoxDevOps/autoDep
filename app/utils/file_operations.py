import sys
import csv
from datetime import datetime

def redirect_output_to_file(file_path):
    sys.stdout = open(file_path, 'w')

def restore_output():
    sys.stdout.close()
    sys.stdout = sys.__stdout__


def insert_data_to_csv(ip_address, facility_name, cluster_id, status):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [current_date, ip_address, facility_name, cluster_id, status]
    
    with open('update_status.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    
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
