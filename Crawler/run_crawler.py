import seleniumCrawler_tuple
import seleniumCrawler
from datetime import datetime
import csv
from tqdm import tqdm
import logging
import os

#로그 폴더 생성. 필요시 path수정
log_dir = os.getcwd() + '\Log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# Data 폴더 생성
data_dir = os.getcwd() + '\Data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

#csv read
with open(r"C:\Users\user\OneDrive\바탕 화면\plantcrawllist.csv", 'r') as f:
    reader = csv.reader(f)
    read = list(reader)

crawllist=[]
for ele in read:
    try:
        pair=(ele[2],(ele[3].split(','))[0],ele[3].split(',')[1])
    except:
        pair=(ele[2],(ele[3].split(','))[0],ele[0])
    crawllist.append(pair)


#searchterm이 list일때
for searchterms in tqdm(crawllist[53:54]):
    print((searchterms[0])) #str
    log_file = os.path.join(log_dir, f"{searchterms[0]}.log")
    seleniumCrawler_tuple.ImageCrawl(searchterms,log_file,data_dir)

# # searchterm이 string일때
# crawllist=['search keyword']
# for searchterm in tqdm(crawllist):
#     log_file = os.path.join(log_dir, f"{searchterm}.log")
#     print(searchterm)
#     seleniumCrawler.ImageCrawl(searchterm,log_file,data_dir)