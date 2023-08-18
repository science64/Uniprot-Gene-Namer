import pandas as pd

def main():
    name = '20201030_MAA_JG_CSNK1D_PhosphoSites_Tryp_Proteins'
    Data = pd.read_excel(name + ".xlsx", header=0)

    description = list(Data['Description'])
    j = 0

    for i in description:
        try:
            geneSymbol = i.split('GN=')[1].split(' ')[0]
            print(geneSymbol)
        except:
            geneSymbol = i.split('-')[0]
            print(geneSymbol)

        Data.loc[j, 'Gene Symbol'] = geneSymbol
        j+=1

    Data.to_excel(name + '_NameAdded.xlsx')

if __name__ == '__main__':
    main()
