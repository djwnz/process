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

__author__ = 'David Wright (david@asteriaec.com)'
__version__ = '0.1.0' #Versioning: http://www.python.org/dev/peps/pep-0386/

#
# -------
# Imports

import sys
sys.path.insert(1, '../src/')

import Tkinter as TK
from functools import partial
import process_SCPI
import process_GUI
import time

#
# -------
# Classes

class process_properties:
    """
    The class that contains the process properties common to all steps

    @attribute title    (string)      The title of the process 
    @attribute address  (string)      The address of the module in hex "0x--"
    @attribute module   (string)      The name of the module to be used
    """    
    def __init__(self, mod, addr):
        """ 
        Initialise the properties
        """
        self.title = "Testing Program for the "+ mod
        self.address = addr
        self.module = mod
    #end def
#end class


class SupMCU_process:
    """
    The class that denotes the steps common to all modules

    @attribute process   (list)   The common steps to be performed for 
                                  every module
    """      
    def __init__(self, properties):
        """ 
        Initialise the common process
        
        @param properties  (SUP_process.process_properties) Denotes propeties 
                                                            of the process
        """   
        # Initialse all of the common steps
        __serial_number = _Serial_number(properties)
        __address_request = _Address_request(properties)
        __I2C_Address = _I2C_address(properties)
        __frq_tuning = _Update_OSCTUN(properties)   
        
        # create a list of all of these steps
        self.process = [__address_request, 
                        __serial_number, 
                        __I2C_Address, 
                        __frq_tuning]
    #end def
#end class     
    

