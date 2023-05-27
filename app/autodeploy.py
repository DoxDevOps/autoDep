from multiprocessing import Process
import os
import time
from time import sleep
from dotenv import load_dotenv
load_dotenv()
from utils import imp_exp_func
from transpoter import update_host



def filter_sites(sites_list, data):
    site_ids = data[0]['fields']['site']
    filtered_sites = [site for site in sites_list if site['pk'] in site_ids]
    return filtered_sites

def init():
    print("Starting")
    hosts = imp_exp_func.get_data_from_api(os.getenv('IMPORTER_ENDPOINT'))
    cluster_hosts = imp_exp_func.get_data_from_api(os.getenv('CLUSTER_ID'))
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain', 'Authorization': os.getenv('EXPORTER_KEY')}
    sites = filter_sites(hosts, cluster_hosts)
    processes = []

    for site in sites:
        ip_address = site["fields"]["ip_address"]
        user_name = site["fields"]["username"]


        p_process = Process(target=update_host,
                            args=(ip_address, user_name, headers,))
        # start the process
        p_process.start()
        # add the process to the list
        processes.append(p_process)

    # wait for all processes to finish
    for process in processes:
        process.join()

    return True

def call_process():
    start_time = time.time()
    
    init()
    end_time = time.time()
    runtime = end_time - start_time
    print("Runtime:", runtime, "seconds")
    


if __name__ == '__main__':
    start_time = time.time()
    if init():
        end_time = time.time()
        runtime = end_time - start_time
        print("########################################################################################################")
        print("Runtime: ", runtime, " seconds")
        