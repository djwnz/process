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
import time
import SUP_process

class BM2_verification:
    def __init__(self, properties):
        self.title = "Verify BM2 Values"
        self.text = "Check these values against what you can measure/" +\
            "what you expect.\n Press next when you have done this."
        self.no_aardvark = False
        
        self.voltage_read = 0.0
        self.temp_read = 0.0
        self.SOC_read = 0
        
        self.properties = properties
        
    # end def
    
    def execute(self):
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                self.voltage_read = AARD.read_SCPI("BM2:TEL? 9,data", 
                                                   self.properties.address, 
                                                   "uint")/1000.0
                self.temp_read = AARD.read_SCPI("BM2:TEL? 8,data", 
                                                self.properties.address, 
                                                "uint")/100.0
                self.SOC_read = AARD.read_SCPI("BM2:TEL? 13,data", 
                                               self.properties.address, "uint")
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
        
        self.body = TK.Label(parent_frame, text = self.text)
        self.body.config(font = process_GUI.label_font, 
                           bg = process_GUI.default_color)
        self.body.grid(row = 1, column=0, columnspan = 2, sticky = 'nsew')        
        
        if self.no_aardvark:
            self.error_label = TK.Label(parent_frame, 
                                        text = "No Aardvark Connected")
            self.error_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.error_label.grid(row = 2, column=0, columnspan = 2)   
        
        else:
        
            self.voltage_label = TK.Label(parent_frame, text = "Voltage (V):")
            self.voltage_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.voltage_label.grid(row = 2, column=0, sticky = 'e')
            
            self.voltage = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.voltage.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.voltage.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            self.voltage.insert(0, str(self.voltage_read))
            
            self.temp_label = TK.Label(parent_frame, 
                                       text = "Temperature (degC):")
            self.temp_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.temp_label.grid(row = 3, column=0, sticky = 'e')
            
            self.temp = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.temp.config(font = process_GUI.text_font, 
                             highlightbackground= process_GUI.default_color)
            self.temp.grid(row = 3, column = 1, ipady = 3, sticky = 'w')
            self.temp.insert(0, str(self.temp_read))
            
            self.SOC_label = TK.Label(parent_frame, text = "SOC (%):")
            self.SOC_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.SOC_label.grid(row = 4, column=0, sticky = 'e')     
            
            self.SOC = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.SOC.config(font = process_GUI.text_font, 
                            highlightbackground= process_GUI.default_color)
            self.SOC.grid(row = 4, column = 1, ipady = 3, sticky = 'w')
            self.SOC.insert(0, str(self.SOC_read))
        
    #end def
    
    def close(self):
        
        self.Header.grid_forget()
        self.body.grid_forget()
        
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
#end class    

class BM2_heater_test:
    def __init__(self, properties):
        self.title = "Test the operation of the heater"
        self.text = "The heater will be tested by turning it on and off " +\
            "again and calculating\nthe power drawn by the heaters.\n" +\
            "For 2 and 4 cell batteries this should be approximately 10W and " +\
            "for 3 cells, 12W" 
        self.no_aardvark = False
        
        self.initial_current = 0
        self.voltage = 0
        self.properties = properties
        
    # end def
    
    def execute(self):
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                # read current serial number
                self.initial_current = AARD.read_SCPI("BM2:TEL? 10,data", 
                                                      self.properties.address, 
                                                      "uint")/1000.0
                self.voltage = AARD.read_SCPI("BM2:TEL? 9,data", 
                                              self.properties.address, 
                                              "uint")/1000.0
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
        
        self.body = TK.Label(parent_frame, text = self.text)
        self.body.config(font = process_GUI.label_font, 
                           bg = process_GUI.default_color)
        self.body.grid(row = 1, column=0, columnspan = 2, sticky = 'nsew')          
        
        if self.no_aardvark:
            self.error_label = TK.Label(parent_frame, 
                                        text = "No Aardvark Connected")
            self.error_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.error_label.grid(row = 2, column=0, columnspan = 2)   
        
        else:
        
            self.power_label = TK.Label(parent_frame, 
                                        text = "Heater Power (W):")
            self.power_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.power_label.grid(row = 2, column=0, sticky = 'e')
            
            self.power = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.power.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.power.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            
            self.heater_button = TK.Button(parent_frame, text = 'Test Heater', 
                                         command = partial(self.heater_command, 
                                                           self), 
                                         activebackground = 'green', width = 15)
            self.heater_button.config(font = process_GUI.button_font, 
                                      bg = process_GUI.default_color, 
                                    highlightbackground= process_GUI.default_color)
            self.heater_button.grid(row = 3, column=0, columnspan = 2,
                                    padx=10, pady=10)            
        
    #end def
    
    def close(self):
        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            self.error_label.grid_forget()
            
        else:
            self.power_label.grid_forget()
            self.power.grid_forget()
            self.heater_button.grid_forget()
        # end if
        
    #end def
    
    def heater_command(self, event):
        #self.update_button.config(state = 'disabled')
        
        rest_power = self.initial_current*self.voltage
        
        new_current = self.initial_current
        
        self.power.delete(0, 'end')
        
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                AARD.send_SCPI("BM2:HEA ON", self.properties.address)
                time.sleep(2)
                new_current = AARD.read_SCPI("BM2:TEL? 10,data", 
                                             self.properties.address, 
                                             "int")/-1000.0                
                AARD.send_SCPI("BM2:HEA OFF", self.properties.address)
            else:
                self.no_aardvark = True
            #end if
        # end with
        
        heater_power = (new_current * self.voltage) - rest_power
        
        self.power.insert(0, str(heater_power))
    #end def
#end class   

class BM2_Process:
    def __init__(self):
        self.properties = SUP_process.process_properties("BM2", "0x5C")
        
        verification = BM2_verification(self.properties)
        heater_test = BM2_heater_test(self.properties)
        serial_number = SUP_process.Serial_number(self.properties)
        address_request = SUP_process.Address_request(self.properties)
        I2C_Address = SUP_process.I2C_address(self.properties)
        frq_tuning = SUP_process.Update_OSCTUN(self.properties)
        
        self.process = [address_request, 
                        verification, 
                        frq_tuning,
                        heater_test, 
                        serial_number,
                        I2C_Address]
    # end def        
#end class