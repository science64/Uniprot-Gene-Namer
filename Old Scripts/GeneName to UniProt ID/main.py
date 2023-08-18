import requests
import pandas as pd
import time


def main():

    name = input('Please enter name of the excel file: ')
    #name = 'input'
    Data = pd.read_excel(name + ".xlsx", header=0)

    try:
        geneSymbols = list(Data['Gene Symbol'])
    except:
        geneSymbols = list(Data['Gene Name'])

    j = 0

    for geneSymbol in geneSymbols:
        #print(geneSymbol)

        url = 'https://www.uniprot.org/uploadlists/'

        params = {
            'from': 'GENENAME',
            'to': 'ACC',
            'format': 'tab',
            'query': geneSymbol,
            "taxon": "Homo sapiens(Human)[9606]",
            "reviewed": "yes"
        }

        # data = urllib.parse.urlencode(params)
        # data = data.encode('utf-8')
        # req = urllib.request.Request(url, data)
        # with urllib.request.urlopen(req) as f:
        #     response = f.read()
        # print(response.decode('utf-8'))
        try:
            req = requests.post(url, data=params)
            #print(req.text)
            accession = (req.text.split('	')[2].split('\n')[0].strip())
        except:
            accession = ''

        print(f'{geneSymbol} : {accession}')
        Data.loc[j, 'Accession'] = accession
        j+=1

    Data.to_excel(name + '_Added.xlsx')






if __name__ == '__main__':
    main()