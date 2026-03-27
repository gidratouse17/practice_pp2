import os
#1 shows all files in path ("." is current directory)
my_files = os.listdir('.')
print(my_files)

#2 creating new folder
if not os.path.exists('directory_management/new_folder'):
    os.mkdir('directory_management/new_folder')
    print("Folder is created")
else:
    print("The folder already exists so Im doing nothing")

#3 current directory
current = os.getcwd()
print(f"Current location: {current}")

