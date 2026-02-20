import os
from basicFileInfo import get_basic_info
from exifReader import get_exif_data
from mediaReader import get_media_data
from fileSignatures import detect_file_type

file_path = input("Please enter the file path: ").strip('"')


def diagnose_file(path):
    if not os.path.isfile(path):
        print("File does not exist.")
        return

    filename, ext = os.path.splitext(path)
    ext = ext.lower().replace(".", "")

    actual_type = detect_file_type(path)

    get_basic_info(path)

    print("\nFILE TYPE CHECK")
    print("Extension File Type:", ext)
    print("Actual File Type:", actual_type)

    if ext != actual_type and actual_type != "unknown":
        print("File extension does not match actual file type.")

    # Route to handlers
    if actual_type in ["jpg"]:
        get_exif_data(path)

    elif actual_type in ["mp4", "mov", "mp3", "wav", "ogg"]:
        get_media_data(path)


diagnose_file(file_path)