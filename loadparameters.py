#! python3
import os, sys, math
from beatinc import *
from beatio import *

#***************************************************************************
def LoadParameters() :
#   This procedures accesses the database "library.bea".
#   The database contains specifications of multilayer boards and may
#   be changed or appended at any time.
#   However, when modifying the database please take the rather stringent
#   data structure into account. It is described in the user's manual.
#   Deviating from this structure may very likely casuse BEAT to either
#   run into one of the traps incorporated in this procedure or just
#   crash.
#    Ulf Schlichtmann, 6/89                                                 
#***************************************************************************

#const
#    LibStringLength = 70   no database entry may exceed 70 characters 
#    LayerTypeLength = 10   keyword for layer type : 10 chars max 
                          # Note: if this parameter is changed, the
                          #         comparisons between LayerType and some
                          #         string constants below will have to be
                          #         changed also                           
    LayerTypeMax = 10     # Max number of layer that can be stored. Since boards
                          # are assumed to be symmetrical, boards with twice
                          # as many layers can be handled                
    SpecMax = 20          # Current max number of specs that can be handled   

#type
#   LibString = array[1..LibStringLength] of char;
#   LayerTypeString = array[1..LayerTypeLength] of char;

#var
#   i, j, k, l,
#   NumSpecs,SpecSelect,
#   NumLayers,LayerNum,LayerSelect,
#   TempIndex : integer;
#   dummy : char;
#   InRange, LayerTypeOK, LoadOK : boolean;
#   SpecDocNum,SpecDescription : array[1..SpecMax] of LibString;
#   LayerType : array[1..LayerTypeMax] of LayerTypeString;
#   lib:text;


#        First part of this procedure reads all available specs from the
#        library, displays the titles and gets a user selection 
    SpecDocNum = [' '] * SpecMax
    SpecDescription = [' '] * SpecMax
    LayerType = [' '] * LayerTypeMax
    LoadOK = True
    os.system('cls')
    print('Load Library Parameters:');
    print( 'Listing of currently available Specifications');
    print('--------------------------------------------------------------');

    lib = open('library.bea', 'r')
    line = lib.readline()  # number of available specs
    NumSpecs = int(line)
    dummy = lib.readline()     # 'blank' line

    if NumSpecs > SpecMax :	   # too many specs in database
        LoadOK = False
        print ('\n')
        print ('Database contains %3i' %(NumSpecs),' specs.')				
        print ('Currently BEAT can handle only %3i' %(SpecMax),' specs, however')
        print ('Please change the parameter "SpecMax" and recompile BEAT')
        print ('\n')
        print ('Hit RETURN to continue')
        dummy = input()
    #end if

    for i in range(1, NumSpecs + 1) :  			        # read Doc-number and -description for 
        SpecDocNum[i] = ' ' 
        SpecDescription[i] = ' '
        SpecDocNum[i] = lib.readline()
        SpecDescription[i] = lib.readline()   				            
        print (i,' : ',SpecDocNum[i], end='')  	    	
        print ('     ',SpecDescription[i], end='')
    #end for

    SpecSelect = 1   							        # Get user selection 
    print ('\n')
    while True:
        InRange = True
        SpecSelect = GetIParam ('Select by entering a number : ', SpecSelect)
        if ((SpecSelect < 1) 
		 or (SpecSelect > NumSpecs)) :
            InRange = False
            print ('Incorrect Selection!   Try Again')
        if InRange == True : break

#           Second part of this procedure reads and displays the available
#           layers for the selected spec and gets a user selection.
#           Only first 50% of layers are displayed since boards are
#           assumed to be symmectrical.                                    
    os.system('cls')
    print ('Load Library Parameters:')
    print (SpecDescription[SpecSelect])
    print ('Listing of available layers')
    print ('--------------------------------------------------------------')

    lib=open('library.bea', 'r')
    dummy = lib.readline()                     		 # skip thru listing of available specs 
    dummy = lib.readline()
    for i in range(1, NumSpecs + 1) :
        dummy = lib.readline()
        dummy = lib.readline()
    #end for
    dummy = lib.readline ()                   	     # go thru this loop for all specs up to the 
    for i in range (1, SpecSelect + 1) :      	     # selected spec. Only the data for
        dummy = lib.readline()         	      		 # the selected spec are displayed, however
        dummy = lib.readline()
        line = lib.readline() 		      		 # number of layers for this spec
        NumLayers = int(line)
        if NumLayers/2 != math.trunc(NumLayers/2) :  # only even number allowed
            LoadOK = False
            print ('\n')
            print ('Database shows %2i' %(NumLayers), ' layers for spec. # %2.i' %(i), '.')
            print ('This is incorrect. Only even numbers are allowed.')
            print ('The boards are assumed to be symmetrical.')
            print ('Please check the manual and correct the database')
            print ('\n')
            print ('Hit RETURN to continue')
            dummy = input()
        #end if
        dummy = lib.readline()  			                    # number of this layer 
        for j in range(1, math.trunc(NumLayers/2) + 1) : 	    # type of this layer
            LayerNum = lib.readline()
            LayerType[j] = lib.readline()
            LayerTypeOK = False  								 # make sure it is permitted layer type 
