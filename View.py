# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 00:58:53 2018

@author: Lior Reznik
"""

from Tkinter import *
import tkFileDialog
import tkMessageBox 


class View:
    def __init__(self, main,controller):
        self.controller=controller
        self.main=main
        self.__build

    @property        
    def __build(self):
        """function that builds the gui"""
        self.prevmsg=""
        self.main.geometry("750x450+950+187")
        self.main.title("Naive Bayes Classifier")
        self.main.configure(background="#ffffff")
        self.Browse_Button = Button(self.main,background='#d9d9d9',activebackground="#d9d9d9",activeforeground="#000000")
        self.Browse_Button.place(relx=0.81, rely=0.24, height=34, width=130)
        self.Browse_Button.configure(text="Browse",command=self.__findpath)

        self.Build_Button = Button(self.main,state='disabled',background='#d9d9d9',activebackground="#d9d9d9",activeforeground="#000000")
        self.Build_Button.place(relx=0.23, rely=0.49, height=34, width=247)
        self.Build_Button.configure(text="Build",command=self.controller.builder)
        

        self.Browse_Entry = Entry(self.main,state='readonly',background="white",font="TkFixedFont",insertbackground="black",readonlybackground="white",width=254,text='Click on Browse to select the folder path',)
        self.Browse_Entry.place(relx=0.26, rely=0.24,height=30, relwidth=0.54)
        
        
        self.Classify_Button=Button(self.main,state='disabled',background='#d9d9d9',activebackground="#d9d9d9",activeforeground="#000000")
        self.Classify_Button.place(relx=0.23, rely=0.6, height=34, width=247)
        self.Classify_Button.configure(text="Classify",command=self.controller.classify)

        self.Path_Label = Label(self.main,background="#ffffff",foreground="#000000",text="Directory path")
        self.Path_Label.place(relx=0.03, rely=0.24, height=31, width=104)
      

        self.Bins_Label = Label(self.main,background="#ffffff",foreground="#000000",text="Discretiztion Bins")
        self.Bins_Label.place(relx=0.03, rely=0.33, height=21, width=96)
        
        self.Bins_Entry = Entry(self.main,background="white",font="TkFixedFont",insertbackground="black",readonlybackground="white",state='readonly')
        self.Bins_Entry.place(relx=0.26, rely=0.32,height=30, relwidth=0.14,width=154)
        
        self.InfoLabel = Label(self.main,background="white",text="")
        self.InfoLabel.place(relx=0.26, rely=0.90, height=21, width=400)
        self.InfoLabel2 =Label(self.main,background="white",text="")
        self.InfoLabel2.place(relx=0.26, rely=0.95, height=21, width=400)
       
    def __findpath(self):
        """function to ask the path from the user"""
        self.path=tkFileDialog.askdirectory(parent=self.main,title='Please select a directory')
        #if the user heats the cancule batuoon the we will exit the program
        if not self.path:
            tkMessageBox.showinfo('','Exiting...')
            self.main.destroy()
        self.Browse_Entry.configure(state='normal')
        self.Browse_Entry.delete(0, END)
        self.Browse_Entry.insert(0, self.path)
        self.Browse_Entry.configure(state='readonly')
        #sending the path to check in the controller (to find out if the path contains all the files we need)
        self.controller.check_path(self.path)
  
            
    def update(self,msg):
            """function to show a messagebox with the desiered massage that comes from the controller"""
            tkMessageBox.showinfo("",msg)

    def show_updates(self,prevmsg,msg):
       """function to show updates on the frame"""
       self.InfoLabel.configure(text=prevmsg)
       self.InfoLabel2.configure(text=msg)
       
    
    
   
    def file_error_handling(self,titlemsg,msg):
        tkMessageBox.showerror(titlemsg,msg)
        ans=tkMessageBox.askyesno(message='Do you want to try again?')
        if not ans:
                tkMessageBox.showinfo('','Exiting...')
                self.main.destroy()
        self.__findpath()

    


 
