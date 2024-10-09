import requests

def GeneNameEngine(Data, database):
    # name = input('Please enter name of the excel file: ')
    # Data = pd.read_excel(name + ".xlsx", header=0)

    #database = pd.read_excel("Uniprot_database_2021.xlsx", header=0)
    accessionDatabase = list(database['Accession'])
    geneNameDatabase = list(database['Gene Symbol'])

    try:
        accession = list(Data['Master Protein Accessions'])
    except:
        accession = list(Data['Accession'])
    j = 0

    for i in accession:
        if ';' in i:
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
                geneSymbol = ''

        print(f'{i} : {geneSymbol}')
        Data.loc[j, 'Gene Symbol'] = geneSymbol
        j += 1

    #Data.to_excel(name + '.xlsx')
    return Data
