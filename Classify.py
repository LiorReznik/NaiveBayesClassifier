# -*- coding: utf-8 -*-
"""
Created on Sat Jun 02 00:19:51 2018

@author: Lior Reznik
"""
import csv,os
from math import ceil
class Classify:
    def __init__(self,path,rang,numeric,statistics,k,classes,abs_n,observer):
        self.__path=path
        self.__rang=rang
        self.__numeric=numeric
        self.__statistics=statistics
        self.__classes= classes
        self.__k=k
        self.__abs_n=abs_n
        self.__observer=observer
        self.__update_observers("Doing some preperations")
        self.__prepare
        self.__classify        
        self.__update_observers("All Done")
    @property    
    def __statistics_class(self):
        """building a dictonary when the keys is the classes and the value is 1 (we will multiply all the values with the statistics of the attrs)"""
        self.__classes={element:1 for element in self.__classes}
    @property
    def __prepare(self):
        """function to prepare the dataset for clssification"""
        #reading the file
        self.__read_test
        #tarnsposing the dataset
        self.__transpose
        #deleting the class row
        del self.__test[-1]
        #running on the numeric attributs and seting them to bins
        for row in self.__numeric[1]:
            self.__str_to_num(row)
            self.__set_to_bins(row)
        #transposing back
        self.__transpose

           
    @property    
    def __read_test(self):
        """function to read the test file"""
        self.__update_observers("Reading the test")
        with open(self.__path,'r') as f:
             reader = csv.reader(f)
             self.__test=reader.next()
             rest = [row for row in reader]
             self.__test=[self.__test]+rest
    @property
    def __classify(self):
        """function to classify the file and to write the results into a file"""
        with open(os.path.join(os.path.dirname(self.__path),"Output.txt"), 'w') as f:
         ind=0
         for row in self.__test[1:]:
            self.__statistics_class
            for attr in range(0,len(row)):
                self.__mul(attr,self.__make_pairs(row[attr]))
            ind+=1
            #writing to the file
            f.write(str(ind)+","+str(self.__find_max)+"\n")
    @property
    def __find_max(self):
        """function to find out the maximal class"""
        return max(self.__classes, key=self.__classes.get)
        
    def __mul(self,attr,pairs):
        """function to multiply the statistics"""
        for elem in pairs:
            #checking if we have calculated the statistics of the element, if so multypling the result that we have with the statistics , else calling the laplacian estimator method to calculate the ststistics for the attr
            if elem in self.__statistics[self.__test[0][attr]].keys():
                self.__classes[elem[-1]]*=self.__statistics[self.__test[0][attr]][elem]
            else:
                self.__classes[elem[-1]]*=self.__laplacian_estimator(self.__abs_n[elem[-1]],self.__find_k(attr))
           
    def __make_pairs(self,attr):
       """function to make all the nc options for the attributes value"""
       return [(attr,elm) for elm in self.__classes]
           
    def __find_k(self,attr):
       """function to find  a specific k for the givean attr"""
       return self.__k[self.__test[0][attr]]        
    
                
    
    def __laplacian_estimator(self,n,k):
        """function to calculate propabilty for missing values"""
        return +1/float(n+k)         
    def __update_observers(self,*msg):
        """function to update the observer"""
        self.__observer.update(msg)
    @property               
    def __transpose(self):
        """function to transpose the test list of lists"""
        self.__test=map(list, zip(* self.__test))
    def __str_to_num(self,row):
        """function to convert the numerical strings into float"""
        self.__test[row][1:]=map(lambda y: float(y),self.__test[row][1:])
    def __set_to_bins(self,row):
        """puting the numerical data into bins with the rang givean from the builder"""
        if self.__test[row][0] in self.__rang:
            self.__test[row][1:]=map(lambda y:ceil(y/float(self.__rang[self.__test[row][0]]))*self.__rang[self.__test[row][0]] ,self.__test[row][1:])

       