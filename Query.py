from cgitb import text
import tkinter as tk
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

        
        self.Show_Win_Label = tk.Label(self.Windows, text=self.win_w)
        self.Show_Win_Label.place(x=1,y=1)

        self.__Button__Search = tk.Button(self.Windows, text='SEARCH IT!', command = self.increment)
        self.__Button__Search.place(x=250,y=250)


    def increment(self):
        self.win_w += 1
        self.Show_Win_Label['text'] = self.win_w

    def start(self):
        self.Windows.mainloop()


    
    





if __name__ == "__main__":
    a = myWindows()
    a.start()
    

   