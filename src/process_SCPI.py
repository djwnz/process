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
@package process_SCPI
Module to handle sending and processing of scpi commands within process
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.1.0' #Versioning: http://www.python.org/dev/peps/pep-0386/

import aardvark_py
import time
from array import array
from struct import unpack

# ---------
# Constants

# I2C config
I2C = True
SPI = True
GPIO = False
Pullups = True
radix = 16
Bitrate = 100

class aardvark:
    
    def __init__(self):
        
        self.message = ''
        
        # configure Aardvark if available
        self.port = self.configure_aardvark()
        
        # The length of a name request in bytes
        self.name_size = 32
        
        # The length of the checksum in bytes
        self.chksum_size = 0
        
        # The length of the write flag element in bytes
        self.wflag_size = 1
        
        # The length of the timestamp in bytes
        self.time_size = 4
        
        # The leght of an ascii request in bytes
        self.ascii_size = 128 
        
    #end def
    
    def __enter__(self):
        return self
    # end def
    
    def __exit__(self, type, value, traceback):
        if self.port != None:
            aardvark_py.aa_close(self.port)
        #end if
    #end def
    
    def configure_aardvark(self):
        """ 
        Function to configure the aardvark for pySCPI operation if there is one
        available.
        
        @return  (aardvark_py.aardvark)   The handle of the aardvark to be used
                                          'None' if there is not one available
        """
        # define the handle to return
        Aardvark_in_use = None
        
        # find all connected aardvarks
        AA_Devices = aardvark_py.aa_find_devices(1)
        
        # define a port mask
        Aardvark_port = 8<<7
        
        # assume that an aardvark can be found until proved otherwise
        Aardvark_free = True
        
        # Check if there is an Aardvark present
        if (AA_Devices[0] < 1):
            # there is no aardvark to be found
            self.message = '*** No Aardvark is present ***'
            Aardvark_free = False
            
        else:
            # there is an aardvark connected to select the first one if there
            # are many
            Aardvark_port = AA_Devices[1][0]
        # end if
        
        
        # If there is an Aardvark there is it free?
        if Aardvark_port >= 8<<7 and Aardvark_free:
            # the aardvark is not free
            self.message = '*** Aardvark is being used, '\
                           'disconnect other application or Aardvark device ***'
            # close the aardvark
            aardvark_py.aa_close(Aardvark_port)
            Aardvark_free = False
            
        elif Aardvark_free:
            # Aardvark is available so configure it
            
            # open the connection with the aardvark
            Aardvark_in_use = aardvark_py.aa_open(Aardvark_port)
            
            # set it up in teh mode we need for pumpkin modules
            aardvark_py.aa_configure(Aardvark_in_use, 
                                     aardvark_py.AA_CONFIG_SPI_I2C)
            
            # default to both pullups on
            aardvark_py.aa_i2c_pullup(Aardvark_in_use, 
                                      aardvark_py.AA_I2C_PULLUP_BOTH)
            
            # set the bit rate to be the default
            aardvark_py.aa_i2c_bitrate(Aardvark_in_use, Bitrate)
            
            # free the bus
            aardvark_py.aa_i2c_free_bus(Aardvark_in_use)
            
            # delay to allow the config to be registered
            aardvark_py.aa_sleep_ms(200)    
            
        # end if    
        
        return Aardvark_in_use
    # end def        
    
    def send_SCPI(self, command, address):
        """
        Function to send a SCPI command to the slave device
        
        @param[in]    command:         the command to send (string)
        @param[in]    address:         the decimal address to write to (int)
        """  
        
        # convert the data into a list of bytes and append the terminator
        write_data = list(command)
        write_data = [ord(item) for item in write_data]
        write_data.append(0x0a)
        
        # convert to an array to be compiant with the aardvark
        data = array('B', write_data)  
        
        
        # Write the data to the slave device
        aardvark_py.aa_i2c_write(self.port, int(address, 16), 
                                 aardvark_py.AA_I2C_NO_FLAGS, data)
        
        # pause
        aardvark_py.aa_sleep_ms(400)
        
    # end def
    
    def read_SCPI(self, command, address, return_format):
        """
        Function to send a SCPI command to the slave device
        
        @param[in]    command:         the command to send (string)
        @param[in]    address:         the decimal address to write to (int)
        @param[out]   result:          the variable to store the data in
        """  
        # acceptible data formats
        acceptible_formats = {'int':2, 'long':4, 'long long':8, 'uint':2, 
                              'double':8, 'float':4, 'char':1, 'schar':1, 
                              'hex':1, 'name':self.name_size, 
                              'ascii':self.ascii_size, 'string':self.ascii_size}
        
        # length of preamle
        preamble_length = self.wflag_size + self.time_size + self.chksum_size
        
        # define the read legth as 0
        read_length = 0
        
        # continuation flag
        perform_read = True
        
        # determin the correct read length
        if type(return_format) == list:
            # retun type is a list of items so it has a preamble
            read_length += preamble_length
            
            # add up all of the lengths of the list items
            for item in return_format:
                # ensure each format specifier is acceptible
                if item in acceptible_formats:
                    read_length += acceptible_formats(item)
                    
                else:
                    # error
                    self.message = '***'+ item + \
                        " is an unacceptible format ***"
                    perform_read = False
                    break
                # end if
            # end for
            
        elif return_format in acceptible_formats:
            # return type is an acceptible format
            
            # add preamble to data length if required
            if return_format == 'ascii':
                read_length = acceptible_formats['ascii']
                
            else:
                read_length = preamble_length + acceptible_formats[return_format]
            # end if
        
        else:
            # format is not acceptible
            self.message = '***'+ return_format + " is an unacceptible format ***"            
            perform_read = False
        # end if
        
        if perform_read:
            self.send_SCPI(command, address)
            
            # define array to read data into
            data = array('B', [1]*read_length) 
            
            # read from the slave device
            read_data = aardvark_py.aa_i2c_read(self.port, int(address, 16), 
                                                aardvark_py.AA_I2C_NO_FLAGS, 
                                                data) 
            
            raw_data = list(read_data[1])
            
            # pause
            aardvark_py.aa_sleep_ms(400)         
            
            # extract the data from the returned raw data
            if type(return_format) == list:
                # there are multiple items in the return list
                return_list = []
                
                # remove the preamble
                data = raw_data[preamble_length:]
                
                for item in return_format:
                    # extract each item individually and append to list
                    return_list = return_list + \
                        [extract_data(data[0:accptiable_formats[item]], item)]
                    
                    # shorten data list to what remains
                    data = data[acceptiable_formats[item]:]
                # end for
                
                return return_list
                    
            else:
                # extract the sole peice of data
                if return_format != 'ascii':
                    data = raw_data[preamble_length:]
                # end if
                return extract_data(data, return_format)
            #end if
            
        # end if
        
        # if you make it this far there was a problem with the format strings
        return None
    # end def    
