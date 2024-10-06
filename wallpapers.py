
#Written from scratch. Enjoy your wallpapers :P

import requests,time,os,threading
from bs4 import BeautifulSoup

def makeUrls():
    url_prefix = "https://storage.googleapis.com/panels-api/"
    try:
        res = requests.get(url_prefix)
        res.raise_for_status()
        if res.status_code == 200:
            data  = BeautifulSoup(res.text,'lxml-xml')
            endpoints = [content.find_all("Key")[0].string for content in data.find_all("Contents")]
            return [(url_prefix +  endpoint)  for endpoint in endpoints if "-p~uhd" in endpoint]
    except requests.exceptions.RequestException as e :
        print("ERROR WHILE GETTING URLS",e)
 
def getMasterDataList(urlList):
    mainData = []
    for url in urlList:
        try:
            res = requests.get(url)
            res.raise_for_status()
            if res.status_code == 200:
                mainData.append(res.json()["data"])
                time.sleep(1)
                return mainData
        except requests.exceptions.RequestException as e:
            print("ERROR WHILE GETTING MASTER DATA",e)
   
       
def downloadImage(imgUrl,fileIndex,imgSizeType):
    if not os.path.exists(f"wallpapers/{imgSizeType}"):
        os.makedirs(f"wallpapers/{imgSizeType}") 
    try:
        res = requests.get(imgUrl)
        if res.status_code == 200:
            file_path = os.path.join(f"wallpapers/{imgSizeType}",f"{fileIndex}.jpg")    
            with open(file_path,"wb") as file:
                file.write(res.content)
        
    except requests.exceptions.RequestException as e:
        print("ERROR WHILE DOWNLOADING IMAGE",e)
    

def requestDownload(links,imgSizeType):
    for index,url in enumerate(links):
        downloadImage(url,index + 1,imgSizeType)
        print(f"Downloaded image {index + 1}/{len(links)}")
    
    
def createThreads(data):
    threads = []
    for key in data:
        thread = threading.Thread(target=requestDownload,args=[data[key],key])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("\t\t\t\t\t\t\t\t All wallpapers downloaded")
        
def getSizeSortedLinks(data):
    sizeSortedList = {}
    for rootId in data:
        for sizes in rootId.values():
            for size in sizes.keys():
                if size not in ["am","as","e"]:
                    if size not in sizeSortedList:
                        sizeSortedList[size] = []
                    sizeSortedList[size].append(sizes[size])
    return sizeSortedList
                  
print("\t\t\t\t\t\t\t\t Starting the download \n \t\t\t\t\t\t\t\t Sit back and relax")  
urlList = makeUrls()
time.sleep(1)
masterDataList = getMasterDataList([urlList[0]])
sortedGroup = getSizeSortedLinks(masterDataList)
createThreads(sortedGroup)