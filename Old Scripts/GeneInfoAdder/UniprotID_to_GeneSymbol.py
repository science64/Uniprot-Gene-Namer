import requests
import pandas as pd

def main():
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

        try:
            url = f'https://www.ebi.ac.uk/proteins/api/proteins/{final}'
            req = requests.get(url)
            result = req.json()
            geneSymbol = result['gene'][0]['name']['value']
        except:
            geneSymbol = ''

        print(f'{i} : {geneSymbol}')
        Data.loc[j, 'Gene Symbol'] = geneSymbol
        j+=1

    Data.to_excel(name + '_NameAdded.xlsx')

if __name__ == '__main__':
    main()