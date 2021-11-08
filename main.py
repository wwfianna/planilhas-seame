import pandas as pd
import csv
from pathlib import Path


def get_file_number(files):
    print("Planilhas na disponíveis:")
    for i in range(0, len(files)):
        print(i, files[i])

    try:
        return int(input("Digite o número do arquivo de origem (-1 para sair): "))
    except(ValueError):
        print("Entrada inválida!")
        return -1


def select_files():
    data_sheet = ""
    sheet_path = Path("data/admin_loja/").glob('**/*.CSV')
    for path in sheet_path:
        data_sheet = str(path)
        print("Dataset do admin loja:", data_sheet)

    filepath = Path("data/").glob('*.csv')
    files = []
    for path in filepath:
        files.append(str(path))

    file_num = get_file_number(files)
    while file_num != - 1:
        df1 = pd.read_csv(files[file_num], delimiter=";", encoding="ISO-8859-1")
        df2 = pd.read_csv(data_sheet, delimiter=";", encoding="ISO-8859-1")

        df1['TID'] = df1['TID'].apply(lambda x: str(x))
        df2['TID'] = df2['TID'].apply(lambda x: str(x))

        df1 = df1[df1['TID'].apply(lambda x: False if len(x) < 20 else True)]
        df2 = df2[df2['TID'].apply(lambda x: False if len(x) < 20 else True)]

        pedido_nf = []
        lastTID = ""
        for linha_df2 in df2.values:
            if linha_df2[10] != lastTID:
                for linha_df1 in df1.values:
                    if linha_df2[10] == linha_df1[6]:
                        lastTID = linha_df2[10]
                        linha = [item for item in linha_df1[:15]]
                        linha.append(linha_df2[17])
                        linha.append(4)
                        linha.append(linha_df2[16])
                        linha.append(linha_df2[15])
                        linha.append(linha_df2[14])
                        linha.append("")
                        linha.append(linha_df2[18])
                        linha.append(linha_df2[0])
                        linha.append(linha_df2[9])
                        linha.append("")
                        pedido_nf.append(linha)
                        print("Incluindo linha:", linha)
                        break

        filename = files[file_num].split('/')[-1]
        with open('output/' + filename, mode='w', encoding='ISO-8859-1', newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=';')
            writer.writerow(df1.columns)
            for row in pedido_nf:
                writer.writerow(row)
        print("Gerada a planilha em output/" + filename)

        print("\n\n")
        file_num = get_file_number(files)


select_files()
