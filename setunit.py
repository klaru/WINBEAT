#! python3
import os, sys
from beatinc import *
from beatio import clear_textwindow, gui_input
from tkinter import *

#************************************************************************
def SetUnit(text):
#                                                                        
#  This routine enables the user to select whether he wants to enter     
#  his input data in the metric or in the imperial system of measurement 
#  #units.                                                                
#  Added 6/89 , Ulf Schlichtmann                                         
#************************************************************************

#var
#   UnitChar, temp : char

    global base, UnitSys
    clear_textwindow(text)
    text.insert('1.0', 'Set the Unit System for your input data')
    text.insert(INSERT, '\n')
    text.insert(INSERT, '---------------------------------------')
    text.insert(INSERT, '\n')
    text.insert(INSERT, 'You may now select whether you want to input your data in ')
    text.insert(INSERT, '\n')
    text.insert(INSERT, 'the Metric or in the Imperial system.')
    text.insert(INSERT, '\n')
    text.insert(INSERT, 'keep in mind that the data in the library are in ')
    text.insert(INSERT, '\n')
    text.insert(INSERT, 'the Imperial system')
    text.insert(INSERT, '\n')
    text.insert(INSERT, 'Currently selected: ')
    text.insert(INSERT, base[UnitSys])
    text.insert(INSERT, '\n')
    text.insert(INSERT, '\n')
    if UnitSys == 1 :
        UnitChar = 'm'
    elif UnitSys == 2 :
        UnitChar = 'i'
    text.insert(INSERT, 'Metric or Imperial system?  (m or i)  [')
    text.insert(INSERT, UnitChar)
    text.insert(INSERT, ']')

    while True :
#        temp = msvcrt.getch()
        temp = gui_input('Metric or Imperial system?  (m or i)', 0)
        if (temp == 'm') or (temp == 'i') or (temp == '\r') : break
    if (temp != '\r') : UnitChar = temp
    if UnitChar == 'm' :
        UnitSys = 1
    elif  UnitChar == 'i' : 
         UnitSys = 2
    clear_textwindow(text)
