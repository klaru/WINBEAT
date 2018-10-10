#! python3
import os, sys
from beatinc import *
from beatio import *
from tkinter import *

 
#****************************************************************************
def Reflectcoef(text) :
#****************************************************************************
# This program calculates the reflection coefficient given the load
# impedance and the line impedance

    global LineImp, LoadImp
    Again = True
    while Again == True :
        clear_textwindow(text) 
        text.insert('1.0', 'This program calculates the reflection coefficient')
        text.insert(INSERT,'\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(INSERT, '\n')
        LineImp = GetParam('Line impedance ?', LineImp)
        LoadImp = GetParam('Load impedance ?', LoadImp)      
        ReflectionCoef = (LoadImp - LineImp)/(LoadImp + LineImp)
        text.insert(INSERT, 'Reflection coeffiecient = ')		
        text.insert(INSERT, '%1.2f' %(ReflectionCoef))     
        text.pack()
        input = gui_input(300, 'Another reflection calculation (y/n)?', 0)      
        if (input == 'n') or (input =='N') : Again = False        
        if (Again == False) : break
     #end while
#end Reflectcoef
