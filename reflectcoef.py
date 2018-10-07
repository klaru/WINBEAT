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
    while True :
        clear_textwindow(text) 
        text.insert('1.0', 'This program calculates the reflection coefficient')
        text.insert(INSERT,'\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(INSERT, '\n')
        LineImp = float(gui_input('Line impedance ?'))
        LoadImp = float(gui_input('Load impedance ?'))
        ReflectionCoef = (LoadImp - LineImp)/(LoadImp + LineImp)
        text.insert(INSERT, 'Reflection coeffiecient = ')		
        text.insert(INSERT, '%1.2f' %(ReflectionCoef))     
        text.pack()
        Again = gui_input('Another reflection calculation (y/n)?')  
        clear_textwindow(text)      
        return Again
     #end while
#end Reflectcoef
