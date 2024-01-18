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
from webdriver_manager.chrome import ChromeDriverManager
import traceback
# Replace 'http://username:password@your_proxy_url' with the actual proxy URL, username, and password
proxy_url = 'http://zrscbilj-US-rotate:2u71nkuyuo29@p.webshare.io:80'
# proxy_url = None
proxy = {'http': proxy_url, 'https': proxy_url}
input_file = "keywords.csv"

def downloadVideo(link, id,keyword):
    global proxy
    print(f"Downloading video {id} from: {link} for {keyword}")
    cookies = {
        '_ga': 'GA1.1.940644881.1705262011',
        '__gads': 'ID=c85399c900c8de1c:T=1705262013:RT=1705262013:S=ALNI_MYH4G1QH6PiS4HkAiki0QquZsipug',
        '__gpi': 'UID=00000cf63f2d1c78:T=1705262013:RT=1705262013:S=ALNI_MaYVX4M8txn-I3ziFNO6H75L6vJgA',
        'FCNEC': '%5B%5B%22AKsRol8wsgl7CfwuQpeKukzdl1H26JqjK2kERg-f6ZfzJ2MNGj59In4SmPd6jGy_4hD-hxFhm__EN2t3H7vF1ihVtKgWHVagUwasxas7HSHbAKif2VIVEFejXGB9Wvs49lACCOrvtTRq9oBACKcaXJt7lTKWtDg2aA%3D%3D%22%5D%5D',
        '_ga_ZSF3D6YSLC': 'GS1.1.1705262011.1.0.1705262059.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.940644881.1705262011; __gads=ID=c85399c900c8de1c:T=1705262013:RT=1705262013:S=ALNI_MYH4G1QH6PiS4HkAiki0QquZsipug; __gpi=UID=00000cf63f2d1c78:T=1705262013:RT=1705262013:S=ALNI_MaYVX4M8txn-I3ziFNO6H75L6vJgA; FCNEC=%5B%5B%22AKsRol8wsgl7CfwuQpeKukzdl1H26JqjK2kERg-f6ZfzJ2MNGj59In4SmPd6jGy_4hD-hxFhm__EN2t3H7vF1ihVtKgWHVagUwasxas7HSHbAKif2VIVEFejXGB9Wvs49lACCOrvtTRq9oBACKcaXJt7lTKWtDg2aA%3D%3D%22%5D%5D; _ga_ZSF3D6YSLC=GS1.1.1705262011.1.0.1705262059.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'ZUJCUlM_',
        # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
    }

    # print("STEP 4: Getting the download link")
    # print("If this step fails, PLEASE read the steps above")
    for i in range(200):
        try:
            response = requests.post('https://ssstik.io/abc', params=params,
                                     # cookies=cookies,
                                     headers=headers,
                                     data=data,
                                     proxies=proxy)
            downloadSoup = BeautifulSoup(response.text, "html.parser")

            downloadLink = downloadSoup.a["href"]
            videoTitle = downloadSoup.p.getText().strip()
            break
        except:
            time.sleep(0.5)

    def sub_thread(downloadLink,id,keyword,link):
        # print("STEP 5: Saving the video :)")

        # Create the 'videos' directory if it doesn't exist
        videos_dir = 'videos'
        os.makedirs(videos_dir, exist_ok=True)

        # Create a subfolder inside 'videos' based on the keyword
        keyword_folder = os.path.join(videos_dir, keyword)
        os.makedirs(keyword_folder, exist_ok=True)

        video_path = os.path.join(keyword_folder, f"{id}-{keyword}.mp4")

        mp4File = urlopen(downloadLink)
        # Feel free to change the download directory
        with open(video_path, "wb") as output:
            while True:
                data = mp4File.read(16384)  # You can experiment with different chunk sizes
                if data:
                    output.write(data)
                else:
                    break
        data = get_data(link)
        if data != None:
            like, comment, share, view = data
        else:
            like, comment, share, view = ["", "", "",""]
        # Save video path and details to CSV
        with open('output.csv', mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Description and Tags', 'Video ID', 'Likes', 'Comments', 'Shares', 'Views',
                          'Video Path',
                          'Keyword']
            writer = csv.writer(csvfile)

            # If the file is empty, write the header
            if os.path.getsize('output.csv') == 0:
                writer.writerow(fieldnames)

            writer.writerow([
                videoTitle,
                id,
                like,
                comment,
                share,
                view,
                video_path,
                keyword,
            ])

    s =  threading.Thread(target=sub_thread,args=(downloadLink,id,keyword,link,))
    s.start()

    # print("STEP 5: Saving the video :)")
    # mp4File = urlopen(downloadLink)
    # # Feel free to change the download directory
    # with open(f"videos/{id}-{keyword}.mp4", "wb") as output:
    #     while True:
    #         data = mp4File.read(4096)
    #         if data:
    #             output.write(data)
    #         else:
    #             break
    # data = get_data(link)
    # if data!=None:
    #     like,comment,share = data
    # else:
    #     like,comment,share = ["","",""]
    # # Save video path and details to CSV
    # with open('output.csv', mode='a', newline='', encoding='utf-8') as csvfile:
    #         fieldnames = ['Description and Tags', 'Video ID', 'Likes', 'Comments', 'Shares', 'Video Path']
    #         writer = csv.writer(csvfile)
    #
    #         # If the file is empty, write the header
    #         if os.path.getsize('output.csv') == 0:
    #             writer.writerow(fieldnames)
    #
    #         writer.writerow([
    #             videoTitle,
    #             id,
    #             like,
    #             comment,
    #             share,
    #             os.getcwd()+f"/videos/{id}-{keyword}.mp4"
    #         ])



