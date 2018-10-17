#!python3
import os, sys
from beatio import *
from beatcalc import *

#**************************************************************************
def DistCapAnal():
#
#   Determines the effects of distributed capacitances on effective
#   impediance and propagation delay of a transmission line. The equations
#   can be found in any applicable textbook and also easily be derived.      
#**************************************************************************

#var
#  Again : boolean
    
    global IntImped, IntProp, DistCap
    
    while True :
        os.system('cls')
        print('Calculates the effective impedance and prop delay')
        print('-----------------------------------------------------------')
        print('\n')
        IntImped = GetParam('What is the intrinsic impedance ?',IntImped)
        IntProp = GetParam('What is the intrinsic delay ? ',IntProp)
        DistCap = GetParam('What is the distributed capacitance ?',DistCap)
        IntCap = IntProp/IntImped*1e3/12
        EffImped = IntImped / LoadAdjust(IntCap, DistCap)
        EffProp = IntProp * LoadAdjust(IntCap, DistCap)
        print('\n')
        print('Line analysis:')
        print('--------------')
        print('Impedance (ohms):                == %3.1f' %(EffImped))
        print('Propagation Delay (ns/ft):       == %2.2f' %(EffProp))
        print('Intrinsic Capacitance (pf/in):   == %2.2f' %(IntCap))
        print('Distributed Capacitance (pF/in): == %2.2f' %(DistCap))
        print('\n')
        print('Another line analysis (y/n)? ')
        temp = msvcrt.getch()
        if (temp == b'n') : break

