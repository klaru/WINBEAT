#!python3
import os, sys
from beatio import *
from beatcalc import *
from tkinter import *

#**************************************************************************
def DistCapAnal(text):
#
#   Determines the effects of distributed capacitances on effective
#   impediance and propagation delay of a transmission line. The equations
#   can be found in any applicable textbook and also easily be derived.      
#**************************************************************************

#var
#  Again : boolean
    
    global IntImped, IntProp, DistCap
    Again = True
    while Again == True :
        clear_textwindow(text)
        text.insert('1.0', 'Calculates the effective impedance and prop delay')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        IntImped = GetParam('What is the intrinsic impedance ?  ',IntImped)
        IntProp = GetParam('What is the intrinsic delay ?  ',IntProp)
        DistCap = GetParam('What is the distributed capacitance ?  ',DistCap)
        IntCap = IntProp/IntImped*1e3/12
        EffImped = IntImped / LoadAdjust(IntCap, DistCap)
        EffProp = IntProp * LoadAdjust(IntCap, DistCap)
        text.insert(END, '\n')
        text.insert(INSERT, 'Line analysis:')
        text.insert(END, '\n')
        text.insert(INSERT, '--------------')
        text.insert(END, '\n')
        text.insert(INSERT, 'Impedance (ohms):                == ')
        text.insert(INSERT, '%3.1f' %(EffImped))
        text.insert(END, '\n')
        text.insert(INSERT, 'Propagation Delay (ns/ft):       == ')
        text.insert(INSERT, '%2.2f' %(EffProp))
        text.insert(END, '\n')
        text.insert(INSERT, 'Intrinsic Capacitance (pf/in):   == ')
        text.insert(INSERT, '%2.2f' %(IntCap))
        text.insert(END, '\n')
        text.insert(INSERT, 'Distributed Capacitance (pF/in): == ')
        text.insert(INSERT, '%2.2f' %(DistCap))
        text.insert(END, '\n')
        input = gui_input(300, 'Another line analysis (y/n)? ', 0)
        if (input == 'n') or (input =='N') : Again = False
        if (Again == False) : break       