class _Serial_number:
    """
    Class that manages setting of the module serial number

    @attribute properties    (SUP_process.process_properties) 
                                          Denotes propeties of the step
    @attribute title          (String)    Title text to display
    @attribute text           (String)    Body text to display
    @attribute Header         (TK label)  The title as displayed in the GUI
    @attribute body           (TK label)  Body text display in GUI
    @attribute error_label    (TK label)  Text to display if there is an error
    @attribute no_aardvark    (bool)      True is a connection to an aardvark 
                                          has been made, False otherwise.
    @attribute serial_number  (int)       The module serial number
    @attribute serial_label   (TK label)  Serial number title
    @attribute serial         (TK Entry)  Serial number Display
    @attribute update_button  (TK Button) Button to start the serial number 
                                          setting action
    """     
    def __init__(self, properties):
        """
        Initialise the Serial numnber setting class
    
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """        
        # define the title of the step
        self.title = "Update the " + properties.module + " serial number"
        
        # define the body text for the step
        self.text = "Enter the desired serial number in the box and then " +\
            "press \"update\" to update\nthe module's serial number.\n" +\
            "Press next when you have finished."
        
        # initialise attributes 
        self.no_aardvark = False
        self.serial_number = 0
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step:
    
        Read the current module serial number
        """        
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found, read the data
                self.serial_number = AARD.read_SCPI("SUP:TEL? 9,data", 
                                                    self.properties.address,
                                                    "uint")
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
    # end def
    
    def gui(self, parent_frame):
        """
        Load the GUI for this step
    
        @param parent_frame  (TK Frame)   The GUI frame to load the gui into
        """     
        # the step title
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = process_GUI.title_font, 
                           bg = process_GUI.default_color)
        self.Header.grid(row = 0, column=0, columnspan = 2, sticky = 'nsew')
        
        # the body text for the step
        self.body = TK.Label(parent_frame, text = self.text)
        self.body.config(font = process_GUI.label_font, 
                           bg = process_GUI.default_color)
        self.body.grid(row = 1, column=0, columnspan = 2, sticky = 'nsew')          
        
        if self.no_aardvark:
            # if arrdvark communications were unsuccessful print an error
            self.error_label = TK.Label(parent_frame, 
                                        text = "No Aardvark Connected")
            self.error_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.error_label.grid(row = 2, column=0, columnspan = 2)   
        
        else:
            # Aardvark communications were successful so load the rest of the GUI
        
            # Serial number title        
            self.serial_label = TK.Label(parent_frame, text = "Serial Number:")
            self.serial_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.serial_label.grid(row = 2, column=0, sticky = 'e')
            
            # Serial number display
            self.serial = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.serial.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.serial.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            self.serial.insert(0, str(self.serial_number))
            
            # Button to trigger the updating process
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
        """
        Deconstruct the GUI for this step
        """
        # remove the fixed items        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            # if an aardvark was not found remove the error label
            self.error_label.grid_forget()
            
        else:
            # if an aardvark was found remove all other items
            self.serial_label.grid_forget()
            self.serial.grid_forget()
            self.update_button.grid_forget()
        # end if
    #end def
    
    def get_sn(self):
        """
        Function to find the desired serial number that was entered in the gui.
        
        @return   (string)     The serial number to be set.
        """        
        # read the serial number from the gui
        serial_text = self.serial.get()
        
        # verify if the serial number is valid
        if serial_text.isdigit():
            # is a good serial number so return it
            return serial_text
            
        else:
            # the serial number is not valid
            print '*** Requested Serial Number is not valid, '\
                  'reverting to default ***'
            # return the default serial number
            return '0'
        # end if    
    # end def    
    
    def update_command(self, event):
        """
        Function that gets called when the update button is pressed. 
    
        Updates the module serial number
        """   
        # get the desired serial number
        serial_text = self.get_sn()
        
        # calculate the unlock key for the non volatile memory commands
        nvm_key = self.serial_number + 12345
        
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found, send the commands to unlock the NVM,
                # update the serial number and write it to NVM
                AARD.send_SCPI("SUP:NVM UNLOCK,"+str(nvm_key), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM SERIAL,"+serial_text, 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM WRITE,1", 
                               self.properties.address)
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
    #end def
#end class 

class _I2C_address:
    """
    Class that manages setting of the module I2C address

    @attribute properties    (SUP_process.process_properties) 
                                          Denotes propeties of the step
    @attribute title          (String)    Title text to display
    @attribute text           (String)    Body text to display
    @attribute Header         (TK label)  The title as displayed in the GUI
    @attribute body           (TK label)  Body text display in GUI
    @attribute error_label    (TK label)  Text to display if there is an error
    @attribute no_aardvark    (bool)      True is a connection to an aardvark 
                                          has been made, False otherwise.
    @attribute address_label  (TK label)  I2C Address title
    @attribute address_entry  (TK Entry)  I2C address Display
    @attribute update_button  (TK Button) Button to start the I2C address 
                                          setting action
    """      
    def __init__(self, properties):
        """
        Initialise the I2C address setting task
    
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """      
        # define the title of the step
        self.title = "Update the " + properties.module + " I2C Address"
        
        # define the body text for the step
        self.text = "Enter the desired I2C in the box and then " +\
            "press \"update\" to update\nthe module's I2C Address.\n" +\
            "Press next when you have finished."
        
        # initialise attributes
        self.no_aardvark = False
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step:
    
        Check if the Aardvark is present.
        """         
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found, do nothing
                next
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
    # end def
    
    def gui(self, parent_frame):
        """
        Load the GUI for this step
    
        @param parent_frame  (TK Frame)   The GUI frame to load the gui into
        """        
        # the step title 
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = process_GUI.title_font, 
                           bg = process_GUI.default_color)
        self.Header.grid(row = 0, column=0, columnspan = 2, sticky = 'nsew')
        
        # the body text for the step
        self.body = TK.Label(parent_frame, text = self.text)
        self.body.config(font = process_GUI.label_font, 
                           bg = process_GUI.default_color)
        self.body.grid(row = 1, column=0, columnspan = 2, sticky = 'nsew')          
        
        if self.no_aardvark:
            # if arrdvark communications were unsuccessful print an error
            self.error_label = TK.Label(parent_frame, 
                                        text = "No Aardvark Connected")
            self.error_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.error_label.grid(row = 2, column=0, columnspan = 2)   
        
        else:
            # Aardvark communications were successful so load the rest of the GUI
        
            # address title             
            self.address_label = TK.Label(parent_frame, 
                                  text = "I2C Address of " + self.properties.module + ":")
            self.address_label.config(font = process_GUI.label_font, 
                                      bg = process_GUI.default_color)
            self.address_label.grid(row = 2, column=0, sticky = 'e')
        
            # address display
            self.address_entry = TK.Entry(parent_frame, justify = 'left', 
                                          width = 7)
            self.address_entry.config(font = process_GUI.text_font, 
                                      highlightbackground= process_GUI.default_color)
            self.address_entry.grid(row = 2, column = 1, ipady = 3, sticky = 'w')     
            self.address_entry.insert(0, self.properties.address)
            
            # button to trigger address updating
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
        """
        Deconstruct the GUI for this step
        """        
        # remove the fixed items        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            # if an aardvark was not found remove the error label
            self.error_label.grid_forget()
            
        else:
            # if an aardvark was found remove all other items
            self.address_label.grid_forget()
            self.address_entry.grid_forget()
            self.update_button.grid_forget()
        # end if
    #end def
    
    def get_addr(self):
        """
        Function to find the desired address that was entered in the gui.
        
        @return     (address)         The address that will be set.
        """        
        # read the address from the gui
        address_text = self.address_entry.get()
        # verify if the address is valid
        if (address_text.startswith('0x') and len(address_text) ==4 and
            self.is_hex(address_text[2:])):
            
            # is a good address so return the address
            return address_text
            
        else:
            # the address is not valid
            print '*** Requested address is not valid, '\
                  'reverting to default ***'
            
            # return the default address
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
        """
        Function that gets called when the update button is pressed. 
        
        Updates the module I2C address
        """
        # retrieve the desired I2C address from the GUI
        address_text = self.get_addr()
        
        # extract the decimal address from that string
        address_num = int(address_text[2:], 16)
        
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found extract the NVM key from the 
                # serial number
                nvm_key = AARD.read_SCPI("SUP:TEL? 9,data", 
                                         self.properties.address, "uint")+12345   
                
                # send the commands to unlock the NVM, update the I2C address 
                # and write it to the NVM
                AARD.send_SCPI("SUP:NVM UNLOCK,"+str(nvm_key), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM I2C,"+str(address_num), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM WRITE,1", 
                               address_text)
                
                #update the address in the process properties
                self.properties.address = address_text
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
    #end def
