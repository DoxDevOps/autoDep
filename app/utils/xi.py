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

def get_cluster_id():
    data = get_cluster()
    pks = []
    for item in data:
        pk = item.get("pk")
        if pk is not None:
            pks.append(pk)
    return pks

def get_cluster_name():
    data = get_cluster()
    cluster_name = data[0]['fields']['name']
    return cluster_name
