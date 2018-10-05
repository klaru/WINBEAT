#! python3
import os, sys
from beatinc import *

#************************************************************************
def SetUnit():
#                                                                        
#  This routine enables the user to select whether he wants to enter     
#  his input data in the metric or in the imperial system of measurement 
#  #units.                                                                
#  Added 6/89 , Ulf Schlichtmann                                         
#************************************************************************

#var
#   UnitChar, temp : char

    global base, UnitSys
    os.system('cls')
    print('Set the Unit System for your input data')
    print('---------------------------------------')
    print('\n')
    print('You may now select whether you want to input your data in ')
    print('the Metric or in the Imperial system.')
    print('\n')
    print('Please keep in mind that the data in the library are in ')
    print('the Imperial system')
    print('\n')
    print('Currently selected: ',base[UnitSys])
    print('\n')
    print('\n')
    if UnitSys == 1 :
        UnitChar = 'm'
    elif UnitSys == 2 :
        UnitChar = 'i'
    print('Metric or Imperial system?  (m or i)  [',UnitChar,']')

    while True :
        temp = msvcrt.getch()
        if (temp == b'm') or (temp == b'i') or (temp == b'\r') : break
    if (temp != b'\r') : UnitChar = temp
    if UnitChar == 'm' :
        UnitSys = 1
    elif  UnitChar == 'i' : 
         UnitSys = 2

