import sys

def redirect_output_to_file(file_path):
    sys.stdout = open(file_path, 'w')

def restore_output():
    sys.stdout.close()
    sys.stdout = sys.__stdout__