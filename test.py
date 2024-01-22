from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

import os

# Define Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run Chrome in headless mode
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu') # Disable GPU acceleration

# Set the display environment variable
os.environ['DISPLAY'] = ':99'
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH")

# Initialize the WebDriver with Chrome options
driver = uc.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://github.com")
driver.close()
print("done")

# Sample CSV data
# csv_fieldnames = ['Description and Tags', 'Video ID', 'Likes', 'Comments', 'Shares', 'Views',
# #                   'Video Path', 'Keyword']
# # csv_row_data = [['Oud E Awal , the woody blend for winter , enjoy with Dubai Damas #attar #oud #trending #tariqjameel #oudhindi ', 1, 175, 5, 3, 2730, 'videos\\Ylang-Ylang Essential Oil\\1-Ylang-Ylang Essential Oil.mp4', 'Ylang-Ylang Essential Oil'], ['Olive Oil Health Benefits  #ayorved #herbs #foryoupage #fyp #healthtips #Nadiahealthandbeauty #oliveoil ', 0, 7, 4, 1, 1610, 'videos\\Ylang-Ylang Essential Oil\\0-Ylang-Ylang Essential Oil.mp4', 'Ylang-Ylang Essential Oil'], ['Lavender pure oil for dry skin and best fragrance very cheap price #imperial #cosmetics ', 2, 226, 7, 20, 9598, 'videos\\Ylang-Ylang Essential Oil\\2-Ylang-Ylang Essential Oil.mp4', 'Ylang-Ylang Essential Oil']]
# #
# #
# # csv_content = ""
# # temp = []
# # for data in csv_row_data:
# #     print(data)
# #     temp.append(",".join(data))
# # csv_content+="\n".join(temp)
# # del temp
# # print(csv_content)
# Assuming csv_data is a list of lists
# csv_data = [
#     ['value1', 'value2', 'value3'],
#     ['value4', 'value5', 'value6'],
#     ['value1', 'value2', 'value3'],  # Duplicate
#     ['value7', 'value8', 'value9'],
# ]
#
# # Convert inner lists to tuples before using set()
# csv_data = set(tuple(row) for row in csv_data)
# csv_data = list(list(row) for row in csv_data)
#
# # Now csv_data contains unique rows as tuples
# print(csv_data)