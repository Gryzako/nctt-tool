import customtkinter
from actions import Actions 

customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('dark-blue')

class App(customtkinter.CTk):
    def __init__(self,):
        super().__init__()

        #variable
        self.ListOfTransaction = []
        self.columns = ['Time, ', 'Batch, ', 'TID, ', 'STAN, ', 'Amount, ', 'Authorization number']
        self.POSDMtransaction = []
        self.ADBtransactions = []

        #Cofigure window
        self.geometry('400x300')
        #self.resizable(False, False)
        self.title('NCTT tool')

        #Tabs config

        self.tabView = customtkinter.CTkTabview(self, width=400, height=300)
        self.tabView.grid(row=0, column=0)
        self.tabView.add("NIPC_SAP")
        self.tabView.add("TVersion")
        self.tabView.add("POSDMvsADB")
        self.tabView.tab("NIPC_SAP").grid_columnconfigure(1, weight=1)
        self.tabView.tab("NIPC_SAP").grid_rowconfigure(1, weight=1)
        self.tabView.tab("TVersion").grid_rowconfigure(0, weight=1)
        self.tabView.tab("TVersion").grid_columnconfigure(0, weight=1)
        self.tabView.tab("POSDMvsADB").grid_rowconfigure(2, weight=1)
        self.tabView.tab("POSDMvsADB").grid_columnconfigure(2, weight=1)

        #Widgets NIPC_SAP
        self.LabelStatusName = customtkinter.CTkLabel(self.tabView.tab("NIPC_SAP"), text="File status:", font=('Fixedsys', 12, 'bold'))
        self.LabelStatusName.grid(row=0, column=0, sticky="nsew")
        self.LabelStatusResult = customtkinter.CTkLabel(self.tabView.tab("NIPC_SAP"), text='  File not loaded', font=('Fixedsys', 12, 'bold'))
        self.LabelStatusResult.grid(row=0, column=1, sticky="nsew")

        self.ButtonLoad = customtkinter.CTkButton(self.tabView.tab("NIPC_SAP"), text="Load file", command=self.LoadFileAction)
        self.ButtonLoad.grid(row=1, column=0, padx = 5, sticky="nsew")

        self.buttonSaveResults = customtkinter.CTkButton(self.tabView.tab("NIPC_SAP"), text='Save as TXT', state=customtkinter.DISABLED, command=self.SaveButtonAction)
        self.buttonSaveResults.grid(row=1, column=1, padx = 5, sticky="nsew")


        #Widgets Transaction version
        self.TversionLabel = customtkinter.CTkLabel(self.tabView.tab("TVersion"), text='This program is using connected device report \n and checking whether site has the same terminal version \n on all devices')
        self.TversionLabel.grid(row=0, column=0, sticky="nsew")

        self.LoadButton = customtkinter.CTkButton(self.tabView.tab("TVersion"), text='Load', command=self.LoadTVersion, width=380)
        self.LoadButton.grid(row=1, column=0)

        self.Textbox = customtkinter.CTkTextbox(self.tabView.tab("TVersion"), height=150, width=380)
        self.Textbox.grid(row=2, column=0, padx = 5, pady = 5)

        #Widgets POSDMvsADB
        self.LoadPOSDMbutton = customtkinter.CTkButton(self.tabView.tab("POSDMvsADB"), text='Load POSDM', command=self.LoadPOSDMbuttonAction)
        self.LoadPOSDMbutton.grid(row=0, column=0, padx = 5, pady = 5)
        self.LoadPOSDMlabel = customtkinter.CTkLabel(self.tabView.tab("POSDMvsADB"), text="not loaded")
        self.LoadPOSDMlabel.grid(row=0, column=1)

        self.LoadADBButton = customtkinter.CTkButton(self.tabView.tab("POSDMvsADB"), text='Load ADB', command=self.LoadADBButtonAction)
        self.LoadADBButton.grid(row=1, column=0, padx = 5, pady = 5)
        self.LoadADBlabel = customtkinter.CTkLabel(self.tabView.tab("POSDMvsADB"), text="not loaded")
        self.LoadADBlabel.grid(row=1, column=1)

        self.ActionButton = customtkinter.CTkButton(self.tabView.tab("POSDMvsADB"), text="Action", command=self.POSDMvsADBaction)
        self.ActionButton.grid(row=2, column=0, padx = 5, pady = 5)

        self.TextboxPOSDMvsADB = customtkinter.CTkTextbox(self.tabView.tab("POSDMvsADB"), width=380, height=130)
        self.TextboxPOSDMvsADB.grid(row=3, column=0, padx = 5, pady = 5, columnspan=2)

    def LoadFileAction(self):
        self.ListOfTransaction = []
        self.ListOfTransaction.append(Actions.LoadButton(self))
        self.LabelStatusResult.configure(text='File has been loaded!')
        self.buttonSaveResults.configure(state=customtkinter.ACTIVE)

    def SaveButtonAction(self):
        Actions.SaveButton(self, self.ListOfTransaction, self.columns)

    def LoadTVersion(self):
        differentV = Actions.LoadTversionFile(self)
        self.Textbox.insert('0.0', f'List of the sites which have various software version on terminals: {str(differentV)}')
    
    def LoadPOSDMbuttonAction(self):
        columnName = 'Tender Value'
        self.POSDMtransaction = Actions.LoadPOSDM(self, columnName)
        self.LoadPOSDMlabel.configure(text='Transaction loaded!')
    
    def LoadADBButtonAction(self):
        columnName = 'Final amount'
        self.ADBtransactions = Actions.LoadPOSDM(self, columnName)
        self.LoadADBlabel.configure(text='Transaction loaded!')

    def POSDMvsADBaction(self):
        diff1, diff2, lenPOSDM, lenADB = Actions.ComparisionOfTransaction(self, self.POSDMtransaction, self.ADBtransactions)
        self.TextboxPOSDMvsADB.insert('0.0', f"Raport POSDM zawiera {lenPOSDM} transakcje. Zawiera on następujące transakcje: {diff2} których nie ma raport ADB \n" )
        self.TextboxPOSDMvsADB.insert('0.0', f"Raport ADB zawiera {lenADB} transakcje. Zawiera on następujące transakcje: {diff1} których nie ma raport POSDM \n")

if __name__ == "__main__":
    app = App()
    app.mainloop()