#end class 

class _Update_OSCTUN:
    """
    Class that manages setting of the module Oscillator tuning parameter

    @attribute properties    (SUP_process.process_properties) 
                                          Denotes propeties of the step
    @attribute title          (String)    Title text to display
    @attribute text           (String)    Body text to display
    @attribute Header         (TK label)  The title as displayed in the GUI
    @attribute body           (TK label)  Body text display in GUI
    @attribute error_label    (TK label)  Text to display if there is an error
    @attribute no_aardvark    (bool)      True is a connection to an aardvark 
                                          has been made, False otherwise.
    @attribute tuning_param   (int)       The oscillator tuning parameter
    @attribute param_label    (TK label)  Tuning parameter title
    @attribute param          (TK Entry)  Tuning parameter display
    @attribute update_button  (TK Button) Button to start the tuning parameter 
                                          setting action
    """     
    def __init__(self, properties):
        """
        Initialise the Oscillator tuning parameter setting class
    
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """        
        # define the title of the step
        self.title = "Update the " + properties.module + \
            " oscillator tuning parameter"
        
        # define the body text for the step
        self.text = "Enter the desired tuning parameter in the box and then " +\
            "press \"update\" to update\nthe module's tuning parameter.\n" +\
            "Press next when you have finished."
        
        # initialise attributes 
        self.no_aardvark = False
        self.tuning_param = 0
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step:
    
        Read the tuning parameter from the module
        """         
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found, read the data
                self.tuning_param = AARD.read_SCPI("SUP:TEL? 11,data", 
                                                    self.properties.address,
                                                    "schar")
                
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
    # end def
    
    def gui(self, parent_frame):
        """
        Load the GUI for this step
    
        @param parent_frame  (TK Frame)   The GUI frame to load the gui into
        """
        # the step title          
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = process_GUI.title_font, 
                           bg = process_GUI.default_color)
        self.Header.grid(row = 0, column=0, columnspan = 2, sticky = 'nsew')
        
        # the body text for the step
        self.body = TK.Label(parent_frame, text = self.text)
        self.body.config(font = process_GUI.label_font, 
                           bg = process_GUI.default_color)
        self.body.grid(row = 1, column=0, columnspan = 2, sticky = 'nsew')          
        
        if self.no_aardvark:
            # if arrdvark communications were unsuccessful print an error
            self.error_label = TK.Label(parent_frame, 
                                        text = "No Aardvark Connected")
            self.error_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.error_label.grid(row = 2, column=0, columnspan = 2)   
        
        else:
            # Aardvark communications were successful so load the rest of the GUI
        
            # Tuning Parameter title          
            self.param_label = TK.Label(parent_frame, 
                                         text = "Tuning Parameter:")
            self.param_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.param_label.grid(row = 2, column=0, sticky = 'e')
            
            # Tuning Parameter display
            self.param = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.param.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.param.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            self.param.insert(0, str(self.tuning_param))
            
            # parameter setting starting button
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
        """
        Deconstruct the GUI for this step
        """        
        # remove the fixed items        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            # if an aardvark was not found remove the error label
            self.error_label.grid_forget()
            
        else:
            # if an aardvark was found remove all other items
            self.param_label.grid_forget()
            self.param.grid_forget()
            self.update_button.grid_forget()
        # end if
    #end def
    
    def get_param(self):
        """
        Function to find the desired tuning parameter that was entered 
        in the gui.
        
        @return     (int)         The tuning parameter that will be set.
        """        
        # read the parameter from the gui
        param_text = self.param.get()
        # verify if the parameter is valid
        try:
            int(param_text)
            # is a good parameter so set it as the parameter time
            return param_text
            
        except ValueError:
            # the parameter is not valid
            print '*** Requested Tuning Parameter is not valid, '\
                  'reverting to default ***'
            # restore the default parameter
            return '0'
        # end if    
    # end def    
    
    def update_command(self, event):
        """
        Function that gets called when the update button is pressed. 
        
        Updates the oscillator tuning parameter
        """
        # read the desired parameter from the GUI
        param_text = self.get_param()
        
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found, extract the device NVM key.
                nvm_key = AARD.read_SCPI("SUP:TEL? 9,data", 
                                         self.properties.address, "uint")+12345   
                
                # unlock the module NVM, set the tuning parameter and write it 
                # to the NVM
                AARD.send_SCPI("SUP:NVM UNLOCK,"+str(nvm_key), 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM OSCTUN,"+param_text, 
                               self.properties.address)
                AARD.send_SCPI("SUP:NVM WRITE,1", 
                               self.properties.address)
                
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
    #end def
#end class 

class _Address_request:
    """
    Class that requests teh I2C address from the user.

    @attribute properties      (SUP_process.process_properties) 
                                            Denotes propeties of the step
    @attribute title           (String)     Title text to display
    @attribute text            (String)     Body text to display
    @attribute Header          (TK label)   The title as displayed in the GUI
    @attribute body            (TK label)   Body text display in GUI
    @attribute address_label   (TK label)   address title
    @attribute address_entry   (TK Entry)   address display
    """      
    def __init__(self, properties):
        """
        Initialise the address request class
    
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """        
        # define the title of the step
        self.title = "Enter the current I2C Address of the " + properties.module
        
        # define the body text for the step
        self.text = "The default address has been entered for you" 
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step:
    
        Do nothing
        """         
        next
    # end def
    
    def gui(self, parent_frame):
        """
        Load the GUI for this step
    
        @param parent_frame  (TK Frame)   The GUI frame to load the gui into
        """
        # the step title             
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = process_GUI.title_font, 
                           bg = process_GUI.default_color)
        self.Header.grid(row = 0, column=0, columnspan = 2, sticky = 'nsew')
        
        # the body text for the step
        self.body = TK.Label(parent_frame, text = self.text)
        self.body.config(font = process_GUI.label_font, 
                           bg = process_GUI.default_color)
        self.body.grid(row = 1, column=0, columnspan = 2, sticky = 'nsew')          
        
        # the address title
        self.address_label = TK.Label(parent_frame, 
                                      text = "I2C Address of " + \
                                      self.properties.module + ":")
        self.address_label.config(font = process_GUI.label_font, 
                             bg = process_GUI.default_color)
        self.address_label.grid(row = 2, column=0, sticky = 'e')
        
        # the address entry box
        self.address_entry = TK.Entry(parent_frame, justify = 'left', width = 7)
        self.address_entry.config(font = process_GUI.text_font, 
                            highlightbackground= process_GUI.default_color)
        self.address_entry.grid(row = 2, column = 1, ipady = 3, sticky = 'w')     
        self.address_entry.insert(0, self.properties.address)
    
    def close(self):
        """
        Deconstruct the GUI for this step
        """        
        # remove the fixed items        
        self.Header.grid_forget()
        self.body.grid_forget()
        
        # retrieve the address from the GUI
        addr = self.get_addr()
        
        # if the address was acceptible then update the process properties
        if addr != '0':
            self.properties.address = addr
        #end if
        
        # remove the module specific items   
        self.address_label.grid_forget()
        self.address_entry.grid_forget()
    #end def
    
    def get_addr(self):
        """
        Function to find the desired address that was entered in the gui.
        
        @return     (int)         The address to be used for the process
        """
        # read the address from the gui
        address_text = self.address_entry.get()
        # verify if the address is valid
        if (address_text.startswith('0x') and len(address_text) ==4 and
            self.is_hex(address_text[2:])):
            
            # is a good address so return it
            return address_text
            
        else:
            # the address is not valid
            print '*** Requested address is not valid, '\
                  'reverting to default ***'
            # retun zero
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

