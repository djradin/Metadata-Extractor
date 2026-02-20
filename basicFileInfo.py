import os, time, hashlib

def get_basic_info(path):
    filename, ext = os.path.splitext(path)

    time_create = time.ctime(os.path.getctime(path))
    time_access = time.ctime(os.path.getatime(path))
    time_modified = time.ctime(os.path.getmtime(path))

    print("\nBASIC INFORMATION")
    print("File Name:", filename)
    print("File Extension:", ext)
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
