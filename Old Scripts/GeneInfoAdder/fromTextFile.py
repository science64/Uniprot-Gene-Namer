import requests
import time

# accession = open('./text file/MG132 Increase.txt').readlines()
# accessionDatabase = open('./text file/accession').readlines()
# nonList = []
# for final in accession:
#     if '\n' in final:
#         final = final[:-1]
#     #print(final)
#     for j in range(0, len(accessionDatabase)):
#         if '\n' in accessionDatabase[j]:
#             databaseAccession = accessionDatabase[j][:-1].split(':')[0]
#         if databaseAccession == final:
#             print(final, accessionDatabase[j][:-1].split(':')[1])
#         else:
#             if final not in nonList:
#                 nonList.append(final)
#
# print(nonList)

accession = open('./text file/MG132 Decrease.txt').readlines()
#accessionDatabase = open('./text file/accession').readlines()
nonList = []
for final in accession:
    if '\n' in final:
        final = final[:-1]
    #print(final)
    url = f'https://www.ebi.ac.uk/proteins/api/proteins/{final}'
    req = requests.get(url)
    result = req.json()

    geneSymbol = result['gene'][0]['name']['value']

    geneFeatures = result['features'][0]['description']
    try:
        comments = result['comments'][0]['text'][0]['value']
    except:
        try:
            comments = result['comments'][1]['text'][0]['value']
        except:
            comments = 'Function less known'
    # print(comments)
    # print(geneFeatures)
    print(final + '\t' + geneSymbol + '\t' + geneFeatures + '\t' + comments )