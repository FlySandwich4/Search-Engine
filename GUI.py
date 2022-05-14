import tkinter as tk
from tkinter import Y, ttk
from tkinter import font
from typing import Type
import Query
import json

class EmptyInputException(Exception):
    pass

class EmptyWebsToSearchException(Exception):
    pass

class myWindows:

    def __init__(self):
        self.Windows = tk.Tk()

        self.width = 700
        self.height = 600
        self.win_w = self.Windows.winfo_screenwidth()
        self.win_h = self.Windows.winfo_screenheight()
        
            

        self.Windows.geometry(f"{self.width}x{self.height}+{(self.win_w//2-(self.width//2))}+{(self.win_h//2-(self.height//2))}")
        self.Windows.maxsize(self.width,self.height)
        self.Windows.minsize(self.width,self.height)
        self.Windows.title("I don't know every thing search engine")

        
        #Entry for query
        self.Entry_Query = tk.Entry(self.Windows, text= "Search What You Want")
        self.Entry_Query.place(x=self.width/2-300,y=self.height/4 - 60,width=500,height=30)

        #Text for Google
        

        #Label for Google title
        
        self.Show_Win_Label = tk.Label(self.Windows, text="D",fg="#f57a00")
        self.Show_Win_Label.place(x=self.width/2-72,y=0,width=45)
        self.Show_Win_Label.configure(font=("Times New Roman", 60, "italic",font.BOLD))
        self.Show_Win_Label = tk.Label(self.Windows, text="OOGLE",fg="#26b5e0")
        self.Show_Win_Label.place(x=self.width/2-28.5,y=27,width=100)
        self.Show_Win_Label.configure(font=("Times New Roman", 30, "italic"))
        


        self.Show_Win_Label = tk.Label(self.Windows, text="THE DOG, THE GOOGLE, THE DOOGLE",fg="#0d9aba")
        self.Show_Win_Label.place(x=self.width/2-150,y=63,width=300)
        self.Show_Win_Label.configure(font=("Times New Roman", 10, "italic",font.BOLD))

        #Label for choosing how many values
        self.Label_howManyWebs = tk.Label(self.Windows, text="How many Webs to display?")
        self.Label_howManyWebs.place(x=self.width/2-300,y=self.height/4-25)
        self.Label_howManyWebs.configure(font=("Times New Roman", 15, "italic"))

        #Button of Search button
        Button_Search_height = 30
        Button_Search_width = 100
        self.Button_Search = tk.Button(self.Windows, text='SEARCH IT!',command = self.getAllWebs,font=("Times New Roman",15,font.BOLD))
        self.Button_Search.place(x=self.width/2+200,y=self.height/4-60,width=Button_Search_width,height=Button_Search_height)

        #List Box of choosing how many value
        self.ListBox_howManyWebs = ttk.Combobox(self.Windows,text = "select a number")
        self.ListBox_howManyWebs['values'] = (5,10,15,20,25)
        self.ListBox_howManyWebs.place(x=self.width/2-300,y=self.height/4)

        #null
        self.scrollbar = tk.Scrollbar(self.Windows)
        self.scrollbar.place(x=self.width/2+280,y=self.height/4+30, width= 20, height= 370)

        self.scrollbarX = tk.Scrollbar(self.Windows,orient='horizontal')
        self.scrollbarX.place(x=self.width/2-300,y=self.height/4+400, width= 580, height= 20)

        self.myList = tk.Listbox(self.Windows,xscrollcommand = self.scrollbarX.set,yscrollcommand= self.scrollbar.set)

        
        self.myList.place(x=self.width/2-300,y=self.height/4+30, width= 580, height= 370)
        self.scrollbar.config(command=self.myList.yview)
        self.scrollbarX.config(command=self.myList.xview)
        
    





    #testing function
    def increment(self):
        for i in range(100):
            self.myList.insert(tk.END,str(i))

    #building index and changing labels
    def getAllWebs(self):
        try:
            self.myList.delete(0,tk.END)
            if self.Entry_Query.get().strip() == "":
                raise EmptyInputException
            
            if self.ListBox_howManyWebs.get() == "":
                raise EmptyWebsToSearchException

            DocList = Query.DocumentRetrival(self.Entry_Query.get(),int(self.ListBox_howManyWebs.get()))
            with open('url_index.json', 'r') as FA:
                LstA = json.load(FA)
                for i in DocList:
                    self.myList.insert(tk.END, f"{LstA[i]}")
                    self.myList.insert(tk.END, "\n")

        except EmptyInputException:  
            self.myList.insert(tk.END, "Doggle Can't Find Input!")

        except EmptyWebsToSearchException:
            self.myList.insert(tk.END, "Doggle Don't Know How Many Webs to Display!")

        except:
            if self.Entry_Query.get().lower() == "doogle":
                self.myList.insert(tk.END, "Oh my God! Doogle is not in the Library? Somebody should add it RIGHT NOW!")
            else:
                self.myList.insert(tk.END, "No Related Content! Please check your input!")


    def start(self):
        self.Windows.mainloop()


    
    





if __name__ == "__main__":
    a = myWindows()
    a.start()
    

   
   
