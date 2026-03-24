import os
import json
import shutil
from pathlib import Path

def create_folder(username):
    output_folder  = f"user_data/output/{username}"
    os.makedirs(output_folder, exist_ok = True)
    return output_folder

def delete_folder(username):
    output_folder = Path("user_data/output") / username
    if output_folder.exists() and output_folder.is_dir():
        shutil.rmtree(output_folder)
    return

def save_file(current_user, metadata):
    output_filename = metadata["basic_info"]["File Name"]
    output_folder = create_folder(current_user)
    output_path = f"{output_folder}/{output_filename}.json"
    counter = 1

    while os.path.exists(output_path):
        filename = f"{output_filename} ({counter}).json"
        output_path = os.path.join(output_folder, filename)
        counter += 1


    with open(output_path, "w") as f:
        json.dump(metadata, f)

    print(f"Saved data to: {output_path}")

def list_files(current_user):
    folder = create_folder(current_user)
    return [f for f in os.listdir(folder) if f.endswith(".json")]

def load_file(current_user, filename):
    folder = create_folder(current_user)
    path = os.path.join(folder, filename)

    if not (os.path.exists(path)):
        print("File not found.")
        return None

    with open(path, "r") as f:
        return json.load(f)