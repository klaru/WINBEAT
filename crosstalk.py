#! python3
import os, sys
from beatinc import *
from beatio import *
from beatcalc import *

#**************************************************************************
def CrossTalk():
#                                                                          
# This def calculates the backward and forward crosstalk for         
# microstrip.  It allows for bus structures, distributed capacitance,      
# termination values, different solder mask, and interlaced grounds.       
#                                                                          
# Several papers were used to derive the crosstalk calculation algorithms  
# used in this def.  First, the microstrip characteristics are for   
# even and odd modes are determined using the models defined by Schwarzmann
# in his paper "Microstrip plus equations adds up to fast designs".        
# Second, papers by Ivor Catt, "Crosstalk in Digital Systems" and John     
# Defalco were used for basic crosstalk theory and crosstalk reflection    
# analysis.  Data in these papers were also used for verification of the   
# single line to line crosstalk.  Extrapolations to multiple lines and     
# ground interlacing were primarily intuitive derviations and have been    
# verified against GS2 processor board and backplane data.                 
#                                                                          
# Corrections to the propagation #constant (because of solder mask have     
# been added based on emperical data from GS2 boards.  The correction      
# factor was derived similar to the techinique in "Characteristics of      
# Microstrip Transmission Lines", by H. R. Kaupp.                          
#                                                                          
#**************************************************************************

#var
#   TraceSpace,
#   RiseTime,
#   VoltStep,
#   BackVolt,
#   ForVolt,
#   BackPulWid,
#   ForPulWid,
#   VoltOdd,
#   FCrC,
#   BCrC : extended
#   Count,
#   CountLimit,
#   ActLines : integer
#   BusStruct,
#   Update,
#   Again,IntGnd : boolean
#   SoldMask : char
    global DiConst, TraceSpacing, DistCap, LoadImp, EvenLineImp, OddLineImp, EvenIntProp, OddIntProp
#begin
    Again = True
    VoltStep = 3.0               #v
    RiseTime = 2.8               #ns
    TraceLength = 10.0           #in
    while Again == True :
    #begin
        IntGnd = False
        BusStruct = False
        ActLines = 1
        BCrC = 0
        FCrC = 0
        BackCrossConst = 0
        ForCrossConst = 0
        BackVolt = 0
        ForVolt = 0
        VoltOdd = 0
        SoldMask = 'w'
        EffDiConst = 0.58*DiConst + 0.55 # Set for wet solder mask 
        os.system('cls')
        print ('Crosstalk Analysis')
        print ('-----------------------------------------------------------')
        print('\n')
        TraceParamOut
        Update = GetResponse ('New trace parameters (y/n)? ', 'y' )
        if Update == True :
        #begin
            TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()
            # Adjust the dielectric #constant for solder mask 
            print('Solder mask? (w-wet, d-dry, n-none) ', end='')
            SoldMask = input()
            if SoldMask == 'n' : 
                EffDiConst = 0.475*DiConst + 0.67
            elif SoldMask == 'w' : 
                EffDiConst = 0.58*DiConst + 0.55
            elif SoldMask == 'd' : 
                EffDiConst = DiConst
            #end
        #end
        # Request data essential for crosstalk analysis 
        TraceSpacing = GetParam('Trace spacing from edge to edge ?',1, TraceSpacing)
        TraceLength = GetParam('Trace length ?',1, TraceLength)
        DistCap = GetParam('What is the distributed cap.?',3, DistCap)
        RiseTime = GetParam('Signal Rise time ?',4, RiseTime)
        VoltStep = GetParam('Voltage step ?',5, VoltStep)
        LoadImp = GetParam('What is the load impedance ? ',2, LoadImp)
        IntGnd = GetResponse('Interlaced grounds (y/n)? ', 'n')
        BusStruct = GetResponse('Bus Structure (y/n)? ', 'n')
        # For a bus structure 
        if BusStruct == True :
            #begin
            # Request the number of active lines 
            print('\n')
            print('Number of active lines (1,2,4,6)? ', '[ %1d' %(ActLines),' ]', end='')
            Actlines = input()
            if (IntGnd == True) or (ActLines == 1) :
                CountLimit = 1
            else:
                CountLimit = ActLines // 2
            # For the number of active lines divided by two, interatively add 
            # up the crosstalk #constants                                     
            for Count in range(CountLimit, 0, -1) :
            #begin
                TraceSpace = TraceSpacing
                TraceSpacing = Count*TraceSpacing + (Count-1)*TraceWidth
                LowCap, UpCap, FringeCap = LineCap( TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst)
                EvenUpCap, EvenFringeCap = EvenLineCap(TraceWidth, TraceSpacing, UpCap, FringeCap)
                OddUpCap, OddFringeCap = OddLineCap(TraceThick, TraceWidth, TraceHeight, TraceSpacing, DiConst, EffDiConst)
                EvenIntProp = PropConst(LowCap, EvenUpCap, EvenUpCap, EvenFringeCap, EvenFringeCap, DiConst, EffDiConst)
                OddIntProp = PropConst(LowCap, OddUpCap, OddUpCap, OddFringeCap, OddFringeCap, DiConst, EffDiConst)                
                EvenLineImp = LineImped(EvenIntProp, LowCap, EvenUpCap, EvenUpCap, EvenFringeCap, EvenFringeCap)
                OddLineImp = LineImped(OddIntProp, LowCap, OddUpCap, OddUpCap, OddFringeCap, OddFringeCap)
                BCrC = (EvenLineImp - OddLineImp) / (EvenLineImp + OddLineImp)
                if BCrC >= 0 :
                    BackCrossConst = BackCrossConst + BCrC
                FCrC = (EvenIntProp - OddIntProp)
                if FCrC >= 0 :
                    ForCrossConst = ForCrossConst + FCrC
                TraceSpacing = TraceSpace
            #end  Loop 
            # If bus structure and interlaced grounds : iteratively add 
            # the squares of the backward #constants and divide the odd mode
            # voltage by 2                                                 
            if IntGnd == True :
               #begin
               # Adjust backward #constant for a single adjacent bus trace  
                BCrC = BackCrossConst/2
                BackCrossConst = 0
                if ActLines >= 2 :
                    CountLimit = ActLines // 2
                for Count in range(CountLimit, 0, -1) :
                #begin
                    BCrC = math.pow(BCrC,2)
                    BackCrossConst = BackCrossConst + BCrC
                    VoltOdd = VoltOdd/4 + VoltStep/4
                #end
                # Correct for bus symmetry 
                BackCrossConst = BackCrossConst*2
                #end
            else: # if no interlaced ground 
                VoltOdd = VoltStep/2
            if ActLines == 1 : # Correct for no bus symmetry 
                BackCrossConst = BackCrossConst/2
         #end Bustruct == True 
        else: # BusStruct == False 
        #begin
            LowCap, UpCap, FringeCap = LineCap( TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst)
            EvenUpCap, EvenFringeCap = EvenLineCap(TraceWidth, TraceSpacing, UpCap, FringeCap)
            OddUpCap, OddFringeCap = OddLineCap(TraceThick, TraceWidth, TraceHeight, TraceSpacing, DiConst, EffDiConst)
            EvenIntProp = PropConst(LowCap, UpCap, EvenUpCap, FringeCap, EvenFringeCap, DiConst, EffDiConst)           
            OddIntProp = PropConst(LowCap, UpCap, OddUpCap, FringeCap, OddFringeCap, DiConst, EffDiConst)         
            EvenLineImp = LineImped(EvenIntProp, LowCap, UpCap, EvenUpCap, FringeCap, EvenFringeCap)
            OddLineImp = LineImped(OddIntProp, LowCap, UpCap, OddUpCap, FringeCap, OddFringeCap)
            BackCrossConst = (EvenLineImp - OddLineImp) / (EvenLineImp + OddLineImp)
            ForCrossConst = (EvenIntProp - OddIntProp)
