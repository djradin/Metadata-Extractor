#Making this sucked so bad ngl

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import reverse_geocode


def get_exif_data(path):
    exif_file = Image.open(path)
    exif_data = exif_file.getexif()
    gps_data = exif_data.get_ifd(0x8825)

    if exif_data:
        print("\nEXIF DATA")
    else:
        print("\nNO EXIF DATA FOUND")
        return

    for tag_id in exif_data:
        tag = TAGS.get(tag_id, tag_id)
        data = exif_data.get(tag_id)
        print(f"{tag}: {data}")

    print("\nLOCATION DATA")

    if not gps_data:
        print("NO GPS DATA FOUND")
        return

    gps_parsed = {}

    for key in gps_data:
        name = GPSTAGS.get(key, key)
        gps_parsed[name] = gps_data[key]

    lat = gps_parsed.get("GPSLatitude")
    lat_ref = gps_parsed.get("GPSLatitudeRef")
    lon = gps_parsed.get("GPSLongitude")
    lon_ref = gps_parsed.get("GPSLongitudeRef")

    if lat and lon:
        lat_val = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / 3600
        lon_val = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / 3600

        if lat_ref != "N":
            lat_val = -lat_val
        if lon_ref != "E":
            lon_val = -lon_val

        reverse = reverse_geocode.search([(lat_val, lon_val)])
        country = reverse[0]["country"]
        city = reverse[0]["city"]

        print(f"Country: {country}")
        print(f"City: {city}")
        print(f"Latitude: {lat_val}")
        print(f"Longitude: {lon_val}")

        # The web link stuff
        print(f"Google maps link: https://www.google.com/maps?q={lat_val},{lon_val}")
        print(f"What 3 words link: https://what3words.com/{lat_val},{lon_val}")
