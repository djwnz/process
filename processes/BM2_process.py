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
import SUP_process

#
# -------
# Classes

class _BM2_verification:
    """
    Class that manages verification of BM2 telemetry
 
    @attribute properties    (SUP_process.process_properties) 
                                             Denotes propeties of the step
    @attribute title         (String)        Title text to display
    @attribute text          (String)        Body text to display
    @attribute Header        (TK label)      The title as displayed in the GUI
    @attribute body          (TK label)      Body text display in GUI
    @attribute error_label   (TK label)      Text to display if there is an error
    @attribute no_aardvark   (bool)          True is a connection to an aardvark 
                                             has been made, False otherwise.
    @attribute voltage_read  (float)         Voltage read from the BM2
    @attribute temp_read     (float)         Temperature read from the BM2
    @attribute SOC_read      (int)           State of Charge read from the BM2
    @attribute voltage_label (TK label)      Voltage measurement title
    @attribute voltage       (TK Entry)      Voltage Measurement Display
    @attribute SOC_label     (TK label)      State of Charge measurement title
    @attribute SOC           (TK Entry)      State of Charge Measurement Display
    @attribute temp_label    (TK label)      Temperature measurement title
    @attribute temp          (TK Entry)      Temperature Measurement Display
    """    
    def __init__(self, properties):
        """
        Initialise the BM2 verification class
        
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """
        # define the title of the step
        self.title = "Verify BM2 Values"
        
        # define the body text for the step
        self.text = "Check these values against what you can measure/" +\
            "what you expect.\n Press next when you have done this."
        
        # initialise attributes 
        self.no_aardvark = False
        self.voltage_read = 0.0
        self.temp_read = 0.0
        self.SOC_read = 0
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step:
        
        Read Voltage, State of Charge and Temperature from the BM2 if 
        communications canbe established
        """
        
        with process_SCPI.aardvark() as AARD:
            # initialise the assrdvark
            if AARD.port != None:
                # if an aardvark was found, read the data
                self.voltage_read = AARD.read_SCPI("BM2:TEL? 9,data", 
                                                   self.properties.address, 
                                                   "uint")/1000.0
                self.temp_read = AARD.read_SCPI("BM2:TEL? 8,data", 
                                                self.properties.address, 
                                                "uint")/100.0
                self.SOC_read = AARD.read_SCPI("BM2:TEL? 13,data", 
                                               self.properties.address, "uint")
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
    # end def
    
    def gui(self, parent_frame):
        """
        Load the GUI for this step
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
            
            # Voltage title
            self.voltage_label = TK.Label(parent_frame, text = "Voltage (V):")
            self.voltage_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.voltage_label.grid(row = 2, column=0, sticky = 'e')
            
            # Voltage display
            self.voltage = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.voltage.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.voltage.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            self.voltage.insert(0, str(self.voltage_read))
            
            # Temperature title
            self.temp_label = TK.Label(parent_frame, 
                                       text = "Temperature (degC):")
            self.temp_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.temp_label.grid(row = 3, column=0, sticky = 'e')
            
            # Temperature display
            self.temp = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.temp.config(font = process_GUI.text_font, 
                             highlightbackground= process_GUI.default_color)
            self.temp.grid(row = 3, column = 1, ipady = 3, sticky = 'w')
            self.temp.insert(0, str(self.temp_read))
            
            # State of Charge Title
            self.SOC_label = TK.Label(parent_frame, text = "SOC (%):")
            self.SOC_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.SOC_label.grid(row = 4, column=0, sticky = 'e')     
            
            # State of Charge Dispay
            self.SOC = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.SOC.config(font = process_GUI.text_font, 
                            highlightbackground= process_GUI.default_color)
            self.SOC.grid(row = 4, column = 1, ipady = 3, sticky = 'w')
            self.SOC.insert(0, str(self.SOC_read))
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
            self.voltage_label.grid_forget()
            self.voltage.grid_forget()
            self.temp_label.grid_forget()
            self.temp.grid_forget()
            self.SOC_label.grid_forget()
            self.SOC.grid_forget()
        # end if
    #end def
#end class    

