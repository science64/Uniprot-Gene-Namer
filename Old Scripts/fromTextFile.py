import requests

accession = open('./text file/MG132 Increase.txt').readlines()

for final in accession:
    if '\n' in final:
        final = final[:-1]
    #print(final)
    url = f'https://www.ebi.ac.uk/proteins/api/proteins/{final}'
    req = requests.get(url)
    result = req.json()
    geneSymbol = result['gene'][0]['name']['value']
    print(final+'\t'+geneSymbol)