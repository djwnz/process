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
        communications can be established
        """
        
        with process_SCPI.aardvark() as AARD:
            # initialise the aardvark
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