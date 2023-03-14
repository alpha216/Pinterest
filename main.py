import selenium, time, re, aiohttp, aiofiles, asyncio, os, json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def crowl(_url):
    driver.get(url=_url)
    prev_height = driver.execute_script("return document.body.scrollHeight")

    origin = []
    dir_name = 'image'
    count = 1
    while True:
        # Scroll to the bottom
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(10)
        curr_height = driver.execute_script("return document.body.scrollHeight")
        if(curr_height == prev_height):
            req = driver.page_source
            soup=BeautifulSoup(req, 'html.parser')
            
            img_link = soup.find_all('img', attrs = {'srcset' : True})
            #find       
            for n in img_link:
                n = n['srcset']
                try:
                    m = re.search('3x, (.+?) 4x', n)
                    found = m.group(1)
                except:
                    m = re.search('2x, (.+?) 3x', n)
                    found = m.group(1)
                if found in origin:
                    pass
                else:
                    origin.append(found)
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")
            #go to bs4      
            req = driver.page_source
            soup=BeautifulSoup(req, 'html.parser')
            img_link = soup.find_all('img', attrs = {'srcset' : True})
            if count == 1:
                dir_name = soup.find('h1').text.strip()
                print(dir_name)
            #find       
            for n in img_link:
                n = n['srcset']
                try:
                    m = re.search('3x, (.+?) 4x', n)
                    found = m.group(1)
                except:
                    m = re.search('2x, (.+?) 3x', n)
                    found = m.group(1)
                if found in origin:
                    pass
                else:
                    origin.append(found)
            print('next')
            count += 1

    print(len(origin))

    #make a diractory
    directory = f'./{dir_name}'
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
    print('download')

    #download image
    n = 1
    for i in origin: 
        with urlopen(i) as f:
            with open(f'./{dir_name}/img' + str(n)+'.jpg','wb') as h: 
                img = f.read()
                h.write(img)
        n += 1

if __name__ == "__main__":
    info = json.load(open("./info.json"))
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.set_window_size(100000, 100000)
    driver.get('https://www.pinterest.com/login')

    mail = driver.find_element_by_xpath('//*[@id="email"]')
    mail.send_keys(info["id"])
    password = driver.find_element_by_xpath('//*[@id="password"]')
    password.send_keys(info["password"])
    submit = driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div[3]/form/div[5]/button')
    submit.send_keys(Keys.RETURN)

    time.sleep(5)
    
    for i in info['links']: 
        crowl(i)