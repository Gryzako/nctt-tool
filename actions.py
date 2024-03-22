import customtkinter as ct
import pandas as pd
import numpy as np


class Actions():
    def __init__(self):
        #Variables
        pass
        

    def LoadButton(self):
        ListOfTransaction = []
        try:
            filepath = ct.filedialog.askopenfilename(initialdir='c:\\', title="find NIPC_SAP file")
            with open(filepath) as file:
                for line in file:
                    if line.startswith('3000'):
                        AmountOfTransaction = line[145:151]
                        DeviceNumber = line[55:63]
                        StanNumber = line[65:69]
                        Hour = line[69:71]
                        Minutes = line[71:73]
                        Seconds = line[73:75]
                        Year = line[75:79]
                        Month = line[79:81]
                        Day = line[81:83]
                        AuthCode = line[119:125]
                        BatchNo = line[19:22]
                        ListOfTransaction.append(f'{Year}.{Month}.{Day} {Hour}:{Minutes}:{Seconds}, {BatchNo}, {DeviceNumber}, {StanNumber}, {AmountOfTransaction}, {AuthCode}')
            return ListOfTransaction
        except Exception as e:
            print(e)


    def SaveButton(self, listoftrx, columns):
        try:
            FilesType = [("Excel files", "*.xlsx"), ("Text files", "*.txt"), ("All files", "*.*")]
            file = ct.filedialog.asksaveasfile(mode='w', defaultextension=".xlsx", filetypes=FilesType)
            if file is None:
                return
            filename = file.name
            file.close()

            if filename.endswith('.xlsx'):
                new_list = []
                for i in listoftrx[0]:
                    array = i.split(',')
                    new_list.append(array)
                df = pd.DataFrame(new_list, columns=columns)
                df.to_excel(filename, index=False)
            elif filename.endswith('.txt'):
                with open(filename, 'w') as f:
                    f.write(f'{"".join(columns)}\n')
                    for i in listoftrx:
                        f.write('\n'.join(i))
            else:
                print("Unsupported file format. Please choose either .xlsx or .txt.")
        except Exception as e:
            print(e)

    #Tversion
            
    def LoadTversionFile(self):
        file = ct.filedialog.askopenfilename(initialdir='c:\\', title="find terminal connected report")
        try:
            df = pd.read_excel(file)
            df['software_version'] = df['software_version'].replace('', np.nan)
            same_version = []
            different_version = []
            for site, site_data in df.groupby('site_id'):
                uniqie_tversion = site_data['software_version'].dropna().unique()
                if len(uniqie_tversion) <= 1:
                    same_version.append(site)
                else:
                    different_version.append(site)
            return different_version
        
        except Exception as e:
            print(e)


