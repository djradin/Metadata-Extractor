import os
import json
import shutil
from pathlib import Path

def create_folder(username):
    root = Path(__file__).parent
    path = root / "user_data" / "output" / username
    os.makedirs(path, exist_ok = True)
    return path

def delete_folder(username):
    root = Path(__file__).parent
    path = root / "user_data" / "output" / username
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
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
        json_data = json_convert(metadata)
        print(metadata)
        print(json_data)
        json.dump(json_data, f)

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

def save_settings(username, settings):
    root = Path(__file__).parent
    path = root / "user_data" / "settings" / f"{username}.json"
    os.makedirs(path.parent, exist_ok=True)

    with open(path, "w") as f:
        json.dump(settings, f, indent = 4)

def load_settings(username):
    root = Path(__file__).parent
    path = root / "user_data" / "settings" / f"{username}.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def json_convert(data):
    if isinstance(data, dict):
        return {str(k): json_convert(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [json_convert(v) for v in data]
    elif isinstance(data, bytes):
        return data.decode(errors="ignore")
    elif hasattr(data, "numerator") and hasattr(data, "denominator"):
        return float(data)
    else:
        return data