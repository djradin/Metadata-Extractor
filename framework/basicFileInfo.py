import os, time, hashlib
from framework import adsFinder, fileSignatures, exifReader, mediaReader


def get_basic_info(path):
    filenameUnsplit = os.path.basename(path)
    filename, ext = os.path.splitext(filenameUnsplit)
    filesize = os.path.getsize(path)
    filesizeKB = round(filesize / 1024, 2)
    filesizeMB = round(filesize / 1048576, 2)
    filesizeGB = round(filesize / 1073741824, 2)
    time_create = time.ctime(os.path.getctime(path))
    time_access = time.ctime(os.path.getatime(path))
    time_modified = time.ctime(os.path.getmtime(path))

    print("\nBASIC INFORMATION")
    print("File Name:", filename)
    print("File Extension:", ext)
    print("File Size (Bytes):", filesize, "Bytes")
    if filesizeKB >= 1:
        print("File Size (Kilobytes):", filesizeKB, "KB")
    if filesizeMB >= 1:
        print("File Size (Megabytes):", filesizeMB, "MB")
    if filesizeGB >= 1:
        print("File Size (Gigabytes):", filesizeGB, "GB")
    print("File Created:", time_create)
    print("File Accessed:", time_access)
    print("File Modified:", time_modified)

    with open(path, "rb") as f:
        file_data=f.read()

    md5_hash = hashlib.md5(file_data)
    sha1_hash = hashlib.sha1(file_data)

    print("\nFILE HASHES")
    print("MD5:", md5_hash.hexdigest())
    print("SHA1:", sha1_hash.hexdigest())

    ## big ass list

    metadata = {
        "File Name" : filename,
        "File Extension" : ext,
        "File Size (bytes)" : filesize,
        "Time Created" : time_create,
        "Time Accessed" : time_access,
        "Time Modified" : time_modified,
        "MD5 Hash" : md5_hash.hexdigest(),
        "SHA1 Hash" : sha1_hash.hexdigest()}

    return metadata

# Shoved this here since it was getting annoying to work around.

def diagnose_file(path):
    if not os.path.isfile(path):
        print("File does not exist.")
        return

    metadata = {}

    basic_info = get_basic_info(path)
    metadata["basic_info"] = basic_info

    ads_info = adsFinder.find_ads(path)
    if ads_info:
        metadata["ads"] = ads_info

    filename, ext = os.path.splitext(path)
    ext = ext.lower().replace(".", "")
    actual_type = fileSignatures.detect_file_type(path)

    if ext != actual_type and actual_type != "unknown":
        match = "extension has been changed"
    else:
        match = "extension is correct"

    file_type_info = {"file_type": actual_type, "file_extension": match}

    metadata["file_extension_integrity"] = file_type_info

    if actual_type in ["jpg"]:
        exif_data = exifReader.get_exif_data(path)
        metadata["exif"] = exif_data

    if actual_type in ["png"]:
        png_data = exifReader.get_png_data(path)
        metadata["png"] = png_data

    if actual_type in ["mp4", "mov", "mp3", "wav", "ogg"]:
        media_data = mediaReader.get_media_data(path)
        metadata["media"] = media_data

    print("\nFILE TYPE CHECK")
    print("Extension File Type:", ext)
    print("Actual File Type:", actual_type)

    if ext != actual_type and actual_type != "unknown":
        print("File extension does not match actual file type.")
    else:
        print("File extension is correct.")

    return metadata