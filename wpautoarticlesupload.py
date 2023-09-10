import requests
import subprocess
import urllib.request
import webbrowser
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import threading
import time
import requests
import base64
import json
import feedparser
import requests # request img from web
import shutil # save img locally
from bs4 import BeautifulSoup as BSHTML
import os
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.chrome.service import Service

openai.api_key = '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'

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("campaigns-317204-c9d6f98922b5.json", scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
ss = file.open("Reetik -work")  #open sheet
ws = ss.worksheet('poster')
ws2 = ss.worksheet('application-pass')



x=1
row=1
while (x<6):
    feed=ws2.cell(x, 8).value

    # Parse Upwork URL
    d = feedparser.parse(feed)

    content=2;
    for n in range(5,len(d.entries)):
        try:
            #options = webdriver.ChromeOptions()
            #options.add_argument("headless")
            service = Service(executable_path='chromedriver.exe')
            driver = webdriver.Chrome(service=service)
            #driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://www.paraphrase-online.com")
            time.sleep(21)
            driver.find_element(By.ID, "2").click()
            driver.find_element(By.ID, "input-data").click()
            inputgiven = driver.find_element(By.ID, "input-data").send_keys(d.entries[n].description)
            time.sleep(11)
            driver.find_element(By.CLASS_NAME, "close-adhesive").click()
            driver.find_element(By.CLASS_NAME, "phraseit").click()						
            time.sleep(21)
            ws.update_cell(content, 1, d.entries[n].title)
            ws.update_cell(content, 2, driver.find_element(By.ID, "output-data").text)
            ws.update_cell(content, 3, d.entries[n].thumbimage)
            content=content+1;
            driver.close();
            time.sleep(3)
        except:
            print('error')
    
    r=2
    torun=ws.cell(r, 1).value;
    torun=str(torun)
    count=0

    while (torun != "None"):
        if(count>7):
            count=0
            row=row+1
        url = ws.cell(r, 3).value
        file_name = 'one.jpg'

        res = requests.get(url, stream = True)

        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved')


        username = ws2.cell(row, 1).value;
        password = ws2.cell(row, 2).value;

        creds = username + ':' + password
        cred_token = base64.b64encode(creds.encode())

        header = {'Authorization': 'Basic ' + cred_token.decode('utf-8')}

        url = ws2.cell(row, 3).value;

        image = {
        "file": open("one.jpg", "rb"),
        "caption": "caption",
        "description": "description"
        }

        blog_img = requests.post(url + '/media' , headers=header, files=image)
        print('image posted')
        a = json.loads(blog_img.content)
        media_id=a['id']        
        
        post = {
         'title' : ws.cell(r, 1).value,
         'content' : ws.cell(r, 2).value,
         "featured_media": media_id,
         'status' : 'publish'
        }

        blog = requests.post(url + '/posts' , headers=header, json=post)
        #blog_img = requests.post(url + '/media' , headers=header, files=image)
        print('article posted')
        print(blog)
        #print(blog_img)
        count=count+1
        r=r+1;
        torun=ws.cell(r, 1).value;
        torun=str(torun)
        time.sleep(60)

    x=x+1;
    row=row+1;
    time.sleep(60)