def find_stats(data):
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
        r=requests.get(link,headers=headers,proxies=proxy)
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
                # print(json_data)
            except Exception as e:

                continue
            # Find the stats information using the recursive function
            stats_info = find_stats(json_data)
            # Check if "stats" key exists in the dictionary
            if stats_info:
                # Now you can work with the stats_info dictionary
                # print(stats_info)
                return (stats_info['diggCount'],stats_info['commentCount'],stats_info['shareCount'],
                        stats_info['playCount'])

            # if 'stats' in json_data:
            #     stats_data = json_data['stats']
            #
            #     # Now you can work with the stats_data dictionary
            #     digg_count = stats_data.get('diggCount')
            #     share_count = stats_data.get('shareCount')
            #     comment_count = stats_data.get('commentCount')
            #     play_count = stats_data.get('playCount')
            #     collect_count = stats_data.get('collectCount')
            #
            #     # Print or store the extracted statistics
            #     print(f"Digg Count: {digg_count}")
            #     print(f"Share Count: {share_count}")
            #     print(f"Comment Count: {comment_count}")
            #     print(f"Play Count: {play_count}")
            #     print(f"Collect Count: {collect_count}")
            #     break
            # else:
            #     print("No 'stats' key found in the JSON-like data.")
        else:
            pass
        # return None

def start_process(keyword,driver):


    # Change the tiktok link
    driver.get(f"https://www.tiktok.com/search/video?q={keyword}")

    # IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
    # to 60 seconds, just enough time for you to complete the captcha yourself.
    time.sleep(15)

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

        # elif (screen_height) * i > scroll_height:
        #     break
        # if i>15:
        #     break

        # this class may change, so make sure to inspect the page and find the correct class
    # className = "tiktok-1s72ajp-DivWrapper"
    urlsToDownload=urlsToDownload[:100]
    count=0
    print(urlsToDownload)
    print(f"Scraped {len(urlsToDownload)} video Links")
    threads = []
    for index, url in enumerate(urlsToDownload):

        # print(f"Downloading video: {index}")
        try:
            # downloadVideo(url, index,keyword)
            s=threading.Thread(target=downloadVideo,args=(url, index,keyword,))
            threads.append(s)
        except Exception as e:
            # print(f"An exception occurred: {e}")
            # traceback.print_exc()
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

def main(csv_file_path):
    # Reading the CSV file
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        print("STEP 1: Open Chrome browser")

        options = uc.ChromeOptions()
        # setting profile
        options.user_data_dir = os.getcwd() + "/profile"
        # options.add_argument("--headless")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = uc.Chrome(options=options,)

        # Iterating through each row
        for row in csv_reader:
            # Assuming each row contains a single value
            keyword = row[0]

            # Start Process
            print(f"Downloading Video for keyword {keyword}")
            start_process(keyword,driver)

if __name__ == '__main__':
    main(input_file)
