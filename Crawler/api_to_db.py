import json
import pprint
import xmltodict, json
import requests
import bs4
import csv
from tqdm import tqdm
import pymysql

conn = pymysql.connect(
    host='127.0.0.1', 
    user='root', 
    password='yellowkat99', 
    db='plantInfo', 
    charset='utf8')

cursor = conn.cursor()
# conn.commit()
# conn.close()


#gardenList

url = 'http://api.nongsaro.go.kr/service/garden/gardenList'
params = {'apiKey':'20230323J3HRG9YWSTT0TD7YMQQFQQ',
          'numOfRows':'300',
          'pageNo':'1'
        }
res = requests.post(url,params)

xmlToJsonConverter = xmltodict.parse(res.text)
resultList = json.loads(json.dumps(xmlToJsonConverter))

datalen= len(resultList['response']['body']['items']['item'])
print(datalen)
plantnameNo = []
for i in range(datalen):
    korname = (resultList['response']['body']['items']['item'][i]['cntntsSj'])
    cntntsno = (resultList['response']['body']['items']['item'][i]['cntntsNo'])
    cntntsno = int(cntntsno)

    # #cntntsno로 상세정보 가져오기

    urldtl = 'http://api.nongsaro.go.kr/service/garden/gardenDtl'
    paramsdtl = {'apiKey':'20230323J3HRG9YWSTT0TD7YMQQFQQ',
                'cntntsNo': cntntsno
                #   'numOfRows':'1000'
                #   'pageNo':'1'
                }

    resdtl = requests.post(urldtl,paramsdtl)

    xmlToJson = xmltodict.parse(resdtl.text)
    resultlist = json.loads(json.dumps(xmlToJson))
    # print(resultList)
    # result = resultlist['response']['body']['item']
    # formatted_result = json.dumps(result, indent=4)

    sciname =  resultlist['response']['body']['item']['plntbneNm']
    engname = resultlist['response']['body']['item']['plntzrNm']
    origin = resultlist['response']['body']['item']['orgplceInfo']
    advice = resultlist['response']['body']['item']['adviseInfo']
    height = float(resultlist['response']['body']['item']['growthHgInfo'])
    toxic = resultlist['response']['body']['item']['toxctyInfo']
    propa = resultlist['response']['body']['item']['prpgtEraInfo']
    temp = resultlist['response']['body']['item']['grwhTpCodeNm']
    humid = resultlist['response']['body']['item']['hdCodeNm']
    water = resultlist['response']['body']['item']['watercycleAutumnCodeNm']
    special = resultlist['response']['body']['item']['speclmanageInfo']
    function = resultlist['response']['body']['item']['fncltyInfo']

    query = "insert into plantInfo(korname,cntntsNo,sciname,engname,origin,advise,height,toxicity,propagation,temperature,humidity,water,specialinfo,funtioninfo)\
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print(engname)
    try:
        cursor.execute(query,(korname,cntntsno,sciname,engname,origin,advice,height,toxic,propa,temp,humid,water,special,function))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)

