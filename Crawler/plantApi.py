import json
import pprint
import xmltodict, json
import requests
import bs4
import csv
from tqdm import tqdm

#gardenList

#getting cntntsSj(식물 한글명),cntntsNo(식물번호)
# url = 'http://api.nongsaro.go.kr/service/garden/gardenList'
# params = {'apiKey':'20230323J3HRG9YWSTT0TD7YMQQFQQ',
#           'numOfRows':'300',
#           'pageNo':'1'
#         }
# res = requests.post(url,params)

# xmlToJsonConverter = xmltodict.parse(res.text)
# resultList = json.loads(json.dumps(xmlToJsonConverter))

# datalen= len(resultList['response']['body']['items']['item'])
# print(datalen)
# plantnameNo = []
# for i in tqdm(range(datalen)):
#         name = (resultList['response']['body']['items']['item'][i]['cntntsSj'])
#         no = (resultList['response']['body']['items']['item'][i]['cntntsNo'])
#         plantnameNo.append([name,no])






# gardenDtl (상세정보) : cntno를 가지고 각 식물의 상세정보 가져옴
# 학명: plntbneNm
#cntnoList 파일 열기
Englist=[]
cntlist = []
with open('cntnoList.csv', 'r') as f:
    reader = csv.reader(f)
    cntlist = list(reader)[0]
# print((cntlist))

#상세정보 출력
url = 'http://api.nongsaro.go.kr/service/garden/gardenDtl'

# for cnt in tqdm(list(cntlist[:5])):
for cnt in tqdm((cntlist)):

        params = {'apiKey':'20230323J3HRG9YWSTT0TD7YMQQFQQ',
                'cntntsNo': cnt
                #   'numOfRows':'1000'
                #   'pageNo':'1'
                }

        res = requests.post(url,params)

        xmlToJsonConverter = xmltodict.parse(res.text)
        resultList = json.loads(json.dumps(xmlToJsonConverter))
        # print(resultList)
        res = resultList['response']['body']['item']
        formatted_result = json.dumps(res, indent=4)
        # print(formatted_result)

        # item = resultList['response']['body']['item']['plntbneNm'] #마지막은 변수명.변경
        print(resultList['response']['body']['item']['plntbneNm'],"\n",
                resultList['response']['body']['item']['plntzrNm'],"\n",
                resultList['response']['body']['item']['orgplceInfo'],"\n",
                resultList['response']['body']['item']['adviseInfo'],"\n",
                resultList['response']['body']['item']['growthHgInfo'],"\n",
                resultList['response']['body']['item']['toxctyInfo'],"\n",
                resultList['response']['body']['item']['prpgtEraInfo'],"\n",
                resultList['response']['body']['item']['grwhTpCodeNm'],"\n",
                resultList['response']['body']['item']['hdCodeNm'],"\n",
                resultList['response']['body']['item']['watercycleAutumnCodeNm'],"\n",
                resultList['response']['body']['item']['speclmanageInfo'],"\n",
                resultList['response']['body']['item']['fncltyInfo'],"\n",
                )



        # print(item)
        # Englist.append(item)
        break




# with open('scientific_name.csv','w',newline='')as f:
#       writer = csv.writer(f)
#       for each in Englist:
#         writer.writerow([each])



# #getting plntzrNm(영명)
# Englist = []
# url = 'http://api.nongsaro.go.kr/service/garden/gardenDtl'

# for cnt in tqdm(cntlist):

#         params = {'apiKey':'20230323J3HRG9YWSTT0TD7YMQQFQQ',
#                 'cntntsNo': cnt
#                 #   'numOfRows':'1000'
#                 #   'pageNo':'1'
#                 }

#         res = requests.post(url,params)

#         xmlToJsonConverter = xmltodict.parse(res.text)
#         resultList = json.loads(json.dumps(xmlToJsonConverter))
#         # print(resultList)
#         res = resultList['response']['body']['item']
#         formatted_result = json.dumps(res, indent=4)
#         # print(formatted_result)

#         words = resultList['response']['body']['item']['plntzrNm']
#         word = words.split(',')[0]
#         Englist.append(word)
#         print(Englist)
        
        


# #list 를 csv로 저장
# with open('Eng_api_217_nodup.csv','w',newline='')as f:
#         writer = csv.writer(f)
#         writer.writerow(Englist)

# #리스트를 json으로 저장
# file_path = r"C:\Users\user\Desktop\plantlist.json"
# with open(file_path,'w')as f:
#     json.dump(resultList,f)