
import requests
from bs4 import BeautifulSoup
import os

# define search term and number of images to retrieve
search_term = "cat"
num_images = 100

path = r'C:\Users\user\OneDrive\Desktop'
# create directory to store images
if not os.path.exists(search_term):
    os.makedirs(search_term)

# construct URL for Google Image search
url = "https://www.google.com/search?q=" + search_term + "&tbm=isch"

# send HTTP request to the URL and get the response
response = requests.get(url)

# parse the HTML content of the response using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# find all image tags on the page
img_tags = soup.find_all('img')
print(len(img_tags))
# download the first num_images images to the search_term directory
count = 0
for img_tag in img_tags:
    if count == num_images:
        break
    img_url = img_tag['src']
    print(img_url)
    try:
        img_data = requests.get(img_url).content
        with open(os.path.join(search_term, f"{count}.jpg"), 'wb') as f:
            f.write(img_data)
            count += 1
            print(f"Downloaded image {count} of {num_images}")
    except:
        continue
