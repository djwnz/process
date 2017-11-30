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

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.1.0' #Versioning: http://www.python.org/dev/peps/pep-0386/

import Tkinter as TK
from functools import partial

default_color = '#E1E5E7'
title_font = "Arial 16 bold"
label_font = "Arial 10"
button_font = "Arial 10 bold"
text_font = "Arial 9"

class process_window:
    
    def __init__(self, input_struct):
        
        if input_struct == None:
            input_struct = test_struct()
        # end if
        
        self.root = TK.Tk()
        self.root.geometry('800x600')
        self.root.config(bg = default_color) # to show through the gaps between frames
        
        self.total_steps = len(input_struct.process)
        self.current_step = 0
        
        self.process = input_struct.process 
        
        Header = TK.Label(self.root, text = input_struct.properties.title)
        Header.config(font = title_font, bg = default_color)
        Header.grid(row = 0, column=0, sticky = 'nsew')
        
        button_frame = TK.Frame(self.root)
        button_frame.config(bg = default_color)
        button_frame.grid(row = 2, column = 0, sticky='sew')
        
        if self.total_steps == 1:
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
        
        self.progress_label = TK.Label(button_frame, 
                                       text = "step 1/"+str(self.total_steps))
        self.progress_label.config(font = label_font, bg = default_color)
        self.progress_label.grid(row = 0, column=1, sticky = 'nsew')        
        
        self.back_button = TK.Button(button_frame, text = 'Back', 
                                     command = partial(self.back_command, self), 
                                     activebackground = 'green', width = 15)
        self.back_button.config(font = button_font, bg = default_color, 
                                highlightbackground= default_color, 
                                state = 'disabled')
        self.back_button.grid(row = 0, column=0, sticky='w', padx=10, pady=10) 
        
        self.back_state = 'disabled'
        
        self.useable_frame = TK.Frame(self.root)
        self.useable_frame.config(bg = default_color)
        self.useable_frame.grid(row = 1, column = 0)
        
        self.wait_label = TK.Label(self.useable_frame, 
                                   text = "Please wait, task in progress")
        self.wait_label.config(font = label_font, bg = default_color)        
        
        self.root.rowconfigure(0, weight = 1, minsize = 50)
        self.root.rowconfigure(1, weight = 1, minsize = 500)
        self.root.rowconfigure(2, weight = 1, minsize = 50)
        
        self.root.columnconfigure(0, weight = 1, minsize = 800)
        button_frame.columnconfigure(0, weight = 1, minsize = 200)
        button_frame.columnconfigure(1, weight = 1, minsize = 200)
        button_frame.columnconfigure(2, weight = 1, minsize = 200)
        
        self.root.resizable(0,0)
        
    #end def
    
    def start(self):
        self.root.after(10, self.root.update())
        self.root.after(100, self.initial_display())
        self.root.mainloop()
        
    #end def
    
    def initial_display(self):
        self.please_wait('on')
        self.process[self.current_step].execute()
        self.please_wait('off')
        self.process[self.current_step].gui(self.useable_frame)
    #end def
    
    def set_step(self, step):
        self.progress_label.config(text = "step " + str(step+1) + "/" + 
                                   str(self.total_steps))
    #end def
    
    def next_command(self, event):
        self.process[self.current_step].close()
        self.current_step += 1
        
        self.set_step(self.current_step)
        self.please_wait('on')
        self.process[self.current_step].execute()
        self.please_wait('off')        
        self.process[self.current_step].gui(self.useable_frame)
        
        self.back_button.config(state = 'normal')
        
        if self.current_step == (self.total_steps-1):
            self.next_button.config(text = 'Finish',
                                    command = partial(self.finish_command, self))
        #end def
        
    def please_wait(self, state):
        if state == 'on':
            self.back_state = str(self.back_button['state'])
            self.next_state = str(self.next_button['state'])            
            if self.back_state != 'disabled':
                self.back_button.config(state='disabled')
            #end if
            if self.next_state != 'disabled':
                self.next_button.config(state='disabled')
            #end if            
            self.wait_label.grid(row = 0, column=0)   
            self.root.update()
            
        else:
            self.wait_label.grid_forget()  
            if self.back_state != 'disabled':
                self.back_button.config(state=self.back_state)
            #end if
            if self.next_state != 'disabled':
                self.next_button.config(state=self.next_state)
            #end if             
            
    #end def
    
    def back_command(self, event):
        self.process[self.current_step].close()
        self.current_step -= 1
        
        self.set_step(self.current_step)
        
        self.please_wait('on')
        self.process[self.current_step].execute()
        self.please_wait('off')        
        self.process[self.current_step].gui(self.useable_frame)
        
        self.next_button.config(text = "Next", 
                                command = partial(self.next_command, self))
        
        if self.current_step == 0:
            self.back_button.config(state = 'disabled')
        #end def
            
    #end def   
    
    def finish_command(self, event):
        self.root.destroy()
    #end def
        

# end class
        
        
def test():
    """
    Test code for this module.
    """
    pw = process_window(None)
    
    pw.start()
    
# end def

class test_struct():
    def __init__(self):
        self.title = "This is a test program"
        
        step1 = test_step("This is step 1")
        step2 = test_step("This is step 2")
        step3 = test_step("This is step 3")
        
        self.process = [step1, step2, step3]
    # end def
# end class

class test_step():
    def __init__(self, step_text):
        self.title = step_text
        
    # end def
    
    def execute(self):
        print "executing code for this step"
        
    # end def
    
    def gui(self, parent_frame):
        
        self.Header = TK.Label(parent_frame, text = self.title)
        self.Header.config(font = title_font, bg = default_color)
        self.Header.grid(row = 0, column=0, sticky = 'nsew')
        
        self.test_button = TK.Button(parent_frame, text = 'Test',
                                     command = partial(self.button_command, self), 
                                     activebackground = 'green', width = 15)
        self.test_button.config(font = button_font, bg = default_color, 
                               highlightbackground= default_color)
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

if __name__ == '__main__':
    # if this code is not running as an imported module run test code
    test()
# end if