# skip next data depending on	   
            if ((LayerType[j] == 'strip\n') 
			 or (LayerType[j] == 'embedmicro\n')) :  				 # type of layer
                for l in range(1, 4 + 1) :
                    dummy = lib.readline()
                LayerTypeOK = True
            #end if
            if ((LayerType[j] == 'microstrip\n') 
			 or (LayerType[j] == 'dualstrip\n')) :
                for l in range (1, 5 + 1) : 
                    dummy = lib.readline()
                LayerTypeOK = True
            #end if
            if ((LayerType[j] == 'gnd\n') 
			 or (LayerType[j] == 'pwr\n')					
			 or (LayerType[j] == 'gnd/pwr\n')) :
	            LayerTypeOK = True

            if LayerTypeOK == False :
                LoadOK = True
                print ('\n')
                print (LayerType[j])
                print ('This is not a recognized layer type.')
                print ('Please check the manual and correct the database')
                print ('\n')
                print ('Hit RETURN to continue');
                dummy = input()
            #end if

            dummy = lib.readline()
            if i == SpecSelect :
	            print (j,' : ',LayerType[j], end='')			#:2
        #end for NumLayers
    #end for SpecSelect

            #  The third part of this procedure loads the data for the
            #  selected layer of the selected board into the applicable
            #  variables.                                                
            #  Please note:
            #  Because of the way this is handled - all data up to the
            #  selected layer are loaded into the variables, only the selec-
            #  ted layer will not be overwritten, all variables involved in
            #  this probably will be clobbered.                          
    LayerSelect = 1
    print ('\n')
    while True :
        InRange = True
        LayerSelect = GetIParam ('Select by entering a number : ', LayerSelect)
        if ((LayerSelect < 1) 
		 or (LayerSelect > NumLayers/2)) :
            InRange = False
            print ('Incorrect Selection!   Try Again')
        #end if
        if ((LayerType[LayerSelect] == 'gnd\n') 
		 or (LayerType[LayerSelect] == 'pwr\n') 
		 or (LayerType[LayerSelect] == 'gnd/pwr\n')) :
            InRange = False
            print (LayerType[LayerSelect],':')
            print ('This layer cannot be selected for analysis!    Try Again')
        #end if		   
        if InRange == True : break
    #end while

    lib = open('library.bea','r')
    dummy = lib.readline()
    dummy = lib.readline()
    for i in range(1, NumSpecs + 1) :
        dummy = lib.readline()
        dummy = lib.readline()
    #end for
    dummy = lib.readline()
    for i in range(1, SpecSelect + 1) :
        dummy = lib.readline()
        dummy = lib.readline()
        line = lib.readline()
        NumLayers = int(line)
        dummy = lib.readline()
        if i == SpecSelect :
	        TempIndex = LayerSelect
        else :
            TempIndex = math.trunc(int(NumLayers)/2)
        for j in range(1, TempIndex + 1) :
            LayerNum = lib.readline()
            LayerType[j] = lib.readline()
            if ((LayerType[j] == 'strip\n') 
			 or (LayerType[j] == 'embedmicro\n')) :
                TraceThick = lib.readline()
                TraceWidth = lib.readline()
                TraceHeight = lib.readline()
                DiConst = lib.readline()
		   
            if LayerType[j] == 'microstrip\n' :
                TraceThick = lib.readline()
                TraceWidth = lib.readline()
                TraceHeight = lib.readline()
                DiConst = lib.readline()
                SoldMask = lib.readline()
 
            if LayerType[j] == 'dualstrip\n' :
                TraceThick = lib.readline()
                TraceWidth = lib.readline()
                TraceHeight = lib.readline()
                SigPaneSep = lib.readline()
                DiConst = lib.readline()
            dummy = lib.readline()
        #end for
    #end for
    if LoadOK == True :
        print('\n')
        print('Parameter have been loaded into variables.')
        print('\n')
        print('Hit RETURN to continue.')
        dummy = input()

