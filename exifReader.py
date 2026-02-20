from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_data(path):
    exif_file = Image.open(path)
    exif_data = exif_file.getexif()

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