#
# -------
# Templates

class Template_Task:
    """
    Template for a class that describes a step in a process.
    Elelments included in this template must be preserved.
    
    Essential attributes: 
    @attribute properties    (SUP_process.process_properties) 
                                             Denotes propeties of the step
    @attribute title         (String)        Title text to display
    @attribute text          (String)        Body text to display
    @attribute Header        (TK label)      The title as displayed in the GUI
    @attribute body          (TK label)      Body text display in GUI
    @attribute error_label   (TK label)      Text to display if there is an error
    @attribute no_aardvark   (bool)          True is a connection to an aardvark 
                                             has been made, False otherwise.
                                             
    Other attributes can be added as needed
    """
    def __init__(self, properties):
        """
        Initialise the Class
        
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """
        # define the title of the step
        self.title = "Title for the new step"
        
        # define the body text for the step
        self.text = "Body text to be printed in the GUI"
        
        # initialise attributes 
        self.no_aardvark = False
        # include other attributes as needed
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step, must be present, may be nothing.
        
        This function runs before the GUI is loaded, while the please wait 
        message is displayed.
        
        If the step uses an Aarvark attempt to communicate with it here and 
        set self.no_aardvark if this communication fails.
        """
        # trivial execution 
        self.no_aardvark = False
    # end def
    
    def gui(self, parent_frame):
        """
        This function lodas the gui elements associated with this step.
        
        @param parent_frame  (TK Frame)   The area in the GUI where these 
                                          elements can be placed.
        """
        # the step title
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = process_GUI.title_font, 
                           bg = process_GUI.default_color)
        self.Header.grid(row = 0, column=0, columnspan = 2, sticky = 'nsew')
        
        # the body text for the step
        self.body = TK.Label(parent_frame, text = self.text)
        self.body.config(font = process_GUI.label_font, 
                           bg = process_GUI.default_color)
        self.body.grid(row = 1, column=0, columnspan = 2, sticky = 'nsew')        
        
        # This check is only required if the step 
        # requires the use of the arrdvark
        if self.no_aardvark:
            # if arrdvark communications were unsuccessful print an error
            self.error_label = TK.Label(parent_frame, 
                                        text = "No Aardvark Connected")
            self.error_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.error_label.grid(row = 2, column=0, columnspan = 2)   
        
        else:
            # Aardvark communications were successful so load the rest of the GUI
            # add step specific GUI elements here
            next
    #end def
    
    def close(self):
        """
        Deconstruct the GUI for this step
        """
        # remove the fixed items
        self.Header.grid_forget()
        self.body.grid_forget()
        
        if self.no_aardvark:
            # if an aardvark was not found remove the error label
            self.error_label.grid_forget()
            
        else:
            # if an aardvark was found remove all other items
            # grid_forget all step specific GUI elements here so that they 
            # are removed from the GUI
            next
        # end if
    #end def
#end class

class Template_Process(object):
    """
    The class that contains all the information for a process
    
    @attribute properties  (SUP_process.process_properties) Denotes propeties 
                                                            of BM2 process
    @attribute process     (list)                           Steps in the process
    """
    # define the properties of the Process using the module name and its 
    # I2C address.
    # Initialisation for SUP steps
    properties = process_properties("MOD", "0x5C")
    # Initialisation for Module steps
    #properties = SUP_process.process_properties("MOD", "0x5C")    
    
    # get the SupMCU process list
    # declaration for a SUP step
    __sup_process = SupMCU_process(properties)
    # declaration for a module step
    #__sup_process = SUP_process.SupMCU_process(properties)    
    
    # initialise the module specific process steps
    __Test = Template_Task(properties)
    
    # construct the list of all steps in the process
    process = __sup_process.process + \
             [__Test]     
#end object    




