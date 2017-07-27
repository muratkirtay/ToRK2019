#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright (c) 2016, ROBOTIS CO., LTD.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of ROBOTIS nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################

# Author: Ryu Woon Jung (Leon)

#
# *********     Read and Write Example      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using a Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(support.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 3 (Baudrate : 1000000 [1M])
#


import numpy as np
import yarp
import cv2
import os
import time

os.sys.path.append('../dynamixel_functions_py')             # Path setting
import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library



if os.name == 'nt':
        import msvcrt
            def getch():
                        return msvcrt.getch().decode()
else:
        import sys, tty, termios
            fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                    def getch():
                                try:
                                                tty.setraw(sys.stdin.fileno())
                                                            ch = sys.stdin.read(1)
                                finally:
                                                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                                                        return ch



                                                    # Control table address
                                                    ADDR_PRO_TORQUE_ENABLE       = 64                          # Control table address is different in Dynamixel model
                                                    ADDR_PRO_GOAL_POSITION       = 116
                                                    ADDR_PRO_PRESENT_POSITION    = 132

                                                    # Protocol version
                                                    PROTOCOL_VERSION            = 2                             # See which protocol version is used in the Dynamixel

                                                    # Default setting
                                                    DXL_ID                      = 1                             # Dynamixel ID: 1
                                                    BAUDRATE                    = 57600#1000000
                                                    DEVICENAME                  = "/dev/ttyUSB0".encode('utf-8')# Check which port is being used on your controller
                                                                                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0"

                                                                                                                TORQUE_ENABLE               = 1                             # Value for enabling the torque
                                                                                                                TORQUE_DISABLE              = 0                             # Value for disabling the torque
                                                                                                                DXL_MINIMUM_POSITION_VALUE  = 0                       # Dynamixel will rotate between this value
                                                                                                                DXL_MAXIMUM_POSITION_VALUE  = 4095                        # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
                                                                                                                DXL_MOVING_STATUS_THRESHOLD = 0 #20                            # Dynamixel moving status threshold

                                                                                                                ESC_ASCII_VALUE             = 0x1b

                                                                                                                COMM_SUCCESS                = 0                             # Communication Success result value
                                                                                                                COMM_TX_FAIL                = -1001                         # Communication Tx Failed

                                                                                                                # Initialize PortHandler Structs
                                                                                                                # Set the port path
                                                                                                                # Get methods and members of PortHandlerLinux or PortHandlerWindows
                                                                                                                port_num = dynamixel.portHandler(DEVICENAME)

                                                                                                                # Initialize PacketHandler Structs
                                                                                                                dynamixel.packetHandler()

                                                                                                                dxl_comm_result = COMM_TX_FAIL                              # Communication result
                                                                                                                dxl_error = 0                                               # Dynamixel error

                                                                                                                # Open port
                                                                                                                if dynamixel.openPort(port_num):
                                                                                                                        print("Succeeded to open the port!")
                                                                                                                else:
                                                                                                                        print("Failed to open the port!")
                                                                                                                            print("Press any key to terminate...")
                                                                                                                                getch()
                                                                                                                                    quit()

                                                                                                                                    # Set port baudrate
                                                                                                                                    if dynamixel.setBaudRate(port_num, BAUDRATE):
                                                                                                                                            print("Succeeded to change the baudrate!")
                                                                                                                                    else:
                                                                                                                                            print("Failed to change the baudrate!")
                                                                                                                                                print("Press any key to terminate...")
                                                                                                                                                    getch()
                                                                                                                                                        quit()


                                                                                                                                                        # Enable Dynamixel Torque
                                                                                                                                                        dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
                                                                                                                                                        if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
                                                                                                                                                                dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
                                                                                                                                                        elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
                                                                                                                                                                dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))
                                                                                                                                                        else:
                                                                                                                                                                print("Dynamixel has been successfully connected")


                                                                                                                                                                goal, init_position, dxl_present_position = 11*5, 0

                                                                                                                                                                while(1):
                                                                                                                                                                      # Write goal position
                                                                                                                                                                        dynamixel.write4ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_PRO_GOAL_POSITION, init_position)#dxl_goal_position[index])
                                                                                                                                                                            if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
                                                                                                                                                                                        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
                                                                                                                                                                            elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
                                                                                                                                                                                        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))

                                                                                                                                                                                            dxl_present = dynamixel.read4ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_PRO_PRESENT_POSITION)
                                                                                                                                                                                                if dxl_present  == init_position:
                                                                                                                                                                                                            print "------- Moved To Zero ------"
                                                                                                                                                                                                                    break


                                                                                                                                                                                                                # Disable Dynamixel Torque
                                                                                                                                                                                                                dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
                                                                                                                                                                                                                if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
                                                                                                                                                                                                                        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
                                                                                                                                                                                                                elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
                                                                                                                                                                                                                        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))


                                                                                                                                                                                                                        # Close port
                                                                                                                                                                                                                        dynamixel.closePort(port_num)
                                                                                                                                                                                                                        
