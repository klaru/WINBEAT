#! python3
import os, sys, math
from beatinc import *
from tkinter import *

#procedure GetParam (question : str; UnitSel : integer; var number : extended);
#procedure GetIParam (question : str; var number : integer);
#procedure GetResponse (question : str; var response : boolean);
#procedure GetTraceParam;
#procedure GetTraceStatParam;
#procedure TraceParamOut;
#procedure LineAnalOut(EffImped, EffProp, IntCap, IntInduct, IntRes : extended);
#procedure LineAnalStatOut(EffImpedMean,EffImpedSigma,EffPropMean,
#	EffPropSigma,IntCapMean,IntCapSigma,IntInductMean,
#	IntInductSigma,IntResMean,IntResSigma: real);
#procedure LoadParameters
#procedure menu(NumOpt : integer; Header : str; OptArray : strgarray; var SelOpt : opt);
#procedute StatIterNum;
#procedure gui_input

#****************************************************************************
def GetParam(question, number) :
#****************************************************************************
   
   print(question,'[%3.4f] ' %(number), end='')			  
   string = input()
   if string != '' :
       number = float(string)
   return number
#end GetParam 

#****************************************************************************
def GetIParam (question, number) :
#****************************************************************************

   print(question,'[%6i] ' %(number), end='')				
   string = input()
   if string != '' :
       number = int(string)
   return number
#end GetIParam


#*************************************************************************
def GetNetInfo():
#*************************************************************************
#begin
    global IntImped, IntProp, Resist, TraceLength, TRise
    IntImped = GetParam('What is the line impedance?',IntImped)
    IntProp = GetParam('What is the propagation delay?',IntProp)
    Resist = GetParam('What is the intrinsic resistance?',Resist)
    TraceLength = GetParam('What is the line length?',TraceLength)
    TRise = GetParam('What is the rise time?',TRise)
    return IntImped, IntProp, Resist, TraceLength, TRise
#end


#****************************************************************************
def GetResponse (question, yn) :
#****************************************************************************

    Query = yn
    print (question, '[',yn,'] ', end='')
    while True :
        string = input()
        if ((string == 'y') 
		 or (string == 'Y') 
		 or (string == 'n') 
		 or (string == 'N') 
		 or (string == '')) : break
    if string != '' :
	    Query = string
    if ((Query == 'y') 
	 or (Query == 'Y')) :
        Response = True
    else :
        Response = False
    return Response
#end  GetResponse

#****************************************************************************
def GetTraceParam() :
#****************************************************************************
    UnitSys = 0
    global TraceThick, TraceWidth, TraceHeight, DiConst
    if UnitSys == 1 :
        TraceThick  = TraceThick * 25.4
        TraceWidth  = TraceWidth * 25.4
        TraceHeight = TraceHeight * 25.4
        TraceThick = GetParam('What is the trace thickness? [mm]  ', TraceThick)
        TraceWidth = GetParam('What is the trace width? [mm]  ', TraceWidth)
        TraceHeight = GetParam('What is the trace height? [mm]  ', TraceHeight)
    else :
        TraceThick = GetParam('What is the trace thickness? [in]  ', TraceThick)
        TraceWidth = GetParam('What is the trace width? [in]  ', TraceWidth)
        TraceHeight = GetParam('What is the trace height? [in]  ', TraceHeight)
    DiConst = GetParam('What is the dielectric constant? ', DiConst)
    return TraceThick, TraceWidth, TraceHeight, DiConst
#end GetTraceParam

#**************************************************************************
def GetTraceStatParam() :
#**************************************************************************
#    These routines were derived from GetTraceParamXXX                             
#**************************************************************************

	# initialize default values first
    global TraceThick, TraceWidth, TraceHeight, DiConst, \
           TraceThickSigma, TraceWidthSigma, TraceHeightSigma, DiConstSigma
    TraceWidthMean = TraceWidth 
    TraceThickMean = TraceThick
    TraceHeightMean = TraceHeight
    DiConstMean = DiConst
    TraceThickMean = GetParam('What is the mean trace thickness? ', TraceThickMean)
    TraceThickSigma = GetParam('What is the standard deviation for thickness? ', TraceThickSigma)
    TraceWidthMean = GetParam('What is the mean trace width? ', TraceWidthMean)
    TraceWidthSigma = GetParam('What is the standard deviation for width? ', TraceWidthSigma)
    TraceHeightMean = GetParam('What is the mean trace height? ', TraceHeightMean)
    TraceHeightSigma = GetParam('What is the standard deviation for height? ', TraceHeightSigma)
    DiConstMean = GetParam('What is the mean dielectric constant? ', DiConstMean)
    DiConstSigma = GetParam('What is the standard deviation for DiConst? ', DiConstSigma)
    TraceThick = TraceThickMean  # Keep the entered values as defaults
    TraceWidth = TraceWidthMean
    TraceHeight = TraceHeightMean
    DiConst = DiConstMean
    return TraceThickMean, TraceThickSigma, TraceWidthMean, TraceWidthSigma, TraceHeightMean, TraceHeightSigma, \
           DiConstMean, DiConstSigma 
#end GetTraceStatParam

#****************************************************************************
def TraceParamOut() :
#****************************************************************************

      print ('Micro-strip Trace Parameters')
      print ('-----------------------------')
      print ('Thickness:  %5.4f' %(TraceThick), ' in.')			
      print ('Width:      %4.3f' %(TraceWidth), ' in.')       
      print ('Height:     %4.3f' %(TraceHeight), ' in.')         
      print ('Spacing:    %4.3f' %(TraceSpacing), ' in.')       
      print ('Er:         %3.2f' %(DiConst))                    
      print ('DistCap     %5.4f' %(DistCap))                    
      print ('\n')
