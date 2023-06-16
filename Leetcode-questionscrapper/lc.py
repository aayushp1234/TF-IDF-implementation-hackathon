# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import bs4 as BeautifulSoup

# s=Service('chromedriver.exe')

# driver=webdriver.Chrome(service=s)

# page_URL="https://leetcode.com/problemset/all/?page="

# def get_a_tages(url):
#     driver.get(url)
#     time.sleep(7)
#     links = driver.find_elements(By.TAG_NAME, "a")
#     # print(links)
#     ans=[]
#     pattern="/problems"
#     for i in links:
#         try:
#            if pattern in i.get_attribute("href"):
#                 ans.append(i.get_attribute("href")) 
#         except:
#            pass
#     print(ans)
#     input("Press any key to exit")
# get_a_tages("https://leetcode.com/problemset/all/?page=1")
# time.sleep(5)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

def get_a_tags(url):
    driver.get(url)
    time.sleep(7)
    links = driver.find_elements(By.TAG_NAME, "a")
    ans = []
    pattern = "/problems"
    for i in links:
        try:
            if pattern in i.get_attribute("href"):
                ans.append(i.get_attribute("href"))
        except:
            pass
    ans=list(set(ans))
    return ans
page_URL="https://leetcode.com/problemset/all/?page="
get_a_tags("https://leetcode.com/problemset/all/?page=1")
time.sleep(5)
my_ans=[]
for i in range(1,55):
    my_ans+=(get_a_tags(page_URL +str(i)))

my_ans=list(set(my_ans))

with open('lc.txt','a') as f:
          for j in my_ans:
               f.write(j+'\n')

print(len(my_ans))
driver.quit()
# Keep the live server window open until user interaction
# input("Press any key to exit...")

