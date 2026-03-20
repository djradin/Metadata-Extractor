# Hopefully after removing the bloat from this it can stay fairly minimal on this file.

import fileHandling
import basicFileInfo
import userLogin

current_user = userLogin.login_start()
print(f"Current user: {current_user}")

repeat = "yes"
choice = ""

while repeat == "yes":
    while choice not in ["diagnose", "load"]:
        choice = input("Would you like to diagnose a file, or load a file? ")
        if choice.lower() == "diagnose":
            choice = ""
            file_path = input("Please enter the file path: ").strip('"')
            metadata = basicFileInfo.diagnose_file(file_path)
            fileHandling.save_file(current_user, metadata)
        elif choice.lower() == "load":
            choice = ""
            files = fileHandling.list_files(current_user)
            selected_file = ""

            if not files:
                print("No files saved to user, please process a file first.")
            else:
                for i, f in enumerate(files, 1):
                    print(f"{i}. {f}")

                while selected_file not in files:
                    selected_file = input("Please choose a file to load: ")
                    data = fileHandling.load_file(current_user, selected_file)
                    if not data:
                        continue
                    else:
                        print(f"Metadata for: {selected_file}")
                        print(data)



        else:
            print("please choose either 'diagnose' or 'load'.")

    repeat = input("Would you like to analyse another file?").lower()

print("Closing Program.")
exit()








