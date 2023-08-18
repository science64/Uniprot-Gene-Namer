import requests
import pandas as pd

database = pd.read_excel('../uniprot_database_build_FASTA/Homo Sapiens Gene Symbol Database Uniprot Verified.xlsx')
databaseAccession = list(database['Accession'])
databaseGeneName = list(database['Gene Symbol'])

input = pd.read_excel('input.xlsx')

geneName = list(input['Gene Symbol'])

geneNameList = []

columns = ["Accession", "Gene Symbol"]

out_df = pd.DataFrame(columns=columns)


for name in geneName:
    if name not in geneNameList:
        geneNameList.append(name)
        #print(name)
        status = False
        for s in databaseGeneName:
            if name in s:
                index = databaseGeneName.index(s)
                accession = databaseAccession[index]
                status = True
                break
        if status == False:
            accession = ''

        print(name, accession)

        cache = {'Accession': accession,
                 'Gene Symbol': name}

        out_df = out_df.append(cache, ignore_index=True)

out_df.to_excel('output.xlsx')
# print(geneNameList)
# print(len(geneNameList))