import requests
import time
import pandas as pd
columns = ["Accession", "Gene Symbol", "Status"]
out_df = pd.DataFrame(columns=columns)

database = pd.read_excel("Uniprot_database_2021.xlsx", header=0)
accessionDatabase = list(database['Accession'])

for i in accessionDatabase:
    if ';' in i:
        final = i.split(';')[0]
    elif ' ' in i:
        final = i.split(' ')[0]
    else:
        final = i

    # url = f'https://www.ebi.ac.uk/proteins/api/proteins/{final}'
    # req = requests.get(url)
    # result = req.json()
    # geneSymbol = result['gene'][0]['name']['value']

    url = f'https://www.uniprot.org/uniprot/{final}'

    while(True):
        try:
            req = requests.get(url)
            geneSymbol = req.text.split('<title>')[1].split(' ')[0]
            status = req.text.split('href="/manual/entry_status"><span>')[1].split('</')[0]
            break
        except:
            pass

    print(i, geneSymbol, status)

    cache = {
        "Accession": i,
        "Gene Symbol": geneSymbol,
        "Status": status
    }
    out_df = out_df.append(cache, ignore_index=True)

out_df.to_excel('Uniprot_database_2021_Status.xlsx')
