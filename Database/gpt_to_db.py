#OpenAI의 chatGPT API를 사용하여 plantinfo테이블의 specialinfo와 functioninfo 필드가 모두 null인 항목만 식물에 대한 정보를
# 정보를 chatgpt로부터 얻어와 저장한다.
import os
import requests
import openai
import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import googletrans
import pymysql
import pandas as pd
import csv
from tqdm import tqdm
#api key (key 생성 후 결제 필요)
OPENAI_KEY = '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'
openai.api_key = OPENAI_KEY
MODEL = "gpt-3.5-turbo"

#db연결
conn = pymysql.connect(
    host='plantbase.chm1hhurblp4.ap-northeast-2.rds.amazonaws.com', 
    user='admin', 
    password='plant2023', 
    db='plant', 
    charset='utf8')

# plantinfo테이블의 specialinfo와 functioninfo 필드가 모두 null인 항목의 한글명을 가져온다
cursor = conn.cursor()
query = "select korname from plantinfo where specialinfo is null and functioninfo is null"
cursor.execute(query)
result = cursor.fetchall()
result = [each[0] for each in result]
# print(len(result))


#chatGPT API 사용해서 식물 정보 받아오기
for keyword in tqdm(result):
    print(keyword)
    USER_INPUT_MSG = f"식물 {keyword}에 대한 정보를 한 문단으로 알려줘."

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": USER_INPUT_MSG}
            # {"role": "assistant", "content": "Who's there?"},
        ],
        temperature=0,
    )

    functinfo = response['choices'][0]['message']['content']
    print(functinfo)

    insert_query = f'update plantinfo set functioninfo="{functinfo}" where korname="{keyword}";'
    try:
        cursor.execute(insert_query)
        conn.commit()
    except Exception as e:
        print(e)
conn.close()