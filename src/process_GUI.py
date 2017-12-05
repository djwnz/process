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
@package process_GUI
Module to handle the gui for the process
"""

__author__ = 'David Wright (david@asteriaec.com)'
__version__ = '0.1.0' #Versioning: http://www.python.org/dev/peps/pep-0386/

#
# -------
# Imports

import Tkinter as TK
from functools import partial

#
# -------
# Constants

default_color = '#E1E5E7'
title_font = "Arial 16 bold"
label_font = "Arial 10"
button_font = "Arial 10 bold"
text_font = "Arial 9"

#
# -------
# Classes

class process_window:
    """
    Class that controls the GUI and action events for the process module

    @attribute root           (TK root)   GUI root object
    @attribute total_steps    (int)       Number of steps in the process
    @attribute current_step   (int)       Current step in the process
    @attribute process        (list)      Tasks that form the process
    @attribute next_button    (TK Button) 'Next' Button
    @attribute next_state     (string)    State of the next button eg. 'disabled'
    @attribute progress_label (TK Label)  Displays current step in process
    @attribute back_button    (TK Button) 'Back' Button
    @attribute back_state     (string)    State of the next button eg. 'disabled'
    @attribute useable_frame  (TK Frame)  Area into which processes can have GUI
    @attribute wait_label     (TK Label)  Please wait message
    """     
    
    def __init__(self, input_struct):
        """
        Initialise the GUI
    
        @param[in] input_struct:  .properties: (SUP_process.process_properties)
                                               object containing properties of 
                                               the process
                                  .process     list of process steps
    """         
        if input_struct == None:
            #this is a testing code implementation, use the testing struct
            input_struct = _test_struct()
        # end if
        
        #construct the root window at 800x600 resolution
        self.root = TK.Tk()
        self.root.geometry('800x600')
        self.root.config(bg = default_color) # to show through the gaps between frames
        
        # count the number of steps and start at zero
        self.total_steps = len(input_struct.process)
        self.current_step = 0
        
        # copy the process steps into an attribute
        self.process = input_struct.process 
        
        # create the title header of the process GUI
        Header = TK.Label(self.root, text = input_struct.properties.title)
        Header.config(font = title_font, bg = default_color)
        Header.grid(row = 0, column=0, sticky = 'nsew')
        
        # Create a frame for the buttons
        button_frame = TK.Frame(self.root)
        button_frame.config(bg = default_color)
        button_frame.grid(row = 2, column = 0, sticky='sew')
        
        # Create the next button
        if self.total_steps == 1:
            # If there is only one step the Next button should say 'Finish'
            self.next_button = TK.Button(button_frame, text = 'Finish', 
                                         command = partial(self.finish_command, self), 
                                         activebackground = 'green', width = 15)
        else:
            self.next_button = TK.Button(button_frame, text = 'Next', 
                                         command = partial(self.next_command, self), 
                                         activebackground = 'green', width = 15)     
        #end if
        
        self.next_button.config(font = button_font, bg = default_color, 
                               highlightbackground= default_color)
        self.next_button.grid(row = 0, column=2, sticky='e', padx=10, pady=10)  
        self.next_state = 'normal'
        
        # create a lable that displays the process the user has made through 
        # the process
        self.progress_label = TK.Label(button_frame, 
                                       text = "step 1/"+str(self.total_steps))
        self.progress_label.config(font = label_font, bg = default_color)
        self.progress_label.grid(row = 0, column=1, sticky = 'nsew')        
        
        # create the back button, initially disabled as it is the first step
        self.back_button = TK.Button(button_frame, text = 'Back', 
                                     command = partial(self.back_command, self), 
                                     activebackground = 'green', width = 15)
        self.back_button.config(font = button_font, bg = default_color, 
                                highlightbackground= default_color, 
                                state = 'disabled')
        self.back_button.grid(row = 0, column=0, sticky='w', padx=10, pady=10) 
        self.back_state = 'disabled'
        
        # create a frame into which the process steps can load their 
        # GUI elements
        self.useable_frame = TK.Frame(self.root)
        self.useable_frame.config(bg = default_color)
        self.useable_frame.grid(row = 1, column = 0)
        
        # create a please wait label for in between tasks
        self.wait_label = TK.Label(self.useable_frame, 
                                   text = "Please wait, task in progress")
        self.wait_label.config(font = label_font, bg = default_color)        
        
        #define the size of the rows
        self.root.rowconfigure(0, weight = 1, minsize = 50)
        self.root.rowconfigure(1, weight = 1, minsize = 500)
        self.root.rowconfigure(2, weight = 1, minsize = 50)
        
        #define the size of the columns
        self.root.columnconfigure(0, weight = 1, minsize = 800)
        button_frame.columnconfigure(0, weight = 1, minsize = 200)
        button_frame.columnconfigure(1, weight = 1, minsize = 200)
        button_frame.columnconfigure(2, weight = 1, minsize = 200)
        
        #prevent resizing
        self.root.resizable(0,0) 
    #end def
    
    def start(self):
        """
        Function to start the GUI
        """         
        # schedule GUI initialisation to occur after the root boots up.
        self.root.after(10, self.root.update())
        self.root.after(100, self.initial_display())
        
        #start the gui mainloop
        self.root.mainloop()
        
    #end def
    
    def initial_display(self):
        """
        Set up the first step in the process
        """         
        # display the please wait message
        self.please_wait('on')
        
        # run the first step's code
        self.process[self.current_step].execute()
        
        # take the please wait message down and show the first step's GUI.
        self.please_wait('off')
        self.process[self.current_step].gui(self.useable_frame)
    #end def
    
    def set_step(self, step):
        """
        Update the step count in the GUI
        
        @param[in]    step:     The step number to update to (int)
        """         
        self.progress_label.config(text = "step " + str(step+1) + "/" + 
                                   str(self.total_steps))
    #end def
    
    def next_command(self, event):
        """
        Function to update the gui with the next step in the sequence
        """
        
        # close the previous step in the process
        self.process[self.current_step].close()
        
        # increment the step counter
        self.current_step += 1
        
        # update the step counter in the GUI
        self.set_step(self.current_step)
        
        # display please wait message while running the new step's code
        self.please_wait('on')
        self.process[self.current_step].execute()
        self.please_wait('off')        
        
        # set up the gui for the next step
        self.process[self.current_step].gui(self.useable_frame)
        
        # allow the back button to be used as this cannot be the first step
        self.back_button.update()
        self.back_button.config(state = 'normal')
        
        # if this is the last step change the next button to be a finish button
        if self.current_step == (self.total_steps-1):
            self.next_button.config(text = 'Finish',
                                    command = partial(self.finish_command, self))
        #end def
        
    def please_wait(self, state):
        """
        Function to display a please wait message in the GUI while a task is
        in progress
        
        @param[in]   state   either 'on' or 'off': do or don't display the 
                                                   message
        """
        if state == 'on':
            # display the message
            
            # store the states of the buttons
            self.back_state = str(self.back_button['state'])
            self.next_state = str(self.next_button['state'])    
            
            # disable both the buttons
            self.back_button.config(state='disabled')
            self.next_button.config(state='disabled')  
            self.back_button.update()
            self.next_button.update()             
            
            # display the message and update the GUI
            self.wait_label.grid(row = 0, column=0)   
            self.root.update()
            
        else:
            # remove the message
            
            # delete the message from the GUI
            self.wait_label.grid_forget() 
            
            # return the buttons to their previoud state update to ignore clicks
            self.back_button.update()
            self.next_button.update()              
            self.back_button.config(state=self.back_state)
            self.next_button.config(state=self.next_state)
        #end if              
    #end def
    
    
    def back_command(self, event):
        """
        Function to update the gui with the previous step in the sequence
        """        
        
        # terminate the current step
        self.process[self.current_step].close()
        
        # decrement the step counter
        self.current_step -= 1
        
        # update the progress display
        self.set_step(self.current_step)
        
        # display the please wait message while the new step's code is executed
        self.please_wait('on')
        self.process[self.current_step].execute()
        self.please_wait('off') 
        
        # Load the new step's GUI
        self.process[self.current_step].gui(self.useable_frame)
        
        # make the next button say 'next'
        self.next_button.update()
        self.next_button.config(text = "Next", 
                                command = partial(self.next_command, self))
        
        # If we are back at the first step disable the back button
        if self.current_step == 0:
            self.back_button.config(state = 'disabled')
        #end def
    #end def   
    
    def finish_command(self, event):
        """
        Function to call when the Finish button is pressed
        """
        # terminate the current step
        self.process[self.current_step].close()
        
        # close the GUI
        self.root.destroy()
    #end def
# end class


# test step to use in the test struct for testing purposes
class _test_step():
    def __init__(self, step_text):
        # create the title
        self.title = step_text
    # end def
    
    def execute(self):
        # print a statement when the step is executed
        print "executing code for this step"
    # end def
    
    def gui(self, parent_frame):
        
        # create a title for the step
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = title_font, bg = default_color)
        self.Header.grid(row = 0, column=0, sticky = 'nsew')
        
        # create a testing button for the step
        self.test_button = TK.Button(parent_frame, text = 'Test',
                                     command = partial(self.button_command, self), 
                                     activebackground = 'green', width = 15)
        self.test_button.config(font = button_font, bg = default_color, 
                               highlightbackground= default_color)
        self.test_button.grid(row = 1, column=0, sticky='e', padx=10, pady=10)  
    #end def
    
    def close(self):
        # delete the title and the button when the step is closed
        self.test_button.grid_forget()
        self.Header.grid_forget()
    #end def
    
    def button_command(self, event):
        # function to call when the button is pressed, print a message
        # NOTE: not visible in the GUI
        print "button has been pressed"
    #end def
#end class

# properties to use when testing the module
class _test_properties(object):
    title = "Test process for process_GUI.py "
#end class

# struct to use for testing this module
class _test_struct(object):
    # title of the step
    title = "This is a test program"
    
    #define testing properties
    properties = _test_properties()
    
    # create the steps
    __step1 = _test_step("This is step 1")
    __step2 = _test_step("This is step 2")
    __step3 = _test_step("This is step 3")
    
    # construct a process out of the steps
    process = [__step1, __step2, __step3]
# end class

#
# -------
# Private Functions

def _test():
    """
    Test code for this module.
    """
    pw = process_window(None)

    pw.start()

# end def

if __name__ == '__main__':
    # if this code is not running as an imported module run test code
    _test()
# end if