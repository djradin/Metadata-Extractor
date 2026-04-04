# Since multiple file types have the same magic bytes, namely wav and avi as well as office files and zips
# I made this to stop them just being grouped into one.

import zipfile

def zip_or_office(path):
    """
    Finds out whether the file is zip or an office file via the "Content type" header.
    """
    with zipfile.ZipFile(path, "r") as zFile:
        names = zFile.namelist()
        if "[Content_Types].xml" in names:
            if any(n.startswith("word/") for n in names):
                return "docx"
            elif any(n.startswith("xl/") for n in names):
                return "xlsx"
            elif any(n.startswith("ppt/") for n in names):
                return "pptx"
        return "zip"

def avi_or_wav(path):
    """
    Finds out whether the file is a wav file or an avi file via the bytes after the file size (IDK if there's a better way of doing this).
    """
    with open(path, "rb") as f:

        if f[8:12] == b"\x57\x41\x56\x45":
            return "wav"
        elif f[8:12] == b"\x56\x49\x20":
            return "avi"

