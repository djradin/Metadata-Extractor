import os, time, hashlib

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
