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

class Serial_number:
    def __init__(self, properties):
        self.title = "Update the " + properties.module + " serial number"
        self.text = "Enter the desired serial number in the box and then " +\
            "press \"update\" to update\nthe module's serial number.\n" +\
            "Press next when you have finished."
        
        self.no_aardvark = False
        
        self.serial_number = 0
        
        self.properties = properties
        
    # end def
    
    def execute(self):
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                # read current serial number
                self.serial_number = AARD.read_SCPI("SUP:TEL? 9,data", 
                                                    self.properties.address,
                                                    "uint")
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
        
            self.serial_label = TK.Label(parent_frame, text = "Serial Number:")
            self.serial_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.serial_label.grid(row = 2, column=0, sticky = 'e')
            
            self.serial = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.serial.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.serial.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            self.serial.insert(0, str(self.serial_number))
            
            self.update_button = TK.Button(parent_frame, text = 'Update', 
                                         command = partial(self.update_command, 
                                                           self), 
                                         activebackground = 'green', width = 15)
            self.update_button.config(font = process_GUI.button_font, 
                                      bg = process_GUI.default_color, 
                                    highlightbackground= process_GUI.default_color)
            self.update_button.grid(row = 3, column=0, columnspan = 2,
                                    padx=10, pady=10)            
        
    #end def
    
    def close(self):
        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            self.error_label.grid_forget()
            
        else:
            self.serial_label.grid_forget()
            self.serial.grid_forget()
            self.update_button.grid_forget()
        # end if
        
    #end def
    
    def get_sn(self):
        """
        Function to find the desired delay that was entered in the gui.
        
        @return     (int)         The delay that will be used in ms.
        """        
        # read the delay from the gui
        serial_text = self.serial.get()
        # verify if the delay is valid
        if serial_text.isdigit():
            # is a good delay so set it as the delay time
            return serial_text
            
        else:
            # the delay is not valid
            print '*** Requested Serial Number is not valid, '\
                  'reverting to default ***'
            # restore the default delay
            return '0'
        # end if    
    # end def    
    
    def update_command(self, event):
        #self.update_button.config(state = 'disabled')
        
        serial_text = self.get_sn()
        nvm_key = self.serial_number + 12345
        
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                AARD.send_SCPI("SUP:NVM UNLOCK,"+str(nvm_key), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM SERIAL,"+serial_text, 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM WRITE,1", 
                               self.properties.address)
            else:
                self.no_aardvark = True
            #end if
        # end with
    #end def
#end class 

class I2C_address:
    def __init__(self, properties):
        self.title = "Update the " + properties.module + " I2C Address"
        self.text = "Enter the desired I2C in the box and then " +\
            "press \"update\" to update\nthe module's I2C Address.\n" +\
            "Press next when you have finished."
        
        self.no_aardvark = False
        
        self.serial_number = 0
        
        self.properties = properties
        
    # end def
    
    def execute(self):
        next
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
            self.address_label = TK.Label(parent_frame, 
                                  text = "I2C Address of " + self.properties.module + ":")
            self.address_label.config(font = process_GUI.label_font, 
                                      bg = process_GUI.default_color)
            self.address_label.grid(row = 2, column=0, sticky = 'e')
        
            self.address_entry = TK.Entry(parent_frame, justify = 'left', 
                                          width = 7)
            self.address_entry.config(font = process_GUI.text_font, 
                                      highlightbackground= process_GUI.default_color)
            self.address_entry.grid(row = 2, column = 1, ipady = 3, sticky = 'w')     
            self.address_entry.insert(0, self.properties.address)
            
            self.update_button = TK.Button(parent_frame, text = 'Update', 
                                           command = partial(self.update_command, 
                                           self), 
                                         activebackground = 'green', width = 15)
            self.update_button.config(font = process_GUI.button_font, 
                                      bg = process_GUI.default_color, 
                                      highlightbackground= process_GUI.default_color)
            self.update_button.grid(row = 3, column=0, columnspan = 2,
                                    padx=10, pady=10)   
        #end if
        
    #end def
    
    def close(self):
        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            self.error_label.grid_forget()
            
        else:
            self.address_label.grid_forget()
            self.address_entry.grid_forget()
            self.update_button.grid_forget()
        # end if
        
    #end def
    
    def get_addr(self):
        """
        Function to find the desired delay that was entered in the gui.
        
        @return     (int)         The delay that will be used in ms.
        """        
        # read the delay from the gui
        address_text = self.address_entry.get()
        # verify if the delay is valid
        if (address_text.startswith('0x') and len(address_text) ==4 and
            self.is_hex(address_text[2:])):
            
            # is a good delay so set it as the delay time
            return address_text
            
        else:
            # the delay is not valid
            print '*** Requested address is not valid, '\
                  'reverting to default ***'
            # restore the default delay
            return '0'
        # end if    
    # end def 
    
    def is_hex(self, s):
        """
        Determine if a string is a hexnumber
        
        @param[in]  s:       The string to be tested (string).
        @return     (bool)   True:    The string is a hex number.
                             False:   The command is not a hex number.
        """    
        # if it can be converted to a base 16 int then it is hex
        try:
            int(s, 16)
            return True
        
        except ValueError:
            # it could not be converted therefore is not hex
            return False
        # end try
    # end def    
    
    def update_command(self, event):
        #self.update_button.config(state = 'disabled')
        
        address_text = self.get_addr()
        
        address_num = int(address_text[2:], 16)
        
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                
                nvm_key = AARD.read_SCPI("SUP:TEL? 9,data", 
                                         self.properties.address, "uint")+12345   
                
                AARD.send_SCPI("SUP:NVM UNLOCK,"+str(nvm_key), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM I2C,"+str(address_num), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM WRITE,1", 
                               address_text)
                self.properties.address = address_text
            else:
                self.no_aardvark = True
            #end if
        # end with
    #end def
