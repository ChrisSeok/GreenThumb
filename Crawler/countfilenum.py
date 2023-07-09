import os

path = r"C:\Users\user\Desktop\plantData\Data_1"  # directory path
folder_path = os.listdir(path)
print(len(folder_path))
for file in folder_path:
    dir = path+'\\'+file
    print(file,end=' : ')
    file_count = len([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))])
    # print("Number of files in directory:", file_count)
    print(file_count)
    
