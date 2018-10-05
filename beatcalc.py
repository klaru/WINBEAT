#! python3
import os, sys, math, random
from beatinc import *
from beatio import *
 
#procedure LineImped (var LineImp : extended; Prop,LowCap,UpCap1,UpCap2,FringeCap1,FringeCap2 : extended);
#procedure PropConst (var IntProp : extended; LowCap, UpCap1, UpCap2, FringeCap1, FringeCap2 : extended);
#procedure LinCap (var LowCap, UpCap, FringeCap : extended);
#procedure EvenLineCap ( var EvenUpCap, EvenFringeCap : extended);
#procedure OddLineCap ( var OddUpCap, OddFringeCap : extended);
#function LoadAdjust (IntCap, DistCap : extended) : extended;

#**************************************************************************
def RNDNormal(center, sigma) :
#
#    This routine uses the built-in random number generator (which generates
#    a uniform distribution between 0 and +1) and transforms this into
#    a normal distribution with parameters mean (center) and standard
#    deviation (sigma).
#    This routine was derived from a similar algorithm by D.E. Knuth in
#    "The Art of Computer Programming", volume 2, chapter 3.4.1,
#    algorithm P                                                           
#**************************************************************************
#var u1,u2,v1,v2,s : real;

    while True :
        u1 = random.random()
        u2 = random.random()
        v1 = 2*u1-1       # Shift distribution from 0 .. +1  to  -1 .. +1
        v2 = 2*u2-1
        s = v1*v1 + v2*v2
        if s < 1: break
    RNDNormal = v1 * math.sqrt((-2)*math.log(s)/s) * sigma + center
    return RNDNormal
#end RNDNormal


#***************************************************************************
def LineImped(Prop,LowCap,UpCap1,UpCap2,FringeCap1,FringeCap2) :
#                                                                         
# Calculates the line impedance of a microstrip trace using the model      
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs". He breaks the line capacitance up into:            
#                                                                          
#   Cppu := the upper plate capacitance (UpCap1 and UpCap2)                
#   Cpp  := the lower plate capacitance (LowCap)                           
#   Cf1  & Cf2 := the fringe capacitances (FringeCap1 & FringeCap2)        
#                                                                          
# The capacitance values passed depend on the presense of adjacent traces  
# such as bus structures or whether we are calculated the odd or even mode 
# impednaces.                                                              
#                                                                          
# The impedance is then equal to the propagation constant divided by the   
# total line capacitance (TotalCap).  The propagation constant passed      
# will be different for different line coatings and odd and even modes.    
#                                                                         
#****************************************************************************
#var
#   TotalCap : real;

    TotalCap = LowCap + FringeCap1 + FringeCap2 + UpCap1 + UpCap2
    LineImp = (Prop*1e-9) / (TotalCap*1e-12)
    return LineImp
#end LineImped

#****************************************************************************
def PropConst(LowCap, UpCap1, UpCap2, FringeCap1, FringeCap2, DiConst, EffDiConst) :
#                                                                          
# Calculates the propagation constant of a microstrip trace using the model
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs". He breaks the line capacitance up into:             
#                                                                          
#   Cppu := the upper plate capacitance (UpCap1 and UpCap2)                
#   Cpp  := the lower plate capacitance (LowCap)                           
#   Cf1  & Cf2 := the fringe capacitances (FringeCap1 & FringeCap2)        
#                                                                          
# The capacitance values passed depend on the presense of adjacent traces  
# such as bus structures or whether we are calculated the odd or even mode 
# impednaces.                                                              
#                                                                          
# The impedance is then equal to the propagation constant divided by the   
# total line capacitance (TotalCap).  The propagation constant passed      
# will be different for different line coatings and odd and even modes.    
#                                                                          
#****************************************************************************
#var
#   Cap,
#   VelSub,
#   VelConst : real;

    Cap = LowCap + FringeCap1 + FringeCap2 + UpCap1 + UpCap2
    VelSub = 1/(1 + ((FringeCap1 + FringeCap2)*(DiConst/EffDiConst - 1) + (UpCap1 + UpCap2)*(math.sqrt(DiConst) - 1))/Cap)
    VelConst = 1/math.sqrt(1 + math.pow(VelSub,2)*(DiConst -1))
    IntProp = 1/(SpeedOfLight * VelConst) * 1e9
    return IntProp
#end PropConst 


#***************************************************************************
def LineCap(TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst) :
#                                                                          
# Calculates the capacitances of a microstrip trace using the model        
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs" for an isolated conductor. He breaks the line        
# capacitance up into:                                                     
#                                                                          
#   Cppu := the upper plate capacitance                                    
#   Cpp  := the lower plate capacitance                                    
#   Cf   := the fringe capacitance                                         
#                                                                          
#***************************************************************************
#var
#   CommonTerm : real;
    
    CommonTerm = DiConst / (SpeedOfLight * ImpedOfFreeSpace)
    LowCap = CommonTerm * TraceWidth / TraceHeight * 1e12
    UpCap = 2/6 * (LowCap/math.sqrt(DiConst))
    FringeCap = CommonTerm*(EffDiConst/DiConst) * pi / math.log(4*TraceHeight/TraceThick) * 1e12
    return LowCap, UpCap, FringeCap
#end LineCap

#****************************************************************************
def EvenLineCap(TraceWidth, TraceSpacing, UpCap, FringeCap) :
#                                                                         
# Calculates the capacitances of a microstrip trace using the model        
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs" two conductors - even-mode.  He defines two new line 
# capacitances:                                                            
#                                                                          
#   Cppue := the even-mode upper plate capacitance (EvenUpCap)             
#   Cfe  := the even-mode fringe capacitance (EvenFringeCap)               
#                                                                          
#***************************************************************************
#var
#  EvenCoupConst : real;

    EvenCoupConst = 1 / ((TraceWidth / TraceSpacing) + 1)
    EvenUpCap = UpCap * EvenCoupConst
    EvenFringeCap = FringeCap * EvenCoupConst
    return EvenUpCap, EvenFringeCap
#end EvenLineCap

#***************************************************************************
def OddLineCap(TraceThick, TraceWidth, TraceHeight, TraceSpacing, DiConst, EffDiConst) :
#                                                                          
# Calculates the capacitances of a microstrip trace using the model        
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs" two conductors - odd-mode.  He defines two new line  
# capacitances:                                                            
#                                                                          
#   Cppuo := the odd-mode upper plate capacitance (OddUpCap)               
#   Cfo  := the odd-mode fringe capacitance (OddFringeCap)                 
#                                                                          
#****************************************************************************
#var
#   OddCoupConst,
#   OddFringeDenom,
#   CommonTerm : real;

    CommonTerm =DiConst / (SpeedOfLight * ImpedOfFreeSpace)
    OddCoupConst = 1 / ((TraceSpacing / TraceWidth) + 1)
    OddUpCap = 8/6 * ((CommonTerm * OddCoupConst)/math.sqrt(DiConst)) * 1e12
    OddFringeDenom = math.log(4*TraceSpacing * math.tanh(4*TraceHeight/TraceSpacing) / (pi*TraceThick))
    OddFringeCap = (CommonTerm*(EffDiConst/DiConst)*pi/OddFringeDenom)*1e12
    return OddUpCap, OddFringeCap
#end OddLineCap

#***************************************************************************
def LoadAdjust(IntCap, DistCap) :
#***************************************************************************
#This function calculates the constant used to adjust the impedance or 
#propagation delay based on the added load capacitance per unit length 

    LoadAdjust = math.sqrt(1 + (DistCap/IntCap))
    return LoadAdjust