# end class
        
def extract_data(data, format_string):
    if format_string in ['ascii', 'string', 'name']:
        if 0 in data:
            # terminate printing at the null terminator 
            # of the string
            return ''.join([chr(x) for x in data[0:data.index(0)]])
        else:
            # no null terminator
            return ''.join([chr(x) for x in data])
        # end if        
    elif format_string == 'int':
        return unpack('<h', ''.join([chr(x) for x in data]))[0]
        
    elif format_string == 'long':
        return unpack('<l', ''.join([chr(x) for x in data]))[0]
        
    elif format_string == 'long long':
        return unpack('<q', ''.join([chr(x) for x in data]))[0]        
        
    elif format_string == 'uint':
        return unpack('<H', ''.join([chr(x) for x in data]))[0] 
        
    elif format_string == 'double':
        return unpack('<d', ''.join([chr(x) for x in data]))[0]
        
    elif format_string == 'float':
        return unpack('<f', ''.join([chr(x) for x in data]))[0]                
        
    elif format_string == 'char':
        return unpack('<B', ''.join([chr(x) for x in data]))[0]
    
    elif format_string == 'schar':
        return unpack('<b', ''.join([chr(x) for x in data]))[0]    
    
    elif format_string == 'hex':
        return ' '.join(['%02X' % x for x in data])  
    # end if
    
#end def
    
def test():
    """
    Test code for this module.
    """
    
    #create object
    with aardvark() as AARD:
        if AARD.port != None:
            print "SUP:LED ON"
            AARD.send_SCPI("SUP:LED ON", "0x54")
            
            print "\nSUP:TEL? 1,name:"
            print AARD.read_SCPI("SUP:TEL? 1,name", "0x54", 'name')
            
            print "\nSUP:TEL? 1,length:"
            print AARD.read_SCPI("SUP:TEL? 1,length", "0x54", 'int')
            
            print "\nSUP:TEL? 1,data"
            print AARD.read_SCPI("SUP:TEL? 1,data", "0x54", 'long')
            
            print "\nSUP:TEL? 1,ascii"            
            print AARD.read_SCPI("SUP:TEL? 1,ascii", "0x54", 'ascii')
            
            print "\nSUL:TEL? 1,data"
            print AARD.read_SCPI("SUL:TEL? 1,data", "0x54", 'string')
            
            print "\nSUP:TEL? 1,data"
            print AARD.read_SCPI("SUP:TEL? 1,data", "0x54", 'straing')             
            
            print "\nSUP:RES ERR"
            AARD.send_SCPI("SUP:RES ERR", "0x54")                
            
        else:
            print "No Aardvark Available"
        # end if
    
    # end with
    
# end def


if __name__ == '__main__':
    # if this code is not running as an imported module run test code
    test()
# end if