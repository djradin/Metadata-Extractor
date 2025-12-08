import os
import time
from pymediainfo import MediaInfo
from PIL import Image
from PIL.ExifTags import TAGS

filePath = input("Please enter the file path: ")


def filediagnose(filePathDiagnose):
    """
    Takes the filepath, gives the generic metadata, then gives also sends certain
    file types to other functions for more type-specific metadata.
    :param filePathDiagnose: The file path of the file to be analysed.
    :return:
    """
    if os.path.isfile(filePathDiagnose):
        # I want to filter the quotation marks when
        # copying and pasting from file explorer,
        # but this will not matter when I update to GUI drag and drop method.

        filename, fileext = os.path.splitext(filePathDiagnose)

        # Creation Time
        timecreate = os.path.getctime(filePathDiagnose)
        timecreatereadable = time.ctime(timecreate)

        # Accessed Time
        timeaccess = os.path.getatime(filePathDiagnose)
        timeaccessreadable = time.ctime(timeaccess)

        # Modified Time
        timemod = os.path.getmtime(filePathDiagnose)
        timemodreadable = time.ctime(timemod)

        print("\nBASIC INFORMATION")

        # Prints the data
        # Name and extension
        print("File Name: " + filename)  # Gets the file name from the split file name.
        print("File Extension: " + fileext)  # Literally the same thing but for extension.

        # Time information
        print("File Created: " + timecreatereadable)
        print("File Accessed: " + timeaccessreadable)
        print("File Modified: " + timemodreadable)

        # For sending to EXIF and video metadata
        if fileext == ".jpeg" or fileext == ".jpg":
            getexifdata(filePath)
        elif fileext == ".mov" or fileext == ".mp4" or fileext == ".ogg"\
                or fileext == ".mp3" or fileext == ".wav":
            getmediadata(filePath)
    else:
        print("File does not exist.")


def getexifdata(filePathExif):
    """
    Gives EXIF data for JPEG files.
    :param filePathExif: File path for the image file to get EXIF data from.
    :return:
    """
    exiffile = Image.open(filePathExif)
    exifdatadata = exiffile.getexif()
    if exifdatadata:
        print("\nEXIF DATA")
    else:
        print("\nNO EXIF DATA FOUND")

    # With help from https://stackoverflow.com/questions/64113710/extracting-gps-coordinates-from-image-using-python
    for tag_id in exifdatadata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdatadata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        print(tag + ": " + str(data))

    # Coordinates
    print("\nLOCATION DATA")


def getmediadata(filePathVideo):
    """
    Give Metadata from media files.
    :param filePathVideo: File path for the file to get metadata from.
    :return:
    """
    # Was going to do this purely for video but realised it works for audio too.
    # With help from https://pymediainfo.readthedocs.io/en/stable/introduction.html#id4
    mediadata = MediaInfo.parse(filePathVideo)
    for track in mediadata.tracks:
        if track.track_type == "Video":
            print("\nVIDEO DATA")
            print("Track type: Audio")
            print("Bit rate: " + str(track.bit_rate))
            print("Frame rate: " + str(track.frame_rate))
            print("Format: " + str(track.format))
            print("Duration :" + track.other_duration[1])
        elif track.track_type == "Audio":
            print("\nAUDIO DATA")
            audiodata = track.to_data()
            for key, value in audiodata.items():
                if "other" in key.lower() or "kind" in key.lower():
                    continue
                if "duration" in key.lower():
                    value = str(value) + "ms"
                print(key + ": " + str(value))



filediagnose(filePath)
