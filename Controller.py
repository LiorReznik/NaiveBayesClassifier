# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 17:29:48 2018

@author: Lior Reznik
"""

from BuildClassifier import BuildClassifier
from Classify import Classify
from View import View
import time
import os

class controller:
    """
    implementing the mvc and observer patterns
    controller class that links between the view(gui) class and the PreProcessing and Classify classes (our model)
    our controller is observerbale by the view(the controller sends to the view updates to show on the screen and boxes) and observer of the model classes(that sends the updates and parameters to the controller)
    """
    def __init__(self,root):
        """init function that calls the view init to build the gui"""
        self.prevmsg=""
        self.root=root
        self.view =View (root,self)
    def check_path(self,path):
        """function to check the path that the user gave us, the function checks if the path contains all of the files that we need and also if the files is not empty"""
        self.__path=path
        list_of_file_names={'Structure.txt','test.csv','train.csv'}
        if list_of_file_names <= set(os.listdir(self.__path)):#checking if the path have all the requierd files
            if os.path.getsize(os.path.join(self.__path,'Structure.txt')) > 0 and os.path.getsize(os.path.join(self.__path,'test.csv')) >0 and  os.path.getsize(os.path.join(self.__path,'train.csv'))>0:#checking if the files are not empty
                self.view.Build_Button.config(state='active')
                self.view.Bins_Entry.configure(state='normal',text='Enter number of bins',font=("Calibri",12),justify="center",exportselection=0)
            #sending to the view the  error messages
            else:
                self.view.file_error_handling("","One or more of the files is empty")
        else:
            self.view.file_error_handling("required files are missing", "The directory must have Structure.txt,test.csv and train.csv files")
 
    def update(self,msg):
            """the functions gets updates from the model and sends them to the view, also it gets arrguments from the preprocessing to pass them to the classify class"""
            print msg[0]
            if msg[0]=="End Of Building":
               self.view.Classify_Button.configure(state="normal") 
               self.view.show_updates(""+"","all done it took "+str(time.time()-self.start))
               self.__rang=msg[1]
               self.__numeric=msg[2]
               self.__statistics=msg[3]
               self.__k=msg[-3]
               self.__classes=msg[-2]
               self.__abs_n=msg[-1]
               self.view.update("Build is done, please click on Classify.")

            elif msg[0]=="All Done":
                 self.view.show_updates(""+"","all done it took "+str(time.time()-self.start))
                 self.view.update("All Done Open "+os.path.join(self.__path,'Output.txt')+" for results.")
            else:
                  self.view.show_updates("Last operation: "+self.prevmsg,"Now working on "+msg[0])
            self.prevmsg=msg[0]   
    
    def  builder(self):
        """the function gets the number of bins and checks if it is a ligeal number if so , the function starts the preprocessing process by calling it's init function, if not it revokes the view error hendaling function"""
        self.Number_Of_Bins=self.view.Bins_Entry.get()
        if self.__is_int(self.Number_Of_Bins) and int(self.Number_Of_Bins)>0:
            self.start=time.time()
            BuildClassifier(os.path.join(self.__path,'train.csv'),os.path.join(self.__path,'Structure.txt'),int(self.Number_Of_Bins),self)
            self.view.Build_Button.configure(state="disabled")
        else:
            self.view.file_error_handling("","please enter a valid number of bins")

    def classify(self):
        """the function starts the classify process by inboking it's init method"""
        Classify(os.path.join(self.__path,'test.csv'),self.__rang,self.__numeric,self.__statistics,self.__k,self.__classes,self.__abs_n,self)
        self.view.Build_Button.configure(state="active")
        
    def __is_int(self,string):
        """function to check if a given string is an int"""
        try: 
            int(string)
            return True
        except ValueError:
            return False  