# If not bus structure but interlaced ground 
            if IntGnd == True :
            #begin
                BackCrossConst = math.pow(BackCrossConst,2)
                VoltOdd = VoltOdd/4 + VoltStep/4
            #end
            else:
                VoltOdd = VoltStep/2  # End interlaced ground 
        #end  BusStruct == False 
        # Determine the line impedance 
        LineImp = math.sqrt(EvenLineImp * OddLineImp)
        # Determine the max. backward crosstalk amplitude and pulse width 
        BackVolt = BackCrossConst*VoltStep
        BackPulWid = 2*EvenIntProp*TraceLength/12

        # Adjust the amplitude for the edge rate and trace length if needed 
        if  RiseTime > 2*(EvenIntProp*TraceLength/12) :
            BackVolt = BackVolt*(2*(EvenIntProp*TraceLength/12)/RiseTime)
        # Determine the forward crosstalk amplitude and pulse width 
        ForPulWid = RiseTime
        if (ForCrossConst*TraceLength/12) > RiseTime :
            ForVolt = VoltOdd
        else:
            ForVolt = ((TraceLength/12)*ForCrossConst*VoltOdd)/RiseTime
# Correct for termination mismatch 
        ReflectionCoef = (LoadImp - LineImp)/(LoadImp + LineImp)
        BackVolt = BackVolt * (1 + ReflectionCoef)
        ForVolt = ForVolt *  (1 + ReflectionCoef)
# Output the test conditions and results 
        os.system('cls')
        print('Test Parameters')
        print('-------------------------')
        print('RiseTime:      %3.2F' %(RiseTime),' ns')
        print('Voltage Step:  %4.2f' %(VoltStep),' v')
        print('Dist. Cap.:    %4.2f' %(DistCap),' pf/in')
        print('Trace Length:  %4.2f' %(TraceLength))
        if IntGnd == True :
            print( 'Interlaced grounds')
        print('\n')
        print('Crosstalk Data')
        print('-------------------------')
        print('Backward Crosstalk Constant:    %4.3f' %(BackCrossConst))
        print('Backward Crosstalk Voltage:     %4.3f' %(BackVolt),' v')
        print('Backward Crosstalk Pulse Width: %4.3f' %(BackPulWid),' ns')
        print('Forward Crosstalk Constant:     %4.3f' %(ForCrossConst),' ns/ft')
        print('Forward Crosstalk Voltage:      %4.3f' %(ForVolt),' v')
        print('Forward Crosstalk Pulse Width:  %4.3f' %(ForPulWid),' ns')
        print('Even Line Impedance:            %4.2f' %(EvenLineImp),' ohms')
        print('Odd Line Impedance:             %4.2f' %(OddLineImp),' ohms')
        print('Even Prop Const:                %4.3f' %(EvenIntProp),' ns/ft')
        print('Odd Prop Const:                 %4.3f' %(OddIntProp),' ns/ft')
        print('\n')
        GetResponse('Another crosstalk analysis? (y/n) ','y')
        if Again == False : break
   #end
#end  Crosstalk 
