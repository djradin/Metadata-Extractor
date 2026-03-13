import os

def create_folder(username):
    output_folder  = f"output/{username}"
    os.makedirs(output_folder, exist_ok = True)
    return output_folder
