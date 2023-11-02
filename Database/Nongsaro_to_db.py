import json
import pprint
import xmltodict, json
import requests
import bs4
import csv
from tqdm import tqdm
import pymysql
import googletrans
translator = googletrans.Translator()
# print(translator.translate("Skill Level: Beginner",dest = 'ko'))

conn = pymysql.connect(
    host='plantbase.chm1hhurblp4.ap-northeast-2.rds.amazonaws.com', 
    user='admin', 
    password='plant2023', 
    db='plant', 
    charset='utf8')

cursor = conn.cursor()


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
# print(datalen)
plantnameNo = []
for i in tqdm(range(datalen)):

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
    height = resultlist['response']['body']['item']['growthHgInfo']
    toxic = resultlist['response']['body']['item']['toxctyInfo']
    propa = resultlist['response']['body']['item']['prpgtEraInfo']
    temp = resultlist['response']['body']['item']['grwhTpCodeNm']
    humid = resultlist['response']['body']['item']['hdCodeNm']
    water = resultlist['response']['body']['item']['watercycleAutumnCodeNm']
    special = resultlist['response']['body']['item']['speclmanageInfo']
    function = resultlist['response']['body']['item']['fncltyInfo']

    query = "insert into plantinfo(korname,cntntsNo,sciname,engname,origin,advise,height,toxicity,propagation,temperature,humidity,water,specialinfo,functioninfo)\
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # query = "alter table plantInfo"
    try:
        cursor.execute(query,(korname,cntntsno,sciname,engname,origin,advice,height,toxic,propa,temp,humid,water,special,function))
        conn.commit()
        # print("success!")
    except pymysql.err.IntegrityError as e:
        pass
    except Exception as e:
        print(korname,e)

        # print("eng:",function)
        # kostr = translator.translate(function, dest='ko')
        # print((kostr.text))
        # function = kostr.text


cursor.close() #cursor는 쿼리를 다 끝냈을 때 (for문 모두) 마지막에 close 한다.
conn.close()  

# Update plantinfo
# set functioninfo = '변경할 값'
# where functioninfo = '해당 값'