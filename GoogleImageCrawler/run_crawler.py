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

#csv 읽어서 리스트로 가져오기
with open('Eng_api_217_nodup.csv', 'r') as f:
    reader = csv.reader(f)
    englist = list(reader)[0]
list = englist[6:7] # list 범위 수정

for searchterm in tqdm(list):
    log_file = os.path.join(log_dir, f"{searchterm}.log")
    print(searchterm)
    seleniumCrawler.ImageCrawl(searchterm,log_file,data_dir)