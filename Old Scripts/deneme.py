import uniprot
import pandas as pd
import requests

#https://www.ebi.ac.uk/proteins/api/doc/#!/proteins/getByAccession

def main():
    columns = ["Accession", "Gene Symbol"]

    out_df = pd.DataFrame(columns=columns)

    name = input('Please enter name of the excel file: ')
    Data = pd.read_excel(name + ".xlsx", header=0)

    try:
        accession = list(Data['Master Protein Accessions'])
    except:
        accession = list(Data['Accession'])

    geneNameFromDatabaseList = list(Data['Gene Symbol'])

    j = 0

    finalList = []

    for i in accession:
        if ';'in i:
            final = i.split(';')[0]
        elif ' ' in i:
            final = i.split(' ')[0]
        else:
            final = i

        print(finalList)

        if final not in finalList:

            finalList.append(final)


            geneSymbol = geneNameFromDatabaseList[j]


            #print(f'{final} : {geneSymbol}')

            cache = {'Accession': final,
                    'Gene Symbol': geneSymbol}

            out_df = out_df.append(cache, ignore_index=True)

        j+=1

    out_df.to_excel(name + '_NameAdded.xlsx')


if __name__ == '__main__':
    uniprotID = 'P48730'

    main()
