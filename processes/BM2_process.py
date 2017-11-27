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
        self.title = "Verify what is being read from the BM2 then press next"
        self.no_aardvark = False
        
        self.voltage_read = 0.0
        self.temp_read = 0.0
        self.SOC_read = 0
        
    # end def
    
    def execute(self):
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                self.voltage_read = AARD.read_SCPI("BM2:TEL? 9,data", "0x5C", "uint")/1000.0
                self.temp_read = AARD.read_SCPI("BM2:TEL? 8,data", "0x5C", "uint")/100.0
                self.SOC_read = AARD.read_SCPI("BM2:TEL? 13,data", "0x5C", "uint")
            else:
                self.no_aardvark = True
            #end if
        # end with
        
    # end def
    
    def gui(self, parent_frame):
        
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = process_GUI.title_font, 
                           bg = process_GUI.default_color)
        self.Header.grid(row = 0, column=0, columnspan = 2, sticky = 'nsew')
        
        if self.no_aardvark:
            self.error_label = TK.Label(parent_frame, text = "No Aardvark Connected")
            self.error_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.error_label.grid(row = 1, column=0, columnspan = 2)   
        
        else:
        
            self.voltage_label = TK.Label(parent_frame, text = "Voltage (V):")
            self.voltage_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.voltage_label.grid(row = 1, column=0, sticky = 'e')
            
            self.voltage = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.voltage.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.voltage.grid(row = 1, column = 1, ipady = 3, sticky = 'w')    
            self.voltage.insert(0, str(self.voltage_read))
            
            self.temp_label = TK.Label(parent_frame, text = "Temperature (degC):")
            self.temp_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.temp_label.grid(row = 2, column=0, sticky = 'e')
            
            self.temp = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.temp.config(font = process_GUI.text_font, 
                             highlightbackground= process_GUI.default_color)
            self.temp.grid(row = 2, column = 1, ipady = 3, sticky = 'w')
            self.temp.insert(0, str(self.temp_read))
            
            self.SOC_label = TK.Label(parent_frame, text = "SOC (%):")
            self.SOC_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.SOC_label.grid(row = 3, column=0, sticky = 'e')     
            
            self.SOC = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.SOC.config(font = process_GUI.text_font, 
                            highlightbackground= process_GUI.default_color)
            self.SOC.grid(row = 3, column = 1, ipady = 3, sticky = 'w')
            self.SOC.insert(0, str(self.SOC_read))
        
    #end def
    
    def close(self):
        
        self.Header.grid_forget()
        
        if self.no_aardvark:
            self.error_label.grid_forget()
            
        else:
            self.voltage_label.grid_forget()
            self.voltage.grid_forget()
            self.temp_label.grid_forget()
            self.temp.grid_forget()
            self.SOC_label.grid_forget()
            self.SOC.grid_forget()
        # end if
        
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