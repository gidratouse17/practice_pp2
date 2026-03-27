import os
import shutil
#1 creating a file to copy and delete it later
with open("text_file.txt", "w") as ff:
    ff.write("I want to play Danganronpa")

#2 copying this file
shutil.copy("text_file.txt", "ronpa.txt")
print("File is copied")

#3 deleting this file
if os.path.exists("text_file.txt"):
    os.remove("text_file.txt")
print("The file we created is now deleted")

#4 renaming our new file
if os.path.exists("ronpa.txt"):
     if os.path.exists("danganronpa.txt"):
         os.remove("danganronpa.txt")

os.rename("ronpa.txt", "danganronpa.txt")
print("Our copy has new name now")