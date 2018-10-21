#! python3
import os, sys
from beatinc import *
from beatcalc import *
from winbeatio import *

#**************************************************************************
def MicroStripAnal(text):
#                                                                          
# Calculates the line impedance of a microstrip trace using the model      
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs" for an isolated conductor. He breaks the line        
# capacitance up into:                                                     
#                                                                          
#   Cppu = the upper plate capacitance (UpCap)                            
#   Cpp  = the lower plate capacitance (LowCap)                           
#   Cf   = the fringe capacitances (FringeCap)                            
#                                                                          
# Corrections to the propagation #constant (because of solder mask have     
# been added based on emperical data from GS2 boards.  The correction      
# factor was derived similar to the techinique in "Characteristics of      
# Microstrip Transmission Lines", by H. R. Kaupp.                          
#                                                                          
# Please keep in mind that the same equations used in this def are
#   also contained in MicroStripStatAnal.                                    
#**************************************************************************

#var
#   Cap, Induct : real
#   Again: boolean
#   temp : char
    
    global SoldMask
    Again = True
    while Again == True :
        clear_textwindow(text)
        text.insert('1.0', 'Micro-stripline analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()        
        while True :
            temp = gui_input_string(400, 'Solder mask? (w-wet, d-dry, n-none) ', SoldMask)
            if (temp == 'n') or (temp == 'w') or (temp == 'd') or (temp == ''): break
        if temp == "" : temp = 'n'
        if (temp != '') : 
            SoldMask = temp
            if SoldMask == 'n' : EffDiConst = 0.475*DiConst + 0.67
            elif SoldMask == 'w' : EffDiConst = 0.58*DiConst + 0.55
            elif SoldMask == 'd' : EffDiConst = DiConst
        LowCap, UpCap, FringeCap = LineCap(TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst)
        IntProp = PropConst(LowCap, UpCap, UpCap, FringeCap, FringeCap, DiConst, EffDiConst)
        IntImped = LineImped(IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap)
        Cap = (2*(UpCap + FringeCap) + LowCap)/12
        Induct = IntProp * IntImped/12
        Resist = ResistCopper/(TraceThick * TraceWidth)*1000
        LineAnalOut(text, IntImped, IntProp, Cap, Induct, Resist)
        input = gui_input(300, 'Another micro-stripline analysis (y/n)?',0)
        if (input == 'n') or (input =='N') : Again = False
        if (Again == False) : break

        
#************************************************************************
def MicroStripStatAnal(text):
#                                                                          
# Calculates the line impedance of a microstrip trace using the model      
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs" for an isolated conductor. He breaks the line        
# capacitance up into:                                                     
#                                                                          
#   Cppu = the upper plate capacitance (UpCap)                            
#   Cpp  = the lower plate capacitance (LowCap)                           
#   Cf   = the fringe capacitances (FringeCap)                            
#                                                                          
# Corrections to the propagation #constant (because of solder mask have     
# been added based on emperical data from GS2 boards.  The correction      
# factor was derived similar to the techinique in "Characteristics of      
# Microstrip Transmission Lines", by H. R. Kaupp.                          
#                                                                          
#  Containes the same equations as MicroStripAnal, however this routine
#    is controlled by some statistics code.
#    For comments on program statements, please refer to StripLineStatAnal,
#    which is structured similarly                                           
#**************************************************************************

#var
#   Cap,CapMean,CapSigma, Induct,InductMean,InductSigma,
#   ResistMean,ResistSigma : real
#   i : integer
#   Again : boolean
#   temp : char

    global TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst, NumIterations, IterationsMax, ResistCopper, SoldMask
    Again = True
    while Again == True :
        clear_textwindow(text)
        text.insert('1.0', 'S t a t i s t i c a l    Microstrip Line Analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(INSERT, '\n')
        NumIterations = StatIterNum(NumIterations)
            
        StatData = [[0 for x in range(NumIterations+2)] for y in range(6)]      
     
        TraceThickMean, TraceThickSigma, TraceWidthMean, TraceWidthSigma,  \
        TraceHeightMean, TraceHeightSigma, DiConstMean, DiConstSigma = GetTraceStatParam()       
        while True :
            temp = gui_input_string(400, 'Solder mask? (w-wet, d-dry, n-none) ', SoldMask)
            if (temp == 'n') or (temp == 'w') or (temp == 'd') or (temp == ''): break
        if temp == "" : temp = 'n'
        if (temp != '') : 
            SoldMask = temp
        TraceThickVal = TraceThick
        TraceWidthVal = TraceWidth
        TraceHeightVal = TraceHeight
        DiConstVal = DiConst
        EffDiConstVal = EffDiConst
        text.insert(END, '\n')
        text.insert(INSERT, 'Working')
        for i in range(1,  NumIterations +1) :
            TraceThickVal = RNDNormal(TraceThickMean,TraceThickSigma)
            TraceWidthVal = RNDNormal(TraceWidthMean,TraceWidthSigma)
            TraceHeightVal = RNDNormal(TraceHeightMean,TraceHeightSigma)
            DiConstVal = RNDNormal(DiConstMean,DiConstSigma)            
            if SoldMask == 'n' : EffDiConstVal = 0.475*DiConstVal + 0.67
            elif SoldMask == 'w' : EffDiConstVal = 0.58*DiConstVal + 0.55
            elif SoldMask == 'd' : EffDiConstVal = DiConstVal
                   
            LowCap, UpCap, FringeCap = LineCap(TraceThickVal, TraceWidthVal, TraceHeightVal, DiConstVal, EffDiConstVal)
            IntProp = PropConst (LowCap, UpCap, UpCap, FringeCap, FringeCap, DiConstVal, EffDiConstVal)
            IntImped = LineImped (IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap)
            Cap = (2*(UpCap + FringeCap) + LowCap)/12
            Induct = IntProp * IntImped/12
            Resist = ResistCopper/(TraceThickVal * TraceWidthVal)*1000

            StatData[1][i] = IntImped
            StatData[2][i] = IntProp
            StatData[3][i] = Cap
            StatData[4][i] = Induct
            StatData[5][i] = Resist

        TraceThick = TraceThickVal
        TraceWidth = TraceWidthVal
        TraceHeight = TraceHeightVal    
        DiConst = DiConstVal
        EffDiConst = EffDiConstVal

        IntImpedMean = 0
        IntPropMean = 0
        CapMean = 0
        InductMean = 0
        ResistMean = 0
        for i in range(1,  NumIterations + 1) : 
            IntImpedMean = IntImpedMean + StatData[1][i]
            IntPropMean = IntPropMean + StatData[2][i]
            CapMean = CapMean + StatData[3][i]
            InductMean = InductMean + StatData[4][i]
            ResistMean = ResistMean + StatData[5][i]

        IntImpedMean = IntImpedMean / NumIterations
        IntPropMean = IntPropMean / NumIterations
        CapMean = CapMean/ NumIterations
        InductMean = InductMean / NumIterations
        ResistMean = ResistMean / NumIterations

        IntImpedSigma = 0
        IntPropSigma = 0
        CapSigma = 0
        InductSigma = 0
        ResistSigma = 0
        for i in range(1,  NumIterations + 1) :
            IntImpedSigma = IntImpedSigma + math.pow(StatData[1][i]-IntImpedMean,2)
            IntPropSigma = IntPropSigma + math.pow(StatData[2][i]-IntPropMean,2)
            CapSigma = CapSigma + math.pow(StatData[3][i]-CapMean,2)
            InductSigma = InductSigma + math.pow(StatData[4][i]-InductMean,2)
            ResistSigma = ResistSigma + math.pow(StatData[5][i]-ResistMean,2)

        IntImpedSigma = math.sqrt(IntImpedSigma / (NumIterations-1))
        IntPropSigma = math.sqrt(IntPropSigma / (NumIterations-1))
        CapSigma = math.sqrt(CapSigma/ (NumIterations-1))
        InductSigma = math.sqrt(InductSigma / (NumIterations-1))
        ResistSigma = math.sqrt(ResistSigma / (NumIterations-1))

        LineAnalStatOut(text, IntImpedMean,IntImpedSigma, IntPropMean,IntPropSigma, \
            CapMean,CapSigma, InductMean,InductSigma, ResistMean,ResistSigma)
        input = gui_input(300, 'Another statistical stripline analysis (y/n)?',0)
        if (input == 'n') or (input =='N') : Again = False  
        if (Again == False) : break


       
