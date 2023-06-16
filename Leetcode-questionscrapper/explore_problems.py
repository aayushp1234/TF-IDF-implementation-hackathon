import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

# Create a new instance of the ChromeDriver service with the path to the ChromeDriver executable
chrome_driver_path = ChromeDriverManager().install()
service = Service(chrome_driver_path)

# Start the service
service.start()

# Pass the service object when creating the ChromeDriver instance
driver = webdriver.Chrome(service=service)

heading_class = ".mr-2.text-label-1"
body_class = ".px-5.pt-4"
index = 524
QDATA_FOLDER = "Qdata"


def add_text_to_index_file(text):
    index_file_path = os.path.join(QDATA_FOLDER, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + '\n')


def add_link_to_Qindex_file(text):
    index_file_path = os.path.join(QDATA_FOLDER, "Qindex.txt")
    with open(index_file_path, "a") as Qindex_file:
        Qindex_file.write(text + '\n')


def create_and_add_text_to_file(file_name,text):
    folder_path=os.path.join(QDATA_FOLDER,file_name)
    os.makedirs(folder_path,exist_ok=True)
    file_path=os.path.join(folder_path,file_name+".txt")
    with open (file_path,"w") as new_file:
        new_file.write(text)


def get_array_of_links():
    arr = []
    with open("lc_problems.txt", "r") as f:
        for line in f:
            arr.append(line.strip())
    return arr


def getPageData(url, index):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, body_class)))
        time.sleep(1)
        heading = driver.find_element(By.CSS_SELECTOR, heading_class)
        body = driver.find_element(By.CSS_SELECTOR, body_class)
        print(heading.text)
        if heading.text:
            add_text_to_index_file(heading.text)
            add_link_to_Qindex_file(url)
            create_and_add_text_to_file(str(index), body.text)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False


arr = get_array_of_links()
for i in range(964, len(arr)):
    success = getPageData(arr[i], index)
    if success:
        index = index + 1

driver.quit()
