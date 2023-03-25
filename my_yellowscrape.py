import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


url="https://www.yellowpages.com/search?search_terms=event+planners&geo_location_terms=Los+Angeles%2C+CA"
url2="https://www.yellowpages.com/search?search_terms=event+planners&geo_location_terms="
url3="https://www.yellowpages.com/search?search_terms=event%20planners&geo_location_terms="
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
#req=requests.get(url,headers=headers)
# print(req.status_code)
# print(req.request.headers)

name=input("Enter the locationn name:").replace(" ","+")
state=input("Enter the state abbreviation: ").upper()

os.chdir("D:\Python\Web Scraping\Yellow Pages Scrape")

info=pd.DataFrame()

pages=int(input("Enter the number of pages you want to extract: "))
link=None
count=0
for i in range(1,pages+1):
    try:
        if i>1:
            holding=[x+"%20" for x in name.split("+")]
            first="".join(holding[0:len(holding)-1])
            last=holding[len(holding)-1].split('%20')[0]+'%2C'+'%20'+state+"&page="+str(i)
            link=url3+first+last
            #print(link)
        else:
            link=url2+name+"%2C"+"+"+state
            #print(link)
    except:
        print("Error has occured")
    
    req=requests.get(link,headers=headers)
    soup=BeautifulSoup(req.content,features="lxml")
    try:
        #container=soup.find("div",{"class":"search-results organic"})
        another=soup.find_all("div",{"class":"result"})
        for sections in another:
            business_name=sections.find("a",{"class":"business-name"}).text
            #print(business_name)
            category=sections.find("div",{"class":"categories"}).a.text
            #print(category)
            business_years=sections.find("div",{"class":"years-in-business"})
            if business_years!=None:
                business_years=business_years.text
                #print(business_years)
            else:
                business_years="None"
            phone_no=sections.find("div",{"class":"info-section info-secondary"}).div.text
            if phone_no==None:
                phone_no="None"
            #count+=1
            info.loc[len(info),['Name', 'Contact', 'Category', 'Years in Business']] = [business_name, phone_no, category,business_years]
    except:
        print("Error when assigning value")

#print("Total count:",count)
info.to_csv(f'{name}.csv')
        


    
        