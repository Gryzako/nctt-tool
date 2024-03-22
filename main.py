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

        #Cofigure window
        self.geometry('400x300')
        self.resizable(False, False)
        self.title('NCTT tool')

        #Tabs config

        self.tabView = customtkinter.CTkTabview(self, width=400, height=300)
        self.tabView.grid(row=0, column=0)
        self.tabView.add("NIPC_SAP")
        self.tabView.add("TVersion")
        self.tabView.tab("NIPC_SAP").grid_columnconfigure(1, weight=1)
        self.tabView.tab("NIPC_SAP").grid_rowconfigure(1, weight=1)
        self.tabView.tab("TVersion").grid_rowconfigure(0, weight=1)
        self.tabView.tab("TVersion").grid_columnconfigure(0, weight=1)


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

        self.LoadButton = customtkinter.CTkButton(self.tabView.tab("TVersion"), text='Load', command=self.LoadTVersion)
        self.LoadButton.grid(row=1, column=0, sticky="nsew")

        self.Textbox = customtkinter.CTkTextbox(self.tabView.tab("TVersion"))
        self.Textbox.grid(row=2, column=0, sticky="nsew")

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

if __name__ == "__main__":
    app = App()
    app.mainloop()