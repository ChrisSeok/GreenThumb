# Google Image Crawler


# directory tree
```
📜Eng_api_217_nodup.csv
📜seleniumCrawler.py
📜run_crawler.py
 ┃
📦Data
 ┣ 📂plant1
 ┃ ┣ 📜0.jpg
 ┃ ┣ 📜1.jpg
 ┃      ...
 ┣ 📂plant2
 ┃ ┣ 📜0.jpg
 ┃ ┣ 📜1.jpg
 ┃     ...
📦Log
 ┣ 📜plant1.log
 ┗ 📜plant2.log


``` 
- Eng_api_217_nodup.csv
  - 실내정원용 식물 데이터의 식물의 영문명이 저장된 csv파일. 길이 217
- seleniumCrawler.py
  - 인자로 받은 search word를 구글 이미지에 검색해 나온 이미지를 저장하는 모듈인 ImageCrawl이 위치한다
  - Data 디렉토리 속의 식물명의 폴더를 생성하고 그 속에 수집한 이미지를 저장한다
  - 각 식물명의 이미지를 수집할 때 발생한 로그는 Log 디렉토리 속에 식물명.log 로 저장된다
- run_crawler.py
  - Data 디렉토리와 Log 디렉토리 생성
  - Eng_api_217_nodup.csv파일을 읽어와 리스트로 변환, 리스트의 각 요소들을 for루프에 넣어 ImageCrawl 모듈의 인자로 전달

# 설치가이드

Chrome driver 설치
