import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

def main(name):

    database = pd.read_excel('./uniprot_database_build_FASTA/Homo Sapiens Gene Symbol Database Uniprot Verified.xlsx')
    databaseAccession = list(database['Accession'])
    databaseGeneName = list(database['Gene Symbol'])


    data = pd.read_excel(name + ".xlsx", header=0)

    try:
        accession = list(data['Master Protein Accessions'])
    except:
        accession = list(data['Accession'])

    geneNameExist = list(data['Gene Symbol'])

    j = 0
    for i in accession:
        if ';'in i:
            final = i.split(';')[0]
        elif ' ' in i:
            final = i.split(' ')[0]
        else:
            final = i

        if str(geneNameExist[j]) == 'nan':
            status = False
            for s in databaseAccession:
                if accession == s:
                    index = databaseAccession.index(s)
                    geneSymbol = databaseGeneName[index]
                    status = True
                    break

            if status == False:
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
        else:
            geneSymbol = str(geneNameExist[j])

        print(f'{i} : {geneSymbol}')

        data.loc[j, 'Gene Symbol'] = geneSymbol
        #data.loc[j, 'Gene Symbol_2'] = geneSymbol
        j+=1

    data.to_excel(name + '.xlsx')


if __name__ == '__main__':

    while(True):
        name = input('Please enter name of the excel file: ')
        main(name)