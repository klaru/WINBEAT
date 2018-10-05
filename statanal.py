#! python3
import os, sys
from beatinc import *
from beatio import *
from striplineanal import StripLineStatAnal
from microstriplineanal import MicroStripStatAnal
from dualstriplineanal import DualStripStatAnal
from embedmicrostriplineanal import EmbedMicroStripStatAnal

#************************************************************************
def StatAnal() :
#************************************************************************

#var Ende : boolean

    global Ende, SelOpt
    while Ende == False :
        Header = 'Statistical Analysis'
        OptArray[1] = 'Exit to Main Menue'
        OptArray[2] = 'Strip Line Analysis'
        OptArray[3] = 'Microstrip Line Analysis'
        OptArray[4] = 'Dual-Strip Line Analysis' 
        OptArray[5] = 'Embedded Strip Line Analysis' 
        SelOpt = menu(5,Header,OptArray)
        if SelOpt == '1' :
            Ende = True
        elif SelOpt == '2' :
            StripLineStatAnal()
        elif SelOpt == '3' :
            MicroStripStatAnal()
        elif SelOpt == '4' :
            DualStripStatAnal()
        elif SelOpt == '5' :
            EmbedMicroStripStatAnal()
        else :
            pass
