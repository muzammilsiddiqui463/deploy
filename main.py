import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import csv
import os
import traceback
import random
from selenium.webdriver.common.keys import Keys
import pickle

# Replace 'http://username:password@your_proxy_url' with the actual proxy URL, username, and password
proxy_url = 'http://avzxawjz-rotate:43eiaf24ra8o@p.webshare.io:80'
proxy = {'http': proxy_url, 'https': proxy_url}
input_file = "keywords.csv"

# Define the static variable for the number of URLs to download
URL_count = 30

csv_fieldnames = ['Description and Tags', 'Video ID', 'Likes', 'Comments', 'Shares', 'Views',
                  'Video Path', 'Keyword']
# Create CSV content
csv_content = '\n'.join(','.join(map(str, row_data)) for row_data in [csv_fieldnames])
csv_data = []
sub_threads = []

def downloadVideo(link, id, keyword):
    global proxy,csv_data,csv_content
    print(f"Downloading video {id} from: {link} for {keyword}")
    
    # Cookies and headers for the HTTP request
    cookies = [{
        '_ga': 'GA1.1.549270780.1705679996',
        '__gads': 'ID=7d03875a6c226889:T=1705679998:RT=1705679998:S=ALNI_MZUj747_RPWHjsIS31bp53DVJTuPA',
        '__gpi': 'UID=00000cfb661fc03d:T=1705679998:RT=1705679998:S=ALNI_MZw5PXr24ZQmMzpdEJJImSXFfK05Q',
        'FCNEC': '%5B%5B%22AKsRol__ju4wfJ4QUcQuTKMa1NZ7DIpROf6OEhZ62gQbm59rpvYLE-AULmFAML8v3JFtR5Zm148o88hc3HgrJammf3lBzXKZfZsdLz14aCJ9iMPXLP7OHDFlBTTe_k6N2pChVgHupq3xntVfL-KZPd7wfgiRbk52Hg%3D%3D%22%5D%5D',
        '_ga_0E6L67P48P': 'GS1.1.1705679996.1.0.1705680005.0.0.0',
    },
        {
            '_ga': 'GA1.1.1368246834.1705679183',
            '__gads': 'ID=6ace672e87a29587:T=1705679184:RT=1705679184:S=ALNI_MZCFx8Sd6tfmVIuCZodCd0YR7ZJrQ',
            '__gpi': 'UID=00000cfb642de669:T=1705679184:RT=1705679184:S=ALNI_Ma_DjQn4Zg2pA0MuA0LgVao2UU7QQ',
            'FCNEC': '%5B%5B%22AKsRol9MIRnjpAqWOn6XORyyCSPo5BzlOfWrtWliuHbh-_VOHtI8QDWZRTgZgBHZpZyaGP624iVNINoMA_jD2QLf34XD5q1Fplc8WF7qLl5ZYe2qZ0Aacwb0GLyXkPJjJdSBRQ-I4q0_RaOBLdiuGkKafwwyvuYPVQ%3D%3D%22%5D%5D',
            '_ga_0E6L67P48P': 'GS1.1.1705679182.1.0.1705679219.0.0.0',
        },
        {
            '_ga': 'GA1.1.1827974823.1705680537',
            '__gads': 'ID=2c23abaec0d8b1a7:T=1705680536:RT=1705680536:S=ALNI_MYeGxmOayQYHodj1WPvVRAHq9-rLA',
            '__gpi': 'UID=00000db878254fac:T=1705680536:RT=1705680536:S=ALNI_MbUzb5aMUy86DhELsWemfmhNFi-jQ',
            'FCNEC': '%5B%5B%22AKsRol_tKV79J7BPHljCMIygpyV6k0s_rkJyyVglzYNVpkKjcrF1qV3JL_nkAylnXsozL3HkCJJqx37unV2w1MRepYQ1uX2hq3JW2otXqB1bcHPTksAqAT7XZq9qldXYeJ2G5uaVDdp_x0no_Q-wZChAGY8YNxFENw%3D%3D%22%5D%5D',
            '_ga_0E6L67P48P': 'GS1.1.1705680536.1.0.1705680569.0.0.0',
        }
    ]

    headers = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
         'Accept': '*/*',
         'Accept-Language': 'en-US,en;q=0.5',
         # 'Accept-Encoding': 'gzip, deflate, br',
         'HX-Request': 'true',
         'HX-Trigger': '_gcaptcha_pt',
         'HX-Target': 'target',
         'HX-Current-URL': 'https://tiktokdownload.online/',
         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
         'Origin': 'https://tiktokdownload.online',
         'DNT': '1',
         'Alt-Used': 'tiktokdownload.online',
         'Connection': 'keep-alive',
         'Referer': 'https://tiktokdownload.online/',
         # 'Cookie': '_ga_0E6L67P48P=GS1.1.1705679158.1.1.1705680241.0.0.0; _ga=GA1.1.1577407249.1705679159; __gads=ID=d66d29c1bdd24aea:T=1705679161:RT=1705679161:S=ALNI_MalLdqkP35udomzEn5HHHIu2bcW1Q; __gpi=UID=00000cfb654ef41c:T=1705679161:RT=1705679161:S=ALNI_MbWM0h6m2f4TLO0l7z4DWOYa2GGyQ; FCNEC=%5B%5B%22AKsRol_hHyf4p2hsj2hGcfMX6buQx_VKK3yymLtjWokB2eIQccBeXGaJUTHEfE8HB2iTNT_oFKZxG_OMAndnCJHGn4GVgV1T8o3w7tJylMDXUiTCfBxeVH24XzEK32PtMstwBgrW_N1LYPwH2lGTod67_946RKvjuQ%3D%3D%22%5D%5D',
         'Sec-Fetch-Dest': 'empty',
         'Sec-Fetch-Mode': 'cors',
         'Sec-Fetch-Site': 'same-origin', },
        {'authority': 'tiktokdownload.online',
         'accept': '*/*',
         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
         # 'cookie': '_ga=GA1.1.1368246834.1705679183; __gads=ID=6ace672e87a29587:T=1705679184:RT=1705679184:S=ALNI_MZCFx8Sd6tfmVIuCZodCd0YR7ZJrQ; __gpi=UID=00000cfb642de669:T=1705679184:RT=1705679184:S=ALNI_Ma_DjQn4Zg2pA0MuA0LgVao2UU7QQ; FCNEC=%5B%5B%22AKsRol9MIRnjpAqWOn6XORyyCSPo5BzlOfWrtWliuHbh-_VOHtI8QDWZRTgZgBHZpZyaGP624iVNINoMA_jD2QLf34XD5q1Fplc8WF7qLl5ZYe2qZ0Aacwb0GLyXkPJjJdSBRQ-I4q0_RaOBLdiuGkKafwwyvuYPVQ%3D%3D%22%5D%5D; _ga_0E6L67P48P=GS1.1.1705679182.1.0.1705679219.0.0.0',
         'hx-current-url': 'https://tiktokdownload.online/',
         'hx-request': 'true',
         'hx-target': 'target',
         'hx-trigger': '_gcaptcha_pt',
         'origin': 'https://tiktokdownload.online',
         'referer': 'https://tiktokdownload.online/',
         'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
         'sec-ch-ua-mobile': '?0',
         'sec-ch-ua-platform': '"Windows"',
         'sec-fetch-dest': 'empty',
         'sec-fetch-mode': 'cors',
         'sec-fetch-site': 'same-origin',
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
         },
        {
            'authority': 'tiktokdownload.online',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_ga=GA1.1.1827974823.1705680537; __gads=ID=2c23abaec0d8b1a7:T=1705680536:RT=1705680536:S=ALNI_MYeGxmOayQYHodj1WPvVRAHq9-rLA; __gpi=UID=00000db878254fac:T=1705680536:RT=1705680536:S=ALNI_MbUzb5aMUy86DhELsWemfmhNFi-jQ; FCNEC=%5B%5B%22AKsRol_tKV79J7BPHljCMIygpyV6k0s_rkJyyVglzYNVpkKjcrF1qV3JL_nkAylnXsozL3HkCJJqx37unV2w1MRepYQ1uX2hq3JW2otXqB1bcHPTksAqAT7XZq9qldXYeJ2G5uaVDdp_x0no_Q-wZChAGY8YNxFENw%3D%3D%22%5D%5D; _ga_0E6L67P48P=GS1.1.1705680536.1.0.1705680569.0.0.0',
            'hx-current-url': 'https://tiktokdownload.online/',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://tiktokdownload.online',
            'referer': 'https://tiktokdownload.online/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    ]

    params = {
        'url': 'dl',
    }
    codes = ['eHc4a3lm', 'aVZQQTM1']
    code_i = 0
    for i in range(200):
        try:
            try:
                data = {
                    'id': link,
                    'locale': 'en',
                    'tt': codes[code_i],
                }
                code_i += 1
            except:
                code_i = 0
                data = {
                    'id': link,
                    'locale': 'en',
                    'tt': codes[code_i],
                }
            response = requests.post('https://tiktokdownload.online/abc',
                                     params=params,
                                     cookies=cookies[random.randrange(0, len(cookies))],
                                     headers=headers[random.randrange(0, len(headers))],
                                     data=data,
                                     )
            downloadSoup = BeautifulSoup(response.text, "html.parser")

            downloadLink = downloadSoup.a["href"]
            break
        except:
            time.sleep(0.5)

    def sub_thread(downloadLink, id, keyword, link):
        global csv_content,csv_data
        # Function to save the video

        # # Create the 'videos' directory if it doesn't exist
        # videos_dir = 'videos'
        # os.makedirs(videos_dir, exist_ok=True)
        #
        # # Create a subfolder inside 'videos' based on the keyword
        # keyword_folder = os.path.join(videos_dir, keyword)
        # os.makedirs(keyword_folder, exist_ok=True)

        # video_path = os.path.join(keyword_folder, f"{id}-{keyword}.mp4")

        # mp4File = urlopen(downloadLink)
        
        # Download and save the video to local
        # with open(video_path, "wb") as output:
        #     while True:
        #         data = mp4File.read(16384)  # You can experiment with different chunk sizes
        #         if data:
        #             output.write(data)
        #         else:
        #             break

        # Download and save the video to Bunny CDN
        bunny_url = f'https://NY.storage.bunnycdn.com/tiktok-scraper/{keyword}/{id}-{keyword}.mp4'
        headers = {
            'AccessKey': "82a52388-ed4f-4279-80ee2f752b7c-8662-4259",
            'Content-Type': 'application/octet-stream'
        }
        try:
            with urlopen(downloadLink) as mp4File:
                with requests.put(bunny_url, headers=headers, data=mp4File.read()) as response:
                    print(response.text)

        except Exception as e:
            print(f"Error uploading file: {e}")


        # Get video data from TikTok (likes, comments, shares, views)
        data = get_data(link)
        if data != None:
            like, comment, share, view, videoTitle = data
        else:
            like, comment, share, view, videoTitle = ["", "", "", "", ""]
        
        # Save video path and details to CSV to LOCAL
        # with open(f'output_{keyword}.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        #     fieldnames = ['Description and Tags', 'Video ID', 'Likes', 'Comments', 'Shares', 'Views',
        #                   'Video Path', 'Keyword']
        #     writer = csv.writer(csvfile)
        #
        #     # If the file is empty, write the header
        #     if os.path.getsize(f'output_{keyword}.csv') == 0:
        #         writer.writerow(fieldnames)
        #
        #     writer.writerow([
        #         videoTitle,
        #         id,
        #         like,
        #         comment,
        #         share,
        #         view,
        #         video_path,
        #         keyword,
        #     ])
        data = [
                str(videoTitle).replace(",","|"),
                str(id),
                str(like),
                str(comment),
                str(share),
                str(view),
                f"{id}-{keyword}.mp4",
                keyword,
            ]



        data = ",".join(data)
        csv_content += '\n'+data



        headers = {
            'AccessKey': "82a52388-ed4f-4279-80ee2f752b7c-8662-4259",
            'Content-Type': 'text/csv'
        }
        bunny_url = f'https://NY.storage.bunnycdn.com/tiktok-scraper/{keyword}/Output_{keyword}.csv'

        try:
            with requests.put(bunny_url, headers=headers, data=csv_content) as response:

                return response.ok
        except Exception as e:
            print(f"Error uploading CSV file: {e}")
            return False

        #Save Video to BunnyCDN

    if downloadLink is not None:
        # Only start the thread if downloadLink is not None
        s = threading.Thread(target=sub_thread, args=(downloadLink, id, keyword, link,))
        s.start()

def find_des(data):
    #shareMeta
    if isinstance(data, dict):
        if 'shareMeta' in data:
            return data['shareMeta']
        for key, value in data.items():
            result = find_des(value)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_des(item)
            if result:
                return result
def find_stats(data):
    # Function to find video statistics in the JSON-like data
    if isinstance(data, dict):
        if 'stats' in data:
            return data['stats']
        for key, value in data.items():
            result = find_stats(value)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_stats(item)
            if result:
                return result

def get_data(link):
    # Function to get video data (likes, comments, shares, views) from TikTok
    global proxy
    headers = {
    'authority': 'mcs-va.tiktokv.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://www.tiktok.com',
    'referer': 'https://www.tiktok.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        r = requests.get(link, headers=headers, proxies=proxy)
    except:
        return None
    videoSoup = BeautifulSoup(r.content, "html.parser")

    # Find the script tag that contains the JSON-like data
    script_tags = videoSoup.find_all('script')

    for script_tag in script_tags:
        if script_tag:

            # Extract the content of the script tag
            json_like_text = script_tag.text
            try:
                # Load the JSON-like text into a Python dictionary
                json_data = json.loads(json_like_text)
            except Exception as e:
                continue
            # Find the stats information using the recursive function
            stats_info = find_stats(json_data)
            if stats_info:
                des = find_des(json_data)
                if des != None:

                    des = des['desc']
                else:
                    des = ""
                return (stats_info['diggCount'], stats_info['commentCount'], stats_info['shareCount'],
                        stats_info['playCount'], des)

def start_process(keyword,driver):
    global csv_content,csv_data,csv_fieldnames,sub_threads

    # Change the tiktok link
    driver.get(f"https://www.tiktok.com/search/video?lang=en&q={keyword}&t=1705902142362")
    # Load cookies from the saved file
    with open(os.getcwd()+'/cookies.pkl', 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.save_screenshot("page.png")
    bunny_url = f'https://NY.storage.bunnycdn.com/tiktok-scraper/Tst_screenshots/page.png'
    headers = {
        'AccessKey': "82a52388-ed4f-4279-80ee2f752b7c-8662-4259",
        'Content-Type': 'application/octet-stream'
    }
    with open("page.png", 'rb') as file:
        response = requests.put(bunny_url, headers=headers, data=file)

    # Check the response
    if response.ok:
        print("Screenshot uploaded successfully.")
    else:
        print(f"Error uploading screenshot: {response.status_code}")
    driver.get(f"https://www.tiktok.com/search/video?lang=en&q={keyword}&t=1705902142362")
    # IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
    # to 60 seconds, just enough time for you to complete the captcha yourself.
    time.sleep(15)
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # time.sleep(6)

    # # Change the tiktok link
    # driver.get(f"https://www.tiktok.com/search/video?lang=en&q={keyword}&t=1705902142362")
    # time.sleep(3)
    scroll_pause_time = 3
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    print("STEP 2: Scrolling page")
    urlsToDownload = []


    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")

        className = "css-1as5cen-DivWrapper e1cg0wnj1"
        script = "let l = [];"
        script += "document.getElementsByClassName(\""
        script += className
        script += "\").forEach(item => { l.push(item.querySelector('a').href)});"
        script += "return l;"
        time.sleep(0.8)

        urlsToDownload.extend(driver.execute_script(script))

        if len(urlsToDownload)>=100:
            break

    urlsToDownload=urlsToDownload[:100]
    count=0

    print(f"Scraped {len(urlsToDownload)} video Links")
    threads = []
    for index, url in enumerate(urlsToDownload):


        try:
            # downloadVideo(url, index,keyword)
            s=threading.Thread(target=downloadVideo,args=(url, index,keyword,))
            threads.append(s)


        except Exception as e:

            continue
        # time.sleep(2)
        if count>=100:
            count = 0
            break
        else:
            count+=1
    join_list = []
    count = 0
    for t in threads:
        t.start()
        join_list.append(t)
        if count>20:
            count = 0
            print("Now waiting for current threads to finish.....")
            for j in join_list:
                j.join()
            join_list = []
        else:
            count+=1
        time.sleep(1.6)
    for j in join_list:
        j.join()


def main(csv_file_path):
    global csv_content,csv_data,csv_fieldnames
    # Main function to read keywords from a CSV file and initiate the downloading process
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        print("STEP 1: Open Chrome browser")

        options = uc.ChromeOptions()
        options.user_data_dir = os.getcwd() + "/profile"
        driver = uc.Chrome(options=options)

        for row in csv_reader:
            keyword = row[0]

            # Start Process
            print(f"Downloading Video for keyword {keyword}")
            # Create CSV content
            csv_content = '\n'.join(','.join(map(str, row_data)) for row_data in [csv_fieldnames])
            csv_data = []
            start_process(keyword, driver)

if __name__ == '__main__':
    main(input_file)
