#! python3
import os, sys
from tkinter import *
from beatinc import *
from beatio import *

#****************************************************************************)
def Help(text):
#****************************************************************************)

    def print_help(file) :
        clear_textwindow(text)
        helpfile = open(file)
        for line in helpfile :
            text.insert(INSERT, line)
        helpfile.close() 
    
    def help_reflect() :
        print_help('reflect.hlp')		# reflectcoef
    def help_stripanal() :
        print_help('stripanal.hlp')	    # StripLineAnal
    def help_microstripanal() :
        print_help('microanal.hlp')	    # MicroStripAnal										
    def help_dualstripanal() :
        print_help('dualanal.hlp')		# DualStripAnal
    def help_embedmicrostripanal() :
        print_help('embedmicro.hlp')	# EmbedMicroStripAnal
    def help_distcapanal() :
        print_help('distcap.hlp')		# DistCapAnal
    def help_crosstalk() :
        print_help('crosstalk.hlp')   	# Crosstalk
    def help_laddernetanal() :						
        print_help('tmodel.hlp')		# LadderNetAnal
    def help_fourieranal() :					
        print_help('fourier.hlp')		# FourierAnal
    def help_statanal() :				
        print_help('statistics.hlp')	# StatAnal
    def help_setunit() :			
        print_help('unitsel.hlp')		# SetUnit
    def help_loadparameters() :
        print_help('library.hlp')		# LoadParameters
	
    root = Toplevel()
    root.title('Electrical Analysis - Help Menu - BEAT (Rev 4.0)')
    w = 450 # width for the Tk root
    h = 300 # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    var = IntVar()    
    button = Button(root, text = 'Return to Main Menu', command = root.destroy).grid(row = 1, column = 0, sticky = W)
    Checkbutton(root, text = 'Reflection Analysis', command = help_reflect).grid(row = 2, column = 0, sticky = W)
    Checkbutton(root, text = 'Strip Line Analysis', command = help_stripanal).grid(row = 3, column = 0, sticky = W)
    Checkbutton(root, text = 'Microstrip Line Analysis', command = help_microstripanal).grid(row = 4, column = 0, sticky = W)
    Checkbutton(root, text = 'Dual-strip Line Analysis', command = help_dualstripanal).grid(row = 5, column = 0, sticky = W)
    Checkbutton(root, text = 'Embedded Microstrip Line Analysis', command = help_embedmicrostripanal).grid(row = 6, column = 0, sticky = W)
    Checkbutton(root, text = 'Dist. Cap. Analysis', command = help_distcapanal).grid(row = 7, column = 0, sticky = W)
    Checkbutton(root, text = 'Crosstalk Analysis', command = help_crosstalk).grid(row = 8, column = 0, sticky = W)
    Checkbutton(root, text = 'Trace Pi Model Generation', command = help_laddernetanal).grid(row = 9, column = 0, sticky = W)
    Checkbutton(root, text = 'Fourier Analysis', command = help_fourieranal).grid(row = 10, column = 0, sticky = W)   
    Checkbutton(root, text = 'Statistical Analysis', command = help_statanal).grid(row = 11, column = 0, sticky = W)
    Checkbutton(root, text = 'Set Unit', command = help_setunit).grid(row = 12, column = 0, sticky = W)
    Checkbutton(root, text = 'Load Library Parameters', command = help_loadparameters).grid(row = 13, column = 0, sticky = W)
        
    root.wait_window()        
# end help
    