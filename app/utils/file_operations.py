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
