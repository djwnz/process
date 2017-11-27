#!/usr/bin/env python
################################################################################
#(C) Copyright Pumpkin, Inc. All Rights Reserved.
#
#This file may be distributed under the terms of the License
#Agreement provided with this software.
#
#THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,
#INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE.
################################################################################
"""
@package BM2_process
Module to create the steps for the BM2 process
"""

import sys
sys.path.insert(1, '../src/')

import Tkinter as TK
from functools import partial
import process_SCPI
import process_GUI

class BM2_step_1:
    def __init__(self):
        self.title = "Verify what is being read from the BM2"
        
    # end def
    
    def execute(self):
        print "executing code for this step"
        
    # end def
    
    def gui(self, parent_frame):
        
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = process_GUI.title_font, bg = process_GUI.default_color)
        self.Header.grid(row = 0, column=0, sticky = 'nsew')
        
        self.test_button = TK.Button(parent_frame, text = 'Test',
                                     command = partial(self.button_command, self), 
                                     activebackground = 'green', width = 15)
        self.test_button.config(font = process_GUI.button_font, bg = process_GUI.default_color, 
                               highlightbackground= process_GUI.default_color)
        self.test_button.grid(row = 1, column=0, sticky='e', padx=10, pady=10)  
        
    #end def
    
    def close(self):
        self.test_button.grid_forget()
        self.Header.grid_forget()
    #end def
    
    def button_command(self, event):
        print "button has been pressed"
    #end def
    
#end class    
    
    
#end class
    
    
class BM2_Process:
    def __init__(self):
        self.title = "Testing Program for the BM2"
        
        step1 = BM2_step_1()
        
        self.process = [step1]
    # end def        
#end class