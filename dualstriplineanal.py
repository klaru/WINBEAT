#! python3
import os, sys, math
from beatinc import *
from beatio import *
from beatcalc import *

#**************************************************************************
def DualStripAnal(text):
#                                                                          
# Determines the impedance and propagation #constant of dual-stripline      
# using the equation found the IPC Standard "Design standard for electronic
# packaging utilizing high speed techniques".                              
#                                                                          
# Please keep in mind that the same equations used in this def are
#   also contained in DualStripStatAnal.                                     
#**************************************************************************

#var
#   Cap, Induct,
#   ImpFactor1,ImpFactor2, ImpFactor3 : real
#   Again : boolean

    global SigPlaneSep
    Again = True
    while Again == True :
        clear_textwindow(text)
        text.insert('1.0', 'Dual-stripline analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()        
        SigPlaneSep = GetParam('What is the signal plane separation? ',SigPlaneSep)
        ImpFactor1 = 80/math.sqrt(DiConst)
        ImpFactor2 = math.log(1.9*(2*TraceHeight + TraceThick)/(0.8*TraceWidth + TraceThick))
        ImpFactor3 = 1 - (TraceHeight/(4*(TraceHeight + SigPlaneSep + TraceThick)))
        IntImped = ImpFactor1 * ImpFactor2 * ImpFactor3
        IntProp = 1.017*math.sqrt(DiConst)
        Cap = IntProp/IntImped*1e3/12
        Induct = IntProp * IntImped/12
        Resist = ResistCopper/(TraceThick * TraceWidth)*1000
        LineAnalOut(text, IntImped, IntProp, Cap, Induct, Resist)
        input = gui_input(300, 'Another dual-stripline analysis (y/n)?',0)
        if (input == 'n') or (input =='N') : Again = False        
        if (Again == False) : break


#************************************************************************
def DualStripStatAnal(text):
#                                                                          
# Determines the impedance and propagation #constant of dual-stripline      
# using the equation found the IPC Standard "Design standard for electronic
# packaging utilizing high speed techniques".                              
#                                                                          
#  Containes the same equations as DualStripAnal, however this routine
#    is controlled by some statistics code.
#    For comments on program statements, please refer to StripLineStatAnal,
#    which is structured similarly                                           
#**************************************************************************

#var
#   Cap,CapMean,CapSigma, Induct,InductMean,InductSigma,
#   ResistMean,ResistSigma,
#   ImpFactor1,ImpFactor2, ImpFactor3 : real
#   i : integer
#   Again : boolean

    global NumIterations, IterationsMax, ResistCopper, SigPlaneSep, SigPlaneSepSigma
    Again = True
    while Again == True :
        clear_textwindow(text)
        text.insert('1.0', 'S t a t i s t i c a l    Dual-strip Line Analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        NumIterations = StatIterNum(NumIterations)
            
        StatData = [[0 for x in range(NumIterations+2)] for y in range(6)]         

        TraceThickMean, TraceThickSigma, TraceWidthMean, TraceWidthSigma,  \
        TraceHeightMean, TraceHeightSigma, DiConstMean, DiConstSigma = GetTraceStatParam()
        SigPlaneSepMean = SigPlaneSep  # Get default value 
        SigPlaneSepMean = GetParam('What is the mean signal plane separation? ',SigPlaneSepMean)
        SigPlaneSepSigma = GetParam('What is the standard deviation? ',SigPlaneSepSigma)
        SigPlaneSep = SigPlaneSepMean  # Keep as default value 
        text.insert(END, '\n')
        text.insert(INSERT, 'Working')

        for i in range(1,  NumIterations + 1) : 
            TraceThickVal = RNDNormal(TraceThickMean,TraceThickSigma)
            TraceWidthVal = RNDNormal(TraceWidthMean,TraceWidthSigma)
            TraceHeightVal = RNDNormal(TraceHeightMean,TraceHeightSigma)
            DiConstVal = RNDNormal(DiConstMean,DiConstSigma)
            SigPlaneSepVal = RNDNormal(SigPlaneSepMean,SigPlaneSepSigma)

            ImpFactor1 = 80/math.sqrt(DiConstVal)
            ImpFactor2 = math.log(1.9*(2*TraceHeightVal + TraceThickVal)/(0.8*TraceWidthVal + TraceThickVal))
            ImpFactor3 = 1 - (TraceHeightVal/(4*(TraceHeightVal + SigPlaneSepVal + TraceThickVal)))
            IntImped = ImpFactor1 * ImpFactor2 * ImpFactor3
            IntProp = 1.017*math.sqrt(DiConstVal)
            Cap = IntProp/IntImped*1e3/12
            Induct = (IntProp * IntImped)/12
            Resist = ResistCopper/(TraceThickVal * TraceWidthVal)*1000

            StatData[1][i] = IntImped
            StatData[2][i] = IntProp
            StatData[3][i] = Cap
            StatData[4][i] = Induct
            StatData[5][i] = Resist

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
        input = gui_input(400, 'Another statistical stripline analysis (y/n)?',0)
        if (input == 'n') or (input =='N') : Again = False        
        if (Again == False) : break


