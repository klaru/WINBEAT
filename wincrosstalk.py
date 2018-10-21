#! python3
import os, sys
from tkinter import *
from beatinc import *
from beatcalc import *
from winbeatio import *

#**************************************************************************
def CrossTalk(text):
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
    global DiConst, TraceThick, TraceWidth, TraceHeight, TraceSpacing, DistCap, LoadImp, EvenLineImp, OddLineImp, EvenIntProp, OddIntProp
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
        clear_textwindow(text)
        text.insert('1.0', 'Crosstalk Analysis')
        text.insert(END, '\n')
        text.insert(INSERT, '-----------------------------------------------------------')
        text.insert(END, '\n')
        TraceParamOut
        Update = False
        input = gui_input(300, 'New trace parameters (y/n)? ', 0)
        if (input == 'y') or (input =='Y') : Update = True       
        if Update == True :
        #begin
            TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()
            # Adjust the dielectric #constant for solder mask 
            SoldMask = gui_input(300, 'Solder mask? (w-wet, d-dry, n-none) ', 0)
            if SoldMask == 'n' : 
                EffDiConst = 0.475*DiConst + 0.67
            elif SoldMask == 'w' : 
                EffDiConst = 0.58*DiConst + 0.55
            elif SoldMask == 'd' : 
                EffDiConst = DiConst
            #end
        #end
        # Request data essential for crosstalk analysis 
        TraceSpacing = GetParam('Trace spacing from edge to edge ?  ', TraceSpacing)
        TraceLength = GetParam('Trace length ?  ', TraceLength)
        DistCap = GetParam('What is the distributed cap.?  ', DistCap)
        RiseTime = GetParam('Signal Rise time ?  ', RiseTime)
        VoltStep = GetParam('Voltage step ?  ', VoltStep)
        LoadImp = GetParam('What is the load impedance ? ', LoadImp)
        IntGnd = gui_input(300, 'Interlaced grounds (y/n)? ', 0)
        BusStruct = gui_input(300, 'Bus Structure (y/n)? ', 0)
        # For a bus structure 
        if BusStruct == True :
            #begin
            # Request the number of active lines 
            Actlines = gui_input(400, 'Number of active lines (1,2,4,6)? ', '%1d' %(ActLines))
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
        clear_textwindow(text)
        text.insert('1.0', 'Test Parameters')
        text.insert(END, '\n')        
        text.insert(INSERT, '-------------------------')
        text.insert(END, '\n')        
        text.insert(INSERT, 'RiseTime:      ')
        text.insert(INSERT, '%3.2F' %(RiseTime))
        text.insert(INSERT, ' ns')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Voltage Step:  ')
        text.insert(INSERT, '%4.2f' %(VoltStep))
        text.insert(INSERT, ' v')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Dist. Cap.:    ')
        text.insert(INSERT, '%4.2f' %(DistCap))
        text.insert(INSERT, ' pf/in')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Trace Length:  ')
        text.insert(INSERT, '%4.2f' %(TraceLength))
        if IntGnd == True :
            text.insert(INSERT, 'Interlaced grounds')
        text.insert(END, '\n')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Crosstalk Data')
        text.insert(END, '\n')        
        text.insert(INSERT, '-------------------------')
        text.insert(END, '\n')        
        text.insert(INSERT, 'Backward Crosstalk Constant:    ')
        text.insert(INSERT, '%4.3f' %(BackCrossConst))
        text.insert(END, '\n')
        text.insert(INSERT, 'Backward Crosstalk Voltage:     ')
        text.insert(INSERT, '%4.3f' %(BackVolt))
        text.insert(INSERT, ' v')
        text.insert(END, '\n')
        text.insert(INSERT, 'Backward Crosstalk Pulse Width: ')
        text.insert(INSERT, '%4.3f' %(BackPulWid))
        text.insert(INSERT, ' ns')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Forward Crosstalk Constant:     ')
        text.insert(INSERT, '%4.3f' %(ForCrossConst))
        text.insert(INSERT, ' ns/ft')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Forward Crosstalk Voltage:      ')
        text.insert(INSERT, '%4.3f' %(ForVolt))
        text.insert(INSERT, ' v')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Forward Crosstalk Pulse Width:  ')
        text.insert(INSERT, '%4.3f' %(ForPulWid))
        text.insert(INSERT, ' ns')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Even Line Impedance:            ')
        text.insert(INSERT, '%4.2f' %(EvenLineImp))
        text.insert(INSERT, ' ohms')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Odd Line Impedance:             ')
        text.insert(INSERT, '%4.2f' %(OddLineImp))
        text.insert(INSERT, ' ohms')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Even Prop Const:                ')
        text.insert(INSERT, '%4.3f' %(EvenIntProp))
        text.insert(INSERT, ' ns/ft')
        text.insert(END, '\n')		
        text.insert(INSERT, 'Odd Prop Const:                 ')
        text.insert(INSERT, '%4.3f' %(OddIntProp))
        text.insert(INSERT, ' ns/ft')
        text.insert(END, '\n')
        
        input = gui_input(300, 'Another crosstalk analysis? (y/n)', 0)
        if (input == 'n') or (input =='N') : Again = False   
        if Again == False : break
   #end
#end  Crosstalk 
