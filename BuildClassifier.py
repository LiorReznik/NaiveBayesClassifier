# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 18:03:55 2018

@author: Lior Reznik
"""

import csv
from collections import Counter
from math import ceil
class BuildClassifier:
    
    def __init__(self,train_path,structure_path,bins,observer):
        self.__observer=observer
        self.__statistics={}
        self.__structure_path=structure_path
        self.__train_path=train_path
        self.__bins=bins
        self.__update_observers("Strating the process")
        self.__read_structure
        self.__read_train
        self.__find_index
        self.__transpose
        self.__find_k_factor
        self.__calc_abs_n
        if self.__numeric_attrs[0]:self.__numeric
        if self.__non_numeric_attrs[0]:self.__non_numeric
        
        
        
        self.__update_observers("End Of Building",self.__ranges,self.__numeric_attrs,self.__statistics,self.__k,self.__classes,self.__abs_n)

    @property    
    def __calc_abs_n(self):
        """function to calculate the number of class repeats in the file"""
        self.__abs_n=dict(Counter(self.__train[-1][1:]))
    def __update_observers(self,*msg):
        """function to update the observers/controller"""
        self.__observer.update(msg)
    @property
    def __find_k_factor(self):
        """function to findout the k_Factor(number of possibale options of each attribute), the funcion stores the information in a new dictionary """
        #the keys of the new dictionary is the keys of the structure and the values is num of bins in case of numeric data or the len of the list in the structure in the case of non numeric
        self.__k={}
        for key in self.__structure.keys():
            self.__k[key]=len(self.__structure[key]) if self.__structure[key][0]!="NUMERIC" else self.__bins
        
    @property       
    def __numeric(self):
        """function that handels all the numeric operations"""
        self.__ranges={}
        self.__update_observers("Working on numeric data")
        for row in self.__numeric_attrs[1]:
                self.__update_observers("Preprocessing "+self.__train[row][0]+" attr")
                self.__numeric_preprocessing(row)
                self.__statistics_calculation(row)

    @property            
    def __non_numeric(self):
        """function that handels all the non_numeric operations"""
        self.__update_observers("Working on Non-numeric data")
        self.__non_numericrepeats,self.__non_numericrepeatsGiveanclass={},{}
        for row in self.__non_numeric_attrs[1]:
            self.__update_observers("Preprocessing "+self.__train[row][0]+" attr")
            self.__non_numeric_preprocessing(row)
            self.__statistics_calculation(row)
 
             
    @property
    def __read_structure(self):
        """function to read the structure file and learn the dataset"""
        self.__update_observers("Reading the structure")
        with open(self.__structure_path,'r') as f:#openning the file
            Structure=[line.split() for line in f]#reading the file to a list of lists
        self.__structure={line[1]:line[2].strip('}').strip('{').split(',') for line in Structure}#making a dict from the list of lists when the key is the name of the attribute and the value is the values that can be for this attribute
        #building a list that will hold all the classes that can be
        self.__classes=self.__structure['class']
        del self.__structure['class']
        #building list that will hold all the numeric and non numeric attrs names 
        self.__numeric_attrs=[]
        self.__non_numeric_attrs=[]
        for key in self.__structure:
            if self.__structure[key][0]!= 'NUMERIC':
                self.__non_numeric_attrs.append(key)
            else:
                self.__numeric_attrs.append(key)
        
    @property               
    def __transpose(self):
        """function to transpose the train, so we will get each attribute in row"""
        self.__train=map(list, zip(* self.__train))

    
    @property 
    def __read_train(self):
         """function to read the train dataset and store it in list of lists"""
         self.__update_observers("Reading the train")
         with open(self.__train_path,'r') as f:
             reader = csv.reader(f)
             self.__train = reader.next()
             rest = [row for row in reader]
             self.__train=[self.__train]+rest
             
    @property
    def __find_index(self):
       """function to findout the indexes of the numeric and non-numeric attributes"""
       ind=[self.__train[0].index(var) for var in self.__numeric_attrs]
       self.__numeric_attrs=[self.__numeric_attrs,ind]
       ind=[self.__train[0].index(var) for var in self.__non_numeric_attrs]
       self.__non_numeric_attrs=[self.__non_numeric_attrs,ind]
       
             
    
       

    def __is_float(self,string):
        """function to check if the given string is numeric or not"""
        try: 
            float(string)
            return True
        except ValueError:
            return False
    
    
    def __str_to_num(self,row):
        """function that gets a row and converts it's values to float(if it possibale)"""
        self.__train[row]=map(lambda y: float(y) if self.__is_float(y) else y,self.__train[row])

      

    def __mean(self,row):
        """function to findout the mean of a givean nonnumeric row"""
        vector=filter(lambda x:type(x)!=str,self.__train[row]) 
        return sum(vector)/float(len(vector))    
    def __mode(self,row):
        """function to findout the mode of a givean numeric row"""
        vector=dict(Counter(filter(lambda x:x in self.__structure[self.__non_numeric_attrs[0][self.__non_numeric_attrs[1].index(row)]],self.__train[row])))
        return max(vector, key=vector.get)
        

       
    def __numeric_preprocessing(self,row):
        """function to make a numeric preprocessing
           first of all , the function converts the attribues of each row into float(if possible)
           second, the function fills the missing (or noisy) data with the mean of the row
           third, the function sets the row into bins
        """
        self.__str_to_num(row)    
        self.__fill_missing_numeric(row)
        self.__set_to_bins(row)
          
    def __fill_missing_numeric(self,row):
        """function that fills the missing and/or noisy  data with the mean of the row"""
        mean=self.__mean(row)
        self.__train[row][1:]=map(lambda y:mean if type(y)!=float else y,self.__train[row][1:])
      

    def _fill_missing_non_numeric(self,row):
        """function that fills the missing and/or noisy data with the mode of the row"""
        mode=self.__mode(row)
        self.__train[row][1:]=map(lambda y:mode if y not in self.__structure[self.__non_numeric_attrs[0][self.__non_numeric_attrs[1].index(row)]] else y,self.__train[row][1:])
        
        
    def __non_numeric_preprocessing(self,row):
        """function that doing the non numeric preprocessing"""
        self._fill_missing_non_numeric(row)
        
    
                
    def __set_to_bins(self,row):
        """function to distribute the row into bins"""
        #finding out the delta of the row
        delta=max(self.__train[row][1:])-min(self.__train[row][1:])
        # if the delta is not zero the program will calculate the rang and then change all the numbers into the higher bound of each bin that they belong to
        if delta!=0:
            self.__rang=ceil(delta/float(self.__bins))
            self.__train[row][1:]=map(lambda y:ceil(y/float(self.__rang))*self.__rang ,self.__train[row][1:])
            self.__ranges[self.__train[row][0]]=self.__rang
                
    def __statistics_calculation(self,row):
        """function to calculate the statistics of the row"""
        self.__update_observers("Doing some statistics on "+self.__train[row][0]+" attr")
        #calculating the nc (intersection)
        self.__statistics[self.__train[row][0]]=self.__findout_nc(row)
        #running on all the keys of the statistics of the row, that now holds the nc
        for statistics_key in self.__statistics[self.__train[row][0]].keys():
               #checking if the class of the keys represents in ths abs_n if so, sending all the relevant data into laplacian_Estimator to calc the statistics
                if statistics_key[-1] in self.__abs_n.keys():
                    self.__statistics[self.__train[row][0]][statistics_key]=self.__laplacian_estimator(self.__statistics[self.__train[row][0]][statistics_key],self.__k[self.__train[row][0]],self.__abs_n[statistics_key[-1]])
    def __laplacian_estimator(self,nc,k,abs_n):
        """function to calculate statistics of a givean attrinute, the function uses 'the laplacian estimator' formula"""
        return (nc+1)/float(abs_n+k)         
        
    def __findout_nc(self,row):
        """function that calculates the nc(intersection)"""
        return dict(Counter(zip(self.__train[row],self.__train[-1])[1:]))       
    
    