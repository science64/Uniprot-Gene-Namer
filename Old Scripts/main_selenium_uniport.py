from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("disable-extensions")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("test-type")
chrome_options.add_argument("ignore-certificate-errors")



name = input('Please enter name of the excel file: ')
Data = pd.read_excel(name + ".xlsx", header=0)

try:
    accession = list(Data['Master Protein Accessions'])
except:
    accession = list(Data['Accession'])
j = 0

geneNameFromDatabaseList = list(Data['Gene Symbol'])

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.set_page_load_timeout(30)

for i in accession:

    if ';' in i:
        geneID = i.split(';')[0]
    elif ' ' in i:
        geneID = i.split(' ')[0]
    else:
        geneID = i


    geneNamefromDatabase = geneNameFromDatabaseList[j]

    driver.get(f'https://www.uniprot.org/uniprot/{geneID}')

    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content-gene"]/h2')))
    geneName = driver.find_element_by_xpath('//*[@id="content-gene"]/h2').text

    print(geneName)

    if geneNamefromDatabase != geneName:
        print(f'{geneID}:{geneNamefromDatabase}:{geneName}')

    j+=1

driver.close()