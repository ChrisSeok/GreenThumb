import os
import csv

# specify the directory path
directory_path = r"C:\Users\user\Desktop\archive\Plant_Data\Plant_Data\test"

# get all the file names in the directory
file_names = os.listdir(directory_path)
print(len(file_names))

file_names = [s.replace('_', ' ') for s in file_names]
# print(file_names)


# with open('Eng_mod_list.csv', 'r') as f:
#     reader = csv.reader(f)
#     englist = list(reader)[0]
# print(len(englist))

# count = 0
# for a in englist:
#     for b in file_names:
#         if set(a.split()) & set(b.split()):
#             count += 1
#             print(a,"&&&",b)
#             break  # stop inner loop if match is found
# print(count)


# with open('kaggle_hor_list.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     for row in file_names:
#         writer.writerow([row])