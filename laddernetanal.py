#! python3
import os, sys, math
from beatio import *
from beatinc import *
from beatmath import *

#**************************************************************************
def LadderNetAnal():
# Completely modified 6/89, Ulf Schlichtmann 
# This def requests as input the line impedance and propagation delay
#   #constant of a line as well as the total length of the line and the rise
#   time of the signal that needs to be analyzed.
#   It : proceeds to compute the cutoff frequency of that signal and the
#   number of RLC segments this line has to be split up into if it is to be
#   modelled correctly by SPICE. The values for the R, L and C elements of each
#   segment are also calcutlated and output.
#   To calculate the number of required segments, a "rule of thumb" is used  
#**************************************************************************

#var
#  Again:boolean
#  SegCap, SegInd, SegRes,  # values per segment 
#  CornerFrequ :real
#  NumSeg:integer

#begin   LadderNetAnal 
    global IntImped, IntProp, Resist, TraceLength
    Again = True
    while Again == True : #begin
        os.system('cls')
        print('Trace Pi Model Generation')
        print('-----------------------------------------')
        print('\n')
        IntImped, IntProp, Resist, TraceLength, TRise = GetNetInfo()
        CornerFrequ = 2/TRise           # Cutoff Frequency 
        IntCap = IntProp*TraceLength/IntImped*1000/12
                                     #1000:Conversion to pF
                                     #12: Conversion from ft to inch 
        IntInd = IntProp*TraceLength*IntImped/12
                                     #12: Conversion from ft to inch 
        NumSeg = math.trunc(5/2*CornerFrequ* math.sqrt(IntCap*IntInd)*math.sqrt(0.001))
                                     # "Rule of Thumb" 
                                     # math.sqrt(.001): #unit correction factor 
        print('\n')
        print('Trace Pi Model Analysis')
        print('------------------------')
        print('Calculations have determined the following number of segments.')
        print('Confirm this number by hitting RETURN or change it.')
        NumSeg = GetIParam ('Number of segments:                ',NumSeg)

        SegCap = IntCap/NumSeg          # Capacitance per segment 
        SegInd = IntInd/NumSeg          # Inductance per segment 
        SegRes = Resist*TraceLength/NumSeg/1000  # Resistance per segment 
                                     # 1000 : Conversion mohms --> ohms 

        print('Capacitance per segment (pF):      %2.2f' %(SegCap))
        print('Inductance per segment (nH):       %2.2f' %(SegInd))
        print('Resistance per segment (ohms):     %2.2f' %(SegRes))
        print('\n')

        Again = GetResponse('One More Time ?', 'y')
        if (Again == False) : break
   #end while
#end LadderNetAnal



