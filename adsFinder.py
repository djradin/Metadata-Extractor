import subprocess,re

def find_ads(path):
    """
    Lists all alternate data stream found on a file (Windows only feature).
    Returns a list of stream names and the size of each stream.
    """
    ads_list = []
    ads_return_list = []
    command = subprocess.run(["cmd", "/c", "dir", "/r", path], capture_output=True, text=True)
    output = command.stdout
    count = 0

    for line in output.splitlines():
        line = line.strip()
        if ":" in line and "$DATA" in line:
            ads_list.append(line)

    if ads_list:
        print("\nAlternate data streams:")
        for ads in ads_list:
            if len(ads_list) > 1:
                print(f"Alternate data stream {ads}")
            count += 1
            parts = re.split(r"[ :]", ads)
            try:
                size = int(parts[0])
                name = parts[2]
            except (IndexError, ValueError):
                continue

            print(f"ADS {count}: {name} ({size} bytes")

            ads_return_list.append({
                "ads_number": count,
                "name": name,
                "size": size})
            print(f"Ads size: {ads[0]} bytes")
            print(f"Ads name: {ads[2]}")
    else:
        print("No alternate data streams found.")

    return ads_return_list