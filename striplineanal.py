#! python3
import os, sys
from beatinc import *
from beatio import *
from beatcalc import *

#****************************************************************************
def StripLineAnal() :
#                                                                          
# Determines the impedance and propagation constant of a stripline         
# using the standard equation found in Motorola's MECL Handbook or a       
# hundred other books.                                                     
#                                                                          
# Please keep in mind that the same equations used in this procedure are
#also contained in StripLineStatAnal.                                     
#****************************************************************************
#var
#   Cap, Induct,
#   PlaneSpace,
#   ImpFactor1,ImpFactor2 : real;
#   Again : boolean;
	
    Again = True
    while Again == True :
        os.system('cls')
        print('Stripline analysis')
        print('-----------------------------------------------------------')
        print('\n')
        TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()
        PlaneSpace = 2*TraceHeight + TraceThick
        ImpFactor1 = 60/math.sqrt(DiConst)
        ImpFactor2 = math.log(4*PlaneSpace/(0.67*pi*TraceWidth*(0.8 + TraceThick/TraceWidth)))
        IntImped = ImpFactor1 * ImpFactor2      
        IntProp = 1.017*math.sqrt(DiConst)
        Cap = IntProp/IntImped * 1e3/12
        Induct = IntProp * IntImped/12
        Resist = ResistCopper/(TraceThick * TraceWidth)*1000
        LineAnalOut(IntImped, IntProp, Cap, Induct, Resist)
        Again = GetResponse('Another stripline analysis (y/n)?','n')
        if (Again == False) : break
     #end while
#end StripLineAnal

#************************************************************************
def StripLineStatAnal() :
#                                                                          
# Determines the impedance and propagation #constant of a stripline         
# using the standard equation found in Motorola's MECL Handbook or a       
# hundred other books.                                                     
#                                                                          
# Containes the same equations as StripLineAnal, however this routine
#   is controlled by some statistics code.                                   
#**************************************************************************

#var
#   Cap,CapMean,CapSigma,Induct,InductMean,InductSigma,
#   ResistMean,ResistSigma,
#   PlaneSpace,
#   ImpFactor1,ImpFactor2 : real
#   i : integer
#   Again : boolean

#begin 
    global NumIterations, IterationsMax, ResistCopper
    Again = True
    answer = ''
    while Again == True :
    #begin
        os.system('cls')
        print('S t a t i s t i c a l    Strip Line Analysis')
        print('-----------------------------------------------------------')
        print('\n')
        NumIterations = StatIterNum(NumIterations)
            
        StatData = [[0 for x in range(NumIterations+2)] for y in range(6)] 
        
        TraceThickMean, TraceThickSigma, TraceWidthMean, TraceWidthSigma,  \
        TraceHeightMean, TraceHeightSigma, DiConstMean, DiConstSigma = GetTraceStatParam()    
        print('\n')
        print('Working')

        for i in range(1, NumIterations + 1) :                          #begin for  Main Loop 
            TraceThickVal = RNDNormal(TraceThickMean,TraceThickSigma)   #Get 
            TraceWidthVal = RNDNormal(TraceWidthMean,TraceWidthSigma)   #Value
            TraceHeightVal = RNDNormal(TraceHeightMean,TraceHeightSigma)#for
            DiConstVal = RNDNormal(DiConstMean,DiConstSigma)            #each parameter

            PlaneSpace = 2*TraceHeightVal + TraceThickVal               #calculate output
            ImpFactor1 = 60/math.sqrt(DiConstVal)                       #for these input data 
            ImpFactor2 = math.log(4*PlaneSpace/(0.67*pi*TraceWidthVal*(0.8 + TraceThickVal/TraceWidthVal)))
            IntImped = ImpFactor1 * ImpFactor2
            IntProp = 1.017*math.sqrt(DiConstVal)
            Cap = IntProp/IntImped*1e3/12
            Induct = IntProp * IntImped/12
            Resist = ResistCopper/(TraceThickVal * TraceWidthVal)*1000

            StatData[1][i] = IntImped                                   # store resulting data 
            StatData[2][i] = IntProp
            StatData[3][i] = Cap
            StatData[4][i] = Induct
            StatData[5][i] = Resist
        #end for   Main Loop 

        IntImpedMean = 0  # initialize #variables to determine mean value 
        IntPropMean = 0   # of each output parameter 
        CapMean = 0
        InductMean = 0
        ResistMean = 0
        for i in range(1, NumIterations + 1) :             
            IntImpedMean = IntImpedMean + StatData[1][i]
            IntPropMean = IntPropMean + StatData[2][i]
            CapMean = CapMean + StatData[3][i]
            InductMean = InductMean + StatData[4][i]
            ResistMean = ResistMean + StatData[5][i]
        #end for
        IntImpedMean = IntImpedMean / NumIterations
        IntPropMean = IntPropMean / NumIterations
        CapMean = CapMean/ NumIterations
        InductMean = InductMean / NumIterations
        ResistMean = ResistMean / NumIterations

        IntImpedSigma = 0                                                 # initialize #variables for determining 
        IntPropSigma = 0                                                  # standard deviation for each output parameter 
        CapSigma = 0
        InductSigma = 0
        ResistSigma = 0
        for i in range(1, NumIterations + 1) :                               #begin determine standard deviation 
            IntImpedSigma = IntImpedSigma + math.pow(StatData[1][i]-IntImpedMean,2)
            IntPropSigma = IntPropSigma + math.pow(StatData[2][i]-IntPropMean,2)
            CapSigma = CapSigma + math.pow(StatData[3][i]-CapMean,2)
            InductSigma = InductSigma + math.pow(StatData[4][i]-InductMean,2)
            ResistSigma = ResistSigma + math.pow(StatData[5][i]-ResistMean,2)
        #end for
        IntImpedSigma = math.sqrt(IntImpedSigma / (NumIterations-1))
        IntPropSigma = math.sqrt(IntPropSigma / (NumIterations-1))
        CapSigma = math.sqrt(CapSigma/ (NumIterations-1))
        InductSigma = math.sqrt(InductSigma / (NumIterations-1))
        ResistSigma = math.sqrt(ResistSigma / (NumIterations-1))
        LineAnalStatOut(IntImpedMean,IntImpedSigma, IntPropMean,IntPropSigma, \
          CapMean,CapSigma, InductMean,InductSigma, ResistMean,ResistSigma)

        Again = GetResponse('Another statistical stripline analysis (y/n)?','n')
        if (Again == False) : break      
    #end while
#end  StripLineStatAnal 