#end class 

class Update_OSCTUN:
    def __init__(self, properties):
        self.title = "Update the " + properties.module + \
            " oscillator tuning parameter"
        self.text = "Enter the desired tuning parameter in the box and then " +\
            "press \"update\" to update\nthe module's tuning parameter.\n" +\
            "Press next when you have finished."
        
        self.no_aardvark = False
        
        self.tuning_param = 0
        
        self.properties = properties
        
    # end def
    
    def execute(self):
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                # read current serial number
                self.tuning_param = AARD.read_SCPI("SUP:TEL? 11,data", 
                                                    self.properties.address,
                                                    "schar")
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
        
            self.param_label = TK.Label(parent_frame, 
                                         text = "Tuning Parameter:")
            self.param_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.param_label.grid(row = 2, column=0, sticky = 'e')
            
            self.param = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.param.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.param.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            self.param.insert(0, str(self.tuning_param))
            
            self.update_button = TK.Button(parent_frame, text = 'Update', 
                                         command = partial(self.update_command, 
                                                           self), 
                                         activebackground = 'green', width = 15)
            self.update_button.config(font = process_GUI.button_font, 
                                      bg = process_GUI.default_color, 
                                    highlightbackground= process_GUI.default_color)
            self.update_button.grid(row = 3, column=0, columnspan = 2,
                                    padx=10, pady=10)            
        
    #end def
    
    def close(self):
        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            self.error_label.grid_forget()
            
        else:
            self.param_label.grid_forget()
            self.param.grid_forget()
            self.update_button.grid_forget()
        # end if
        
    #end def
    
    def get_param(self):
        """
        Function to find the desired delay that was entered in the gui.
        
        @return     (int)         The delay that will be used in ms.
        """        
        # read the delay from the gui
        param_text = self.param.get()
        # verify if the delay is valid
        try:
            int(param_text)
            # is a good delay so set it as the delay time
            return param_text
            
        except ValueError:
            # the delay is not valid
            print '*** Requested Tuning Parameter is not valid, '\
                  'reverting to default ***'
            # restore the default delay
            return '0'
        # end if    
    # end def    
    
    def update_command(self, event):
        #self.update_button.config(state = 'disabled')
        
        param_text = self.get_param()
        
        with process_SCPI.aardvark() as AARD:
            if AARD.port != None:
                
                nvm_key = AARD.read_SCPI("SUP:TEL? 9,data", 
                                         self.properties.address, "uint")+12345   
                
                AARD.send_SCPI("SUP:NVM UNLOCK,"+str(nvm_key), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM OSCTUN,"+param_text, 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM WRITE,1", 
                               self.properties.address)
            else:
                self.no_aardvark = True
            #end if
        # end with
    #end def
#end class 

class Address_request:
    def __init__(self, properties):
        self.title = "Enter the current I2C Address of the " + properties.module
        self.text = "The default address has been entered for you" 
        
        self.properties = properties
    # end def
    
    def execute(self):
        next
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
        
        self.address_label = TK.Label(parent_frame, 
                                      text = "I2C Address of " + \
                                      self.properties.module + ":")
        self.address_label.config(font = process_GUI.label_font, 
                             bg = process_GUI.default_color)
        self.address_label.grid(row = 2, column=0, sticky = 'e')
        
        self.address_entry = TK.Entry(parent_frame, justify = 'left', width = 7)
        self.address_entry.config(font = process_GUI.text_font, 
                            highlightbackground= process_GUI.default_color)
        self.address_entry.grid(row = 2, column = 1, ipady = 3, sticky = 'w')     
        self.address_entry.insert(0, self.properties.address)
    
    def close(self):
        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        addr = self.get_addr()
        
        if addr != '0':
            self.properties.address = addr
        #end if
        
        self.address_label.grid_forget()
        self.address_entry.grid_forget()

    #end def
    
    def get_addr(self):
        """
        Function to find the desired delay that was entered in the gui.
        
        @return     (int)         The delay that will be used in ms.
        """        
        # read the delay from the gui
        address_text = self.address_entry.get()
        # verify if the delay is valid
        if (address_text.startswith('0x') and len(address_text) ==4 and
            self.is_hex(address_text[2:])):
            
            # is a good delay so set it as the delay time
            return address_text
            
        else:
            # the delay is not valid
            print '*** Requested address is not valid, '\
                  'reverting to default ***'
            # restore the default delay
            return '0'
        # end if    
    # end def 
    
    def is_hex(self, s):
        """
        Determine if a string is a hexnumber
        
        @param[in]  s:       The string to be tested (string).
        @return     (bool)   True:    The string is a hex number.
                             False:   The command is not a hex number.
        """    
        # if it can be converted to a base 16 int then it is hex
        try:
            int(s, 16)
            return True
        
        except ValueError:
            # it could not be converted therefore is not hex
            return False
        # end try
    # end def    
#end class 

class process_properties:
    def __init__(self, mod, addr):
        self.title = "Testing Program for the "+ mod
        self.address = addr
        self.module = mod
    #end def
#end class