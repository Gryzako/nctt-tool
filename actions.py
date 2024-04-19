from customtkinter import filedialog
from pandas import DataFrame, read_excel, read_csv
from numpy import nan
import os
import time

class Actions():
    def __init__(self):
        #Variables
        pass
    
    def LoadButton(self):
        try:
            filepath = filedialog.askopenfilename(initialdir='c:\\', title="find NIPC_SAP file")
            action_instance = Actions()
            return action_instance.sortList(filepath)
        except Exception as e:
            print(e)
    
    def OpenFolder(self, columns):
        folder_path = filedialog.askdirectory()
        files = os.listdir(folder_path)
        for file in files:
            try:
                action_instance = Actions()
                listOfTrx = []
                listOfTrx.append(action_instance.sortList(os.path.join(folder_path, file)))
                action_instance.saveAsExcel(listOfTrx, columns, f'{file}.xlsx')
            except Exception as e:
                print(e)
            time.sleep(1)

    def SaveButton(self, listoftrx, columns):
        try:
            FilesType = [("Excel files", "*.xlsx"), ("Text files", "*.txt"), ("All files", "*.*")]
            file = filedialog.asksaveasfile(mode='w', defaultextension=".xlsx", filetypes=FilesType)
            if file is None:
                return
            filename = file.name
            file.close()

            action_istance = Actions()

            if filename.endswith('.xlsx'):
                action_istance.saveAsExcel(listoftrx, columns, filename)
            elif filename.endswith('.txt'):
                action_istance.saveAsTxt(listoftrx, columns, filename)
            else:
                print("Unsupported file format. Please choose either .xlsx or .txt.")
        except Exception as e:
            print(e)

    def saveAsExcel(self, list, columns, name):
        new_list = []
        for i in list[0]:
            array = i.split(',')
            new_list.append(array)
        df = DataFrame(new_list, columns=columns)
        comma = lambda val: '{:0.2f}'.format(float(val.lstrip('0')) / 100)
        df['Amount, '] = df['Amount, '].apply(comma)
        df.to_excel(name, index=False)

    def saveAsTxt(self, list, column, name):
        with open(name, 'w') as f:
            f.write(f'{"".join(column)}\n')
            for i in list:
                f.write('\n'.join(i))

    def sortList(self, file):
        sortedList = []
        with open(file) as f:
            for line in f:
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
                    sortedList.append(f'{Year}.{Month}.{Day} {Hour}:{Minutes}:{Seconds}, {BatchNo}, {DeviceNumber}, {StanNumber}, {AmountOfTransaction}, {AuthCode}')
        return sortedList
    
    #Tversion
            
    def LoadTversionFile(self):
        file = filedialog.askopenfilename(initialdir='c:\\', title="find terminal connected report")
        try:
            df = read_excel(file)
            df['software_version'] = df['software_version'].replace('', nan)
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


    def LoadPOSDM(self, column) -> list:
        file = filedialog.askopenfilename(initialdir='c:\\', title="Find POSDM report")
        transactions = []
        try:
            if file.lower().endswith('.xlsx'):
                df = read_excel(file)
            elif file.lower().endswith('.csv'):
                df = read_csv(file, delimiter=";")
            else:
                raise ValueError("Unsupported file format. Please provide a .xlsx or .csv file.")
            if column not in df.columns:
                raise ValueError("Specified column not found in the file.")
            transactions = df[column].tolist()
        except Exception as e:
            print(f"An error occurred: {e}")
        return transactions
    
    def ComparisionOfTransaction(self, reportOne, reportTwo):
        count_a = {}
        count_b = {}

        for amount in reportOne:
            count_a[amount] = count_a.get(amount, 0) +1

        for amount in reportTwo:
            count_b[amount] = count_b.get(amount, 0) +1

        missing_in_b = [amount for amount in count_a if amount not in count_b or count_a[amount] > count_b[amount]]
        missing_in_a = [amount for amount in count_b if amount not in count_a or count_b[amount] > count_a[amount]]

        return missing_in_a, missing_in_b, len(reportOne), len(reportTwo)


    






