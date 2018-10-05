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
    if True :
        text.delete('1.0', END) 
        text.insert('1.0', 'This program calculates the reflection coefficient')
        text.insert('2.0', '\n')
        text.insert('3.0', '-----------------------------------------------------------')
        text.insert('4.0', '\n')
#        LineImp = GetParam('Line impedance ? ',LineImp)
#        LoadImp = GetParam('Load impedance ? ',LoadImp)
        ReflectionCoef = (LoadImp - LineImp)/(LoadImp + LineImp)
        text.insert('5.0', 'Reflection coeffiecient = ', ReflectionCoef)			    #ReflectionCoef:1:2
        text.insert('6.0', '\n')
        for line in range(5, 27) :
            text.insert("%d.%d" %(line, 0), '                                                                             ')         
        text.pack()
#        Again = GetResponse('Another reflection calculation (y/n)?', 'y')
#        if (Again == False) : break
     #end while
#end Reflectcoef
