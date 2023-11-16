import glob
import pandas as pd
from bs4 import BeautifulSoup
import requests
import shutil
import random
import time

logo_dict = {}
for file in glob.glob('htmls/*'):
    print(file)
    soup = BeautifulSoup(open(file), features='html.parser')

    data = soup.find_all('img')
    for num, img in enumerate(data):
        if img.has_attr('class') and img['class'][0] == 'teamlogo':
            #print(num)
            logo_link = img['src']
    
    school = file.split('\\')[1].split('.')[0]
    #print(school)
    logo_dict[school] = logo_link
    
    
#print(logo_dict)

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
proxy = {'http': '50.218.57.71'}
start = False
for image in logo_dict:
    wait = random.randint(0, 5)
    if image == 'southern-illinois' and not start:
        start = True
    
    if start:
        print(logo_dict[image])
        
        response = requests.get(logo_dict[image], headers=headers, stream = True)
        with open(f'logos\{image}.png', 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        time.sleep(wait)
    

