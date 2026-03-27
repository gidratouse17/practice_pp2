import os
#1 renaming file name
old_file = 'directory_management/twilight.txt'
new_name = 'directory_management/sparkle.txt'

if os.path.exists(old_file):
    os.rename(old_file, new_name)
    print(f"Yay! {old_file} has been renamed to {new_name}")
else:
    print(f" {old_file} wasnt found or already renamed.")

#2 removing a folder
folder_to_remove = 'directory_management/new_folder'

if os.path.exists(folder_to_remove):
    os.rmdir(folder_to_remove)
    print(f"Folder '{folder_to_remove}' has been deleted.")
else:
    print(f" Folder '{folder_to_remove}' does not exist.")

#3 finding absolute path
f_name = 'directory_management/example.txt'
full_path = os.path.abspath(f_name)
print(full_path)