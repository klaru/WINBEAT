#! python3
import os, sys, math
from beatinc import *
from beatio import *
from tkinter import *

#procedure FourierValues(var Cmag, Cphase:extendedvector);
#procedure FourierAnal;

global NumHarmonics
Cmag = [0.0] * (NumHarmonics + 1)
Cphase = [0.0] * (NumHarmonics + 1)
Slope = [0.0] * (NumHarmonics + 1)
Csub = [0.0] * (NumHarmonics + 1)

def FourierValues(text):
#var
#  Csub,
#  Slope : extendedvector;
#  X,K : integer;
#  NumHarmonics,NumPoints : integer;
#  A,B : real;
#  Period : extended;

    global NumHarmonics, NumPoints, Period
    text.insert(END, '\n')
    NumHarmonics = GetIParam('Number of Harmonics? ', NumHarmonics)
    NumPoints = GetIParam('Number of Points? ', NumPoints)
    Period = GetParam('Enter Period : ', Period)
    for X in range(1, NumPoints + 1) :
        text.insert(END, '\n')
        Time[X] = GetParam('Enter time : ', Time[X])
        Magnitude[X] = GetParam('Enter magnitude: ', Magnitude[X])
    #end for

    Magnitude[NumPoints + 1] = Magnitude[1]
    Time[NumPoints + 1] = Period
    Cmag[0] = 0
    Cphase[0] = 0
    for X in range(1, NumPoints + 1) :
        Cmag[0] = Cmag[0] + 0.5*(Magnitude[X+1]+Magnitude[X])*(Time[X+1]-Time[X])/Period
        Slope[X] = (Magnitude[X+1] - Magnitude[X])/(Time[X+1] - Time[X])
    #end for
    Csub[1] = Slope[1]-Slope[NumPoints]
    for X in range(1, NumPoints) :
        Csub[X+1] = Slope[X+1] - Slope[X]
    for K in range(1, NumHarmonics + 1) :
        A = 0
        B = 0
        for X in range(1, NumPoints + 1) :
            A = -Csub[X] * math.cos(2*pi*K*Time[X]/Period) + A
            B = Csub[X] * math.sin(2*pi*K*Time[X]/Period) + B
        #end for
        Cmag[K] = (Period/(math.pow(2*pi*K,2)))*math.sqrt(math.pow(A,2) + math.pow(B,2))
        Cphase[K] = math.atan2(B,A)
    #end for
    clear_textwindow(text)
    text.insert('1.0', 'FUNCTION DEFINITION')
    text.insert(END, '\n')
    text.insert(INSERT, '------------------------------')
    text.insert(END, '\n')
    text.insert(INSERT, 'Period(ns) ')
    text.insert(INSERT, Period)
    text.insert(END, '\n')
    text.insert(INSERT, '| Point | Time(ns)| Magnitude |')
    text.insert(END, '\n')
    text.insert(INSERT, '-------------------------------')
    text.insert(END, '\n')
    for X in range(1, NumPoints + 1) :
        text.insert(INSERT, '|%6d' %(X))
        text.insert(INSERT, '  |%7d' %(Time[X]))
        text.insert(INSERT, ' |%10d' %(Magnitude[X]))
        text.insert(INSERT,' |')
        text.insert(END, '\n')       
    return Cmag, Cphase
#end FourierValues

#****************************************************************************
def FourierAnal(text):
#****************************************************************************

#var
#   Cmag,Cphase : extendedvector;
#   Again : boolean;
#   K : integer;
#   FourierCoefDat : File of extended;

    Again = True
    while Again == True :
        FourierCoefDat = open('FourierCoef.dat','w')
        clear_textwindow(text)
        text.insert('1.0', 'This program executes a fourier analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        Cmag, Cphase = FourierValues(text)
        text.insert(INSERT, '| Harmonic | C_Mag     | C_Phase    |')
        text.insert(END, '\n')
        text.insert(INSERT, '-------------------------------------')
        text.insert(END, '\n')
        lineout = str(NumHarmonics) + str(Period)
        FourierCoefDat.write(lineout)
        for K in range(NumHarmonics + 1) :
            text.insert(INSERT, '|%9d' %(K))
            text.insert(INSERT, ' |%10d' %(Cmag[K]))
            text.insert(INSERT, '  |%10d' %(Cphase[K]))
            text.insert(INSERT,' |')
            text.insert(END, '\n')           
            lineout = str(K) + str(Cmag[K]) + str(Cphase[K])
            FourierCoefDat.write(lineout)
        #end for
        text.insert(INSERT, '(Coefficient data written to file "FourierCoefDat".)')
        text.insert(END, '\n')
        FourierCoefDat.close()
        input = gui_input(300, 'Another fourier analysis (y/n)? ',0)
        if (input == 'n') or (input =='N') : Again = False          
        if Again == False: break
    #end while
#end FourierAnal