class _BM2_heater_test:
    """
    Class that manages testing the BM2 heaters

    @attribute properties      (SUP_process.process_properties) 
                                            Denotes propeties of the step
    @attribute title           (String)     Title text to display
    @attribute text            (String)     Body text to display
    @attribute Header          (TK label)   The title as displayed in the GUI
    @attribute body            (TK label)   Body text display in GUI
    @attribute error_label     (TK label)   Text to display if there is an error
    @attribute no_aardvark     (bool)       True is a connection to an aardvark 
                                            has been made, False otherwise.
    @attribute initial_current (float)      Initial current read from the BM2
    @attribute voltage         (float)      Voltage read from the BM2
    @attribute power_label     (TK Label)   Power calculation title
    @attribute power           (TK Entry)   Power calculation display
    @attribute heater_button   (TK Button)  Button to control the heater test
    """       
    def __init__(self, properties):
        """
        Initialise the BM2 verification class
    
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """
        # define the title of the step
        self.title = "Test the operation of the heater"
        
        # define the body text for the step
        self.text = "The heater will be tested by turning it on and off " +\
            "again and calculating\nthe power drawn by the heaters.\n" +\
            "For 2 and 4 cell batteries this should be approximately 10W and " +\
            "for 3 cells, 12W" 
        
        # initialise attributes 
        self.no_aardvark = False
        self.initial_current = 0
        self.voltage = 0
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step:
    
        Read Voltage and Current from the BM2 if 
        communications can be established
        """        
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found, read the data
                self.initial_current = AARD.read_SCPI("BM2:TEL? 10,data", 
                                                      self.properties.address, 
                                                      "uint")/1000.0
                self.voltage = AARD.read_SCPI("BM2:TEL? 9,data", 
                                              self.properties.address, 
                                              "uint")/1000.0
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
        
            # Power title        
            self.power_label = TK.Label(parent_frame, 
                                        text = "Heater Power (W):")
            self.power_label.config(font = process_GUI.label_font, 
                                 bg = process_GUI.default_color)
            self.power_label.grid(row = 2, column=0, sticky = 'e')
            
            # Power display
            self.power = TK.Entry(parent_frame, justify = 'left', width = 7)
            self.power.config(font = process_GUI.text_font, 
                                highlightbackground= process_GUI.default_color)
            self.power.grid(row = 2, column = 1, ipady = 3, sticky = 'w')    
            
            # Heater test starting button
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
            self.power_label.grid_forget()
            self.power.grid_forget()
            self.heater_button.grid_forget()
        # end if
    #end def
    
    def heater_command(self, event):
        """
        Function that gets called when the heater button is pressed. 
        
        Performs the heater test
        """
        # calculate the initial power being consumed by the BM2
        rest_power = self.initial_current*self.voltage
        
        # initialise the new current measurement
        new_current = self.initial_current
        
        # remove the previous power measurement from the display
        self.power.delete(0, 'end')
        
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
            if AARD.port != None:
                # if an aardvark was found, command the heater on
                AARD.send_SCPI("BM2:HEA ON", self.properties.address)
                
                # wait for 2 seconds
                time.sleep(2)
                
                # read the new current
                new_current = AARD.read_SCPI("BM2:TEL? 10,data", 
                                             self.properties.address, 
                                             "int")/-1000.0    
                
                #comand the heater to turn off again
                AARD.send_SCPI("BM2:HEA OFF", self.properties.address)
                
            else:
                # no aardvark was found
                self.no_aardvark = True
            #end if
        # end with
        
        # calculate the power increase with the heaters on
        heater_power = (new_current * self.voltage) - rest_power
        
        #update the GUI with the new power value
        self.power.insert(0, str(heater_power))
    #end def
#end class   

class _Calibrate_Temp:
    """
    Class that manages calibrating the BM2 temperature sensors

    @attribute properties    (SUP_process.process_properties) 
                                          Denotes propeties of the step
    @attribute title          (String)    Title text to display
    @attribute text           (String)    Body text to display
    @attribute Header         (TK label)  The title as displayed in the GUI
    @attribute body           (TK label)  Body text display in GUI
    @attribute error_label    (TK label)  Text to display if there is an error
    @attribute no_aardvark    (bool)      True is a connection to an aardvark 
                                          has been made, False otherwise.
    @attribute temp_label     (TK label)  Temperature title
    @attribute temp           (TK Entry)  Temperature display
    @attribute cal_button     (TK Button) Button to start the calibration.
    """     
    def __init__(self, properties):
        """
        Initialise the Temperature calibration class
    
        @param  properties   (SUP_process.process_properties) 
                                             Denotes propeties of the step
        """        
        # define the title of the step
        self.title = "Calibrate the BM2 Temperature sensors"
        
        # define the body text for the step
        self.text = "Enter the current abbient temperature in the box below\n" +\
                    "Ensure that the battery has been at rest for at least an\n" +\
                    "hour before performing calibration.\n NOTE: This" +\
                    "calibration on calibrates the sensors managed by the\n" +\
                    "supMCU, the BQ temp sensors must be calibrated separately"
        
        # initialise attributes 
        self.no_aardvark = False
        
        # copy the properties
        self.properties = properties
    # end def
    
    def execute(self):
        """
        The code to run for this step:
    
        Check for a present Aardvark
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


class BM2_Process(object):
    """
    The class that represents the BM2 Process
    
    @attribute properties  (SUP_process.process_properties) Denotes propeties 
                                                            of BM2 process
    @attribute process     (list)                           Steps in the process
    """
    # define the properties of the Process
    properties = SUP_process.process_properties("BM2", "0x5C")
    
    # get the SupMCU process list
    __sup_process = SUP_process.SupMCU_process(properties)
    
    # initialise the BM2 process steps
    __verification = _BM2_verification(properties)
    __heater_test = _BM2_heater_test(properties)
    
    # construct the list of steps in the process
    process = __sup_process.process + \
             [__verification,
              __heater_test]     
#end object