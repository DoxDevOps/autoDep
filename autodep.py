import os
from dotenv import load_dotenv
load_dotenv()
from utils import imp_exp_func

def getSites():
    hosts = imp_exp_func.get_data_from_api(os.getenv('IMPORTER_ENDPOINT'))
    cluster_hosts = imp_exp_func.get_data_from_api(os.getenv('CLUSTER_ID'))
    sites = filter_sites(hosts, cluster_hosts)

def filter_sites(sites_list, data):
    site_ids = data[0]['fields']['site']
    filtered_sites = [site for site in sites_list if site['pk'] in site_ids]
    return filtered_sites


getSites()