# end TraceParamOut


#****************************************************************************
def LineAnalOut(EffImped, EffProp, IntCap, IntInduct, IntRes) :
#****************************************************************************

   print ('\n')
   print ('Line analysis:')
   print ('--------------')
   print ('Impedance (ohms):                = %3.1f' %(EffImped)) 
   print ('Propagation Delay (ns/ft):       = %2.2f' %(EffProp))   
   print ('Intrinsic Capacitance (pf/in):   = %2.2f' %(IntCap))    
   print ('Intrinsic Inductance (nH/in):    = %2.2f' %(IntInduct))
   print ('Intrinsic Resistance (mohms/in)  = %2.2f' %(IntRes)) 
   print ('\n')
#end LineAnalOut


#**************************************************************************
def LineAnalStatOut(EffImpedMean,EffImpedSigma,EffPropMean,EffPropSigma,IntCapMean,IntCapSigma,IntInductMean,IntInductSigma,IntResistMean,IntResistSigma) :
#
#    output of the data which resulted from statistical analysis. This is
#    basically a modified version of LineAnalOut.                          
#**************************************************************************

    print ('\n')
    print ('Line analysis:')
    print ('--------------')
    print ('Impedance (ohms):               mean = %3.1f' %(EffImpedMean), '   sigma = %3.3f' %(EffImpedSigma))  
    print ('Propagation Delay (ns/ft):      mean = %2.2f' %(EffPropMean), '   sigma = %2.4f' %(EffPropSigma))     
    print ('Intrinsic Capacitance (pf/in):  mean = %2.2f' %(IntCapMean), '   sigma = %2.4f' %(IntCapSigma))       
    print ('Intrinsic Inductance (nH/in):   mean = %2.2f' %(IntInductMean), '   sigma = %2.4f' %(IntInductSigma))
    print ('Intrinsic Resistance (mohms/in) mean = %2.2f' %(IntResistMean), '   sigma = %2.4f' %(IntResistSigma)) 
    print ('\n')
# end LineAnalStatOut


#****************************************************************************)
def menu(NumOpt, Header, OptArray, text):
#****************************************************************************)

# This procedure provides the ability to generate a menu driven program *)
# Options are limited to ten selections.  The Option number selected is *)
# returned to the main program.                                         *)

#var
#  Temp,
#  DepthMargin,
#  WidthMargin : integer;
#  Option : opt;

    Temp = 0
#    os.system('cls')     Clear Screen 
    for Temp in range(1, (ScreenWidth - 48)//2 + 6) :
        text.insert(INSERT, ' ')
    text.insert(INSERT, 'Board Electrical Analysis Tool - BEAT (Rev 4.0)')   
    DepthMargin = (ScreenDepth - NumOpt - 5)//2
    WidthMargin = (ScreenWidth - 40)//2
    for Temp in range(1, DepthMargin + 1) :
        text.insert(INSERT, '\n')
    for Temp in range (1, WidthMargin + 1) :
        text.insert(INSERT, ' ')
    text.insert(INSERT, Header)
    text.insert(INSERT, '\n')
    for Temp in range(1, WidthMargin + 1) :
        text.insert(INSERT, ' ')
    text.insert(INSERT, '-----------------------------------------------')
    text.insert(INSERT, '\n')
    for Option in range(1, NumOpt + 1) :
        for Temp in range(1, (WidthMargin - 3 + 1)) :
            text.insert(INSERT, ' ')
        text.insert(INSERT,'\n')
        out = str(Option)
        text.insert(INSERT, out)
        out = str(') ')
        text.insert(INSERT, out)
        text.insert(INSERT, OptArray[Option])
    for Temp in range(1, WidthMargin + 1) :
        text.insert(INSERT, ' ')
    text.pack()
#   os.system('cls')

#************************************************************************
def StatIterNum(NumIterations) :
#************************************************************************           
        while True:    
            NumIterations = GetIParam('Enter number of iterations :', NumIterations)
            if (NumIterations <= 0) or (NumIterations > IterationsMax) :
                print('\n')
                print('The number of iterations must be more than 1.')
                print('If you want to exceed ',IterationsMax,' Iterations,')
                print('you will have to change the #constant "IterationsMax"')
                print('in "beatinc.py" and recompile the program.')
                print('\n')
                answer = GetResponse('Hit >RETURN< to continue','y')            
            if (NumIterations > 0) and (NumIterations <= IterationsMax) : break
        return NumIterations            

 
def gui_input(prompt):

    root = Toplevel()
    w = 300 # width for the Tk root
    h = 65 # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


    # this will contain the entered string, and will
    # still exist after the window is destroyed
    var = StringVar()

    # create the GUI
    label = Label(root, text=prompt)
    entry = Entry(root, textvariable=var)
    label.pack(side="left", padx=(20, 0), pady=20)
    entry.pack(side="right", fill="x", padx=(0, 20), pady=20, expand=True)
    entry.focus()

    # Let the user press the return key to destroy the gui 
    entry.bind("<Return>", lambda event: root.destroy())

    # this will block until the window is destroyed
    root.wait_window()

    # after the window has been destroyed, we can't access
    # the entry widget, but we _can_ access the associated
    # variable
    value = var.get()
    return value           
