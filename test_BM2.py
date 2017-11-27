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
@package test_BM2
Top level script to test the BM2's operation
"""

import sys
sys.path.insert(1, 'src/')
sys.path.insert(1, 'processes/')

import BM2_process
import process_GUI
import process_SCPI

BM2_struct = BM2_process.BM2_Process()
main_gui = process_GUI.process_window(BM2_struct)

main_gui.start()



