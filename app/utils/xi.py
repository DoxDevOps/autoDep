import os
from dotenv import load_dotenv
load_dotenv()
from utils import imp_exp_func

def get_sites():
    hosts = imp_exp_func.get_data_from_api(os.getenv('IMPORTER_ENDPOINT'))
    return hosts

def get_cluster():
    cluster = imp_exp_func.get_data_from_api(os.getenv('CLUSTER_ID'))
    return cluster