#! python3
import os, sys
from beatinc import *
from beatio import *
from beatcalc import *
from tkinter import *

#**************************************************************************
def EmbeddedMicroStripAnal(text):
#                                                                          
# Calculates the line impedance of an embedded microstrip trace by calculating
# first the impedance of  the microstripline case and then adjusting for the
# higher effective impedance of the embedded case                        
#                                                                          
# Please keep in mind that the same equations used in this def are
#   also contained in MicroStripStatAnal.                                    
#**************************************************************************

#var
#   Cap, Induct : real
#   Again: boolean
#   temp : char
    
    global EmbedHeight
    Again = True
    while Again == True :
        clear_textwindow(text)
        text.insert('1.0', 'Embedded micro-stripline analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()   
        EmbedHeight = GetParam('What is the dielectrical height above the bottom of the trace? ', EmbedHeight)
        EffDiConst = DiConst
        LowCap, UpCap, FringeCap = LineCap(TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst)
        IntProp = PropConst(LowCap, UpCap, UpCap, FringeCap, FringeCap, DiConst, EffDiConst)
        IntImped = LineImped(IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap)
        EffDiConstmicro = IntProp*1e9*IntProp*1e9/(SpeedOfLight*SpeedOfLight)
        EffDiConstburied = EffDiConstmicro*math.exp(-2*EmbedHeight/TraceHeight) + DiConst*(1 - math.exp(-2*EmbedHeight/TraceHeight))
        LowCap, UpCap, FringeCap = LineCap(TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConstburied)
        IntPropEmbed = PropConst(LowCap, UpCap, UpCap, FringeCap, FringeCap, DiConst, EffDiConstburied)
        IntImpedEmbed = IntImped*math.sqrt(EffDiConstmicro)/math.sqrt(EffDiConstburied)
        Cap = (2*(UpCap + FringeCap) + LowCap)/12
        Induct = IntPropEmbed * IntImpedEmbed/12
        Resist = ResistCopper/(TraceThick * TraceWidth)*1000
        LineAnalOut(text, IntImpedEmbed, IntPropEmbed, Cap, Induct, Resist)
        input = gui_input(400, 'Another micro-stripline analysis (y/n)?', 0)
        if (input == 'n') or (input =='N') : Again = False       
        if (Again == False) : break

        
#************************************************************************
def EmbedMicroStripStatAnal(text):
#                                                                          
#  Calculates the line impedance of an embedded microstrip trace by calculating
#  first the impedance of  the microstripline case and then adjusting for the
#  higher effective impedance of the embedded case                         
#                                                                          
#  Containes the same equations as MicroStripAnal, however this routine
#  is controlled by some statistics code.
#  For comments on program statements, please refer to StripLineStatAnal,
#  which is structured similarly                                           
#**************************************************************************

#var
#   Cap,CapMean,CapSigma, Induct,InductMean,InductSigma,
#   ResistMean,ResistSigma : real
#   i : integer
#   Again : boolean
#   temp : char

    global TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst, NumIterations, IterationsMax, ResistCopper, EmbedHeight, EmbedHeightSigma
    Again = True
    while Again == True :
        clear_textwindow(text)
        text.insert('1.0', 'S t a t i s t i c a l    Embedded microstripline Analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        NumIterations = StatIterNum(NumIterations)
            
        StatData = [[0 for x in range(NumIterations+2)] for y in range(6)]      
     
        TraceThickMean, TraceThickSigma, TraceWidthMean, TraceWidthSigma,  \
        TraceHeightMean, TraceHeightSigma, DiConstMean, DiConstSigma = GetTraceStatParam()
        EmbedHeightMean = EmbedHeight  # Get default value 
        EmbedHeightMean = GetParam('What is the dielectrical height above the bottom of the trace? ', EmbedHeightMean)
        EmbedHeightSigma = GetParam('What is the standard deviation for dielectric height above? ', EmbedHeightSigma)
        EmbedHeight = EmbedHeightMean  # Keep as default value 
        
        TraceThickVal = TraceThick
        TraceWidthVal = TraceWidth
        TraceHeightVal = TraceHeight
        DiConstVal = DiConst
        EffDiConstVal = EffDiConst
        for i in range(1,  NumIterations +1) :
            TraceThickVal = RNDNormal(TraceThickMean,TraceThickSigma)
            TraceWidthVal = RNDNormal(TraceWidthMean,TraceWidthSigma)
            TraceHeightVal = RNDNormal(TraceHeightMean,TraceHeightSigma)
            DiConstVal = RNDNormal(DiConstMean,DiConstSigma)   
            EffDiConstVal = DiConstVal            
                   
            LowCap, UpCap, FringeCap = LineCap(TraceThickVal, TraceWidthVal, TraceHeightVal, DiConstVal, EffDiConstVal)
            IntProp = PropConst (LowCap, UpCap, UpCap, FringeCap, FringeCap, DiConstVal, EffDiConstVal)
            IntImped = LineImped (IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap)
            EffDiConstmicro = IntProp*1e9*IntProp*1e9/(SpeedOfLight*SpeedOfLight)
            EffDiConstburied = EffDiConstmicro*math.exp(-2*EmbedHeight/TraceHeight) + DiConst*(1 - math.exp(-2*EmbedHeight/TraceHeight))
            LowCap, UpCap, FringeCap = LineCap(TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConstburied)
            IntPropEmbed = PropConst(LowCap, UpCap, UpCap, FringeCap, FringeCap, DiConst, EffDiConstburied)
            IntImpedEmbed = IntImped*math.sqrt(EffDiConstmicro)/math.sqrt(EffDiConstburied)            
            Cap = (2*(UpCap + FringeCap) + LowCap)/12
            Induct = IntPropEmbed * IntImpedEmbed/12
            Resist = ResistCopper/(TraceThickVal * TraceWidthVal)*1000

            StatData[1][i] = IntImpedEmbed
            StatData[2][i] = IntPropEmbed
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
        input = gui_input(400, 'Another statistical embedded microstripline analysis (y/n)?', 0)
        if (input == 'n') or (input =='N') : Again = False        
        if (Again == False) : break


       