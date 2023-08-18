import pandas as pd

data = open('uniprot_sprot.fasta').readlines()

columns = ["Species", "Accession", "Description", "Gene Name Long", "Gene Symbol"]
out_df = pd.DataFrame(columns=columns)
out_df2 = pd.DataFrame(columns=columns)

for line in data:

    if 'OS=Homo sapiens' in line:
        species = 'Homo sapiens'
        accessionID = line.split('|')[1]
        details = line.split('|')[2].split(' OS=')[0]
        GeneNameLong = line.split('|')[2].split(' ')[0]
        try:
            GeneName = line.split('GN=')[1].split(' ')[0]
        except:
            GeneName = GeneNameLong.split('_')[0]

        cache = {
            "Species": species,
            "Accession": accessionID,
            "Description": details,
            "Gene Name Long": GeneNameLong,
            "Gene Symbol": GeneName
        }

        out_df = out_df.append(cache, ignore_index=True)

    elif 'OS=Mus musculus' in line:
        species = 'Mus musculus'
        accessionID = line.split('|')[1]
        details = line.split('|')[2].split(' OS=')[0]
        GeneNameLong = line.split('|')[2].split(' ')[0]

        try:
            GeneName = line.split('GN=')[1].split(' ')[0]
        except:
            GeneName = GeneNameLong.split('_')[0]

        cache2 = {
            "Species": species,
            "Accession": accessionID,
            "Description": details,
            "Gene Name Long": GeneNameLong,
            "Gene Symbol": GeneName
        }

        out_df2 = out_df2.append(cache2, ignore_index=True)

out_df.to_excel('Homo Sapiens Gene Symbol Database Uniprot Verified.xlsx')
out_df2.to_excel('Mus musculus Gene Symbol Database Uniprot Verified.xlsx')

print('Finished!')