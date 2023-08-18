import requests
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
#https://www.ebi.ac.uk/proteins/api/doc/#!/proteins/getByAccession

def main():

    database = pd.read_excel("database.xlsx", header=0)
    accessionDatabase = list(database['Accession'])
    geneNameDatabase = list(database['Gene Symbol'])

    name = input('Please enter name of the excel file: ')
    Data = pd.read_excel(name + ".xlsx", header=0)

    try:
        accession = list(Data['Master Protein Accessions'])
    except:
        accession = list(Data['Accession'])
    j = 0

    for i in accession:
        if ';'in i:
            final = i.split(';')[0]
        elif ' ' in i:
            final = i.split(' ')[0]
        else:
            final = i

        if final in accessionDatabase:
            index = accessionDatabase.index(final)
            geneSymbol = geneNameDatabase[index]

        else:
            try:
                url = f'https://www.ebi.ac.uk/proteins/api/proteins/{final}'
                req = requests.get(url)
                result = req.json()
                geneSymbol = result['gene'][0]['name']['value']
            except:
                try:
                    driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
                    driver.set_page_load_timeout(30)
                    driver.get(f'https://www.uniprot.org/uniprot/{final}')

                    wait = WebDriverWait(driver, 15)
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content-gene"]/h2')))
                    geneSymbol = driver.find_element_by_xpath('//*[@id="content-gene"]/h2').text
                    driver.close()
                except:
                    geneSymbol = ''

        print(f'{i} : {geneSymbol}')
        Data.loc[j, 'Gene Symbol'] = geneSymbol
        j+=1

    Data.to_excel(name + '_NameAdded.xlsx')






if __name__ == '__main__':
    uniprotID = 'P48730'

    main()
