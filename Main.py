# Hopefully after removing the bloat from this it can stay fairly minimal on this file.

import basicFileInfo
import userLogin

current_user = userLogin.login_start()
print(f"Current user: {current_user}")

repeat = "yes"

while repeat == "yes":
    metadata = []
    file_path = input("Please enter the file path: ").strip('"')
    basicFileInfo.diagnose_file(file_path)

    repeat = input("Would you like to analyse another file?").lower()

print("Closing Program.")








