__author__ = "Süleyman Bozkurt"
__version__ = "v3.1"
__maintainer__ = "Süleyman Bozkurt"
__email__ = "sbozkurt.mbg@gmail.com"
__date__ = '18.01.2022'
__update__ = '09.10.2024'

import pandas as pd
from threading import Thread
from tkinter import *
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from functions import *

class MyWindow():
    def __init__(self, parent):

        self.frame = Frame(parent, width=840, height=480)
        self.font = Font(family="Times New Roman", size=16)
        self.request_timeout = 30
        global root
        root=parent
        Label(self.frame, text="Select Protein file!", fg='#ffe7b6', bg='#b97455', font=self.font).place(x=220, y=15)

        self.fontRadio = Font(family="Times New Roman", size=13)
        self.var = StringVar()


        try:
            self.database = pd.read_excel('./files/Uniprot_database_2021.xlsx')
            self.mouse = pd.read_excel('./files/Mus musculus Gene Symbol Database Uniprot Verified.xlsx')
        except Exception as e:
            print(e)
            self.Message('Error, "Uniprot_database_2021.xlsx" not found!', 'Please put "Uniprot_database_2021.xlsx" into "files" folder.')
            root.destroy()

        ####### Browse label and button ######
        self.browseLabel = Label(self.frame, font=Font(family="Times New Roman", size=14), text="Please, choose a file:")
        self.browseLabel.place(x = 80, y = 80)
        self.browseButton = Button(self.frame, text="Browse", justify=LEFT, font=Font(family="Times New Roman", size=12, weight='bold'), command=self.browse)
        self.browseButton.place(x = 250, y = 75)

        ######## Sorting Buttongs #######
        self.varDecision = StringVar()
        self.all = Radiobutton(root, font=self.fontRadio,  text="Human", value="human", variable=self.varDecision)
        self.all.select()
        self.all.place(x=450, y=80)

        self.mito = Radiobutton(root, font=self.fontRadio,  text="Mouse", value="mouse", variable=self.varDecision)
        self.mito.place(x=600, y=80)

        self.statusbar = ScrolledText(self.frame, state='disabled')
        self.statusbar.place(x=100, y=200, width=650, height=180)

        self.runbutton = Button(self.frame, text='RUN', fg='black', bg='#b4e67e',
                                font=Font(family="Times New Roman", size=18, weight='bold'), command=self.runbutton_click)
        self.runbutton.place(x=320, y=410, width=150, height=50)

        self.frame.pack()

        self.update_status_box('\n\t >> :: Uniprot Gene Namer Bot Started! :: <<\n')
        self.update_status_box('\n------------------------------------------------------------------------------\n')


    def Message(self, title, message):
        messagebox.showinfo(title=title, message=message)

    def update_status_box(self, text):
        self.statusbar.configure(state='normal')
        self.statusbar.insert(END, text)
        self.statusbar.see(END)
        self.statusbar.configure(state='disabled')

    def clear_status_box(self):
        self.statusbar.configure(state='normal')
        self.statusbar.delete(1.0, END)
        self.statusbar.see(END)
        self.statusbar.configure(state='disabled')

    def check_main_thread(self):
        root.update()
        if self.myThread.is_alive():
            root.after(1000, self.check_main_thread)
        else:
            self.x = True

    def browse(self):

        self.filename = filedialog.askopenfile(parent=self.frame, mode='rb', title='Choose a file')
        self.filenamePretify = str(self.filename).split('/')[-1].split("'>")[0]
        if self.filenamePretify == "None":
            self.Message('Error!', 'Please choose a file!')
            return 0
        self.update_status_box(f'\n "{self.filenamePretify}" file is chosen! \n')
        self.outputLocation =  str(self.filename).split("'")[1].split(".xlsx")[0]+'.xlsx'
        self.outputLocationPretify = str(self.outputLocation).split('/')[-1].split("'>")[0]

    def runbutton_click(self):
        #self.update_status_box(f'\n "{self.varDecision.get()}" is selected! \n')
        self.myThread = Thread(target=self.engine)
        self.myThread.daemon = True
        self.myThread.start()
        root.after(1000, self.check_main_thread)

    def engine(self):
        try:
            self.update_status_box(f'\n The file is reading..! \n')
            self.fileRead = pd.read_excel(self.filename)
        except Exception as e:
            self.update_status_box(f'\n Error is "{e}"! \n')
            self.Message('Error!', 'An Error Occured, please choose a file before run!')
            return 0
        self.update_status_box(f'\n The file is read! \n')

        try:
            self.accessionNum = list(self.fileRead['Accession'])
        except:
            self.accessionNum = list(self.fileRead['Master Protein Accessions'])

        if self.varDecision.get() == 'mouse':
            self.update_status_box(f'\n Running..! \n')
            self.data = GeneNameEngine(self.fileRead, self.mouse)

        elif self.varDecision.get() == 'human':
            self.update_status_box(f'\n Running..! \n')
            self.data = GeneNameEngine(self.fileRead, self.database)

        self.update_status_box(f'\n Completed..! \n')
        self.update_status_box(f'\n Data is saving..! \n')
        try:
            self.data.to_excel(self.outputLocation, index=False)
            self.update_status_box(f'\n Saved as {self.outputLocationPretify}! \n')
            self.Message('Finished!', 'Application Completed!')
        except Exception as e:
            self.update_status_box(f'\n Error is "{e}"! \n')
            self.Message('Error!', 'An Error Occured, please fix it and rerun!')

if __name__ == '__main__':

    root = Tk()
    # root.iconbitmap('files//icon.ico')

    root.title("Uniprot Gene Namer v3.1 by S. Bozkurt")
    root.geometry("840x480")
    root.resizable(0, 0)

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (840 / 2)
    y = (hs / 2) - (480 / 2)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (840, 480, x, y))

    # root.iconphoto(False, tkinter.PhotoImage(file='icon.ico'))
    MyWindow(root)
    root.wm_iconbitmap('files//icon.ico')
    root.mainloop()