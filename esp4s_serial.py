# -*- coding: utf-8 -*-
"""
Created on Feb 14 13:17:15 2015

@author: Alan Yorinks
Copyright (c) 2015 Alan Yorinks All right reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import threading
import time

import serial


class EspSerial(threading.Thread):
    """
     This class manages the serial port for Arduino serial communications
    """

    # class variables
    esplora = serial.Serial()  # reference to the serial port
    port_id = ""
    baud_rate = 57600
    timeout = 1
    command_deque = None
    orientation = "Joystick_On_Left"
    temp_units = "Celcius"

    SYNC = 0  # ESP String is start of frame
    PUSH_BUTTON_DOWN = 1
    PUSH_BUTTON_LEFT = 2
    PUSH_BUTTON_UP = 3
    PUSH_BUTTON_RIGHT = 4
    SLIDER = 5
    LIGHT = 6
    TEMP = 7
    SOUND = 8
    JOYSTICK_PUSH_BUTTON = 9
    JOYSTICK_X_AXIS = 10
    JOYSTICK_Y_AXIS = 11
    ACCEL_X_AXIS = 12
    ACCEL_Y_AXIS = 13
    ACCEL_Z_AXIS = 14
    TINKERKIT_IN_A = 15
    TINKERKIT_IN_B = 16

    MAX_SENSOR = 17

    snap_data = {'Down': 0, 'Left': 0, 'Up': 0, 'Right': 0, 'slider': 0, 'light': 0, 'temp': 0, 'sound': 0,
                 'Button': 0, 'Left-Right_(X)': 0, 'Up-Down_(Y)': 0, 'X__Side-Twist': 0, 'Y__Front-Twist': 0,
                 'Z__Raise-Lower': 0, 'A': 0, 'B': 0}

    key_list = ['Down', 'Left', 'Up', 'Right', 'slider', 'light', 'temp', 'sound', 'Button', 'Left-Right_(X)',
                'Up-Down_(Y)', 'X__Side-Twist', 'Y__Front-Twist', 'Z__Raise-Lower', 'A', 'B']

    multi_map = {"Down": "buttons", "Up": "buttons", "Left": "buttons", "Right": "buttons",
                 "Left-Right_(X)": "joystick", 'Up-Down_(Y)': "joystick", "Button": "joystick",
                 "X__Side-Twist": "accel", "Y__Front-Twist": "accel", "Z__Raise-Lower": "accel",
                 "A": "tkInput", "B": "tkInput"}

    def __init__(self, port_id, command_deque):
        """
        Constructor:
        :param command_deque: A reference to the deque shared with the _command_handler
        :return: None
        """
        self.port_id = port_id
        self.command_deque = command_deque

        threading.Thread.__init__(self)
        self.daemon = True
        self.esplora = serial.Serial(self.port_id, self.baud_rate,
                                     timeout=int(self.timeout), writeTimeout=0)

        self.stop_event = threading.Event()
        time.sleep(1)

    def stop(self):
        """
        This method sets the threading event
        :return: None
        """
        self.stop_event.set()

    def is_stopped(self):
        """
        This method returns the state of the threading event
        :return: Threading event state
        """
        return self.stop_event.is_set()

    def open(self):
        """
        open the serial port using the configuration data
        :return: a reference to this instance
        """

        # open a serial port
        print('\nOpening Esplora Serial port %s ' % self.port_id)

        try:
            # in case the port is already open, let's close it and then
            # reopen it
            self.esplora.close()
            time.sleep(1)
            self.esplora.open()
            time.sleep(1)
            return self.esplora

        except Exception:
            # opened failed - will report back to caller
            raise

    def close(self):
        """
        Close the serial port
        :return: None
        """
        try:
            self.esplora.close()
        except OSError:
            pass

    def write(self, data):
        """
        This method writes data to the serial port
        :param data: Data to write to the esplora
        :return: Number of bytes written
        """
        return self.esplora.write(data)

    # noinspection PyMethodMayBeStatic
    def is_single_type(self, key):
        """
        This method validates if the block is associated with a single value and not a drop down list in the block
        :param key: Lookup key for "singles"
        :return: True if the key is found, else False
        """
        singles = ["slider", "light", "temp", "sound", ]
        if key in singles:
            return True
        else:
            return False

    def create_reporter_reply(self, data_list):
        """
        Validate that the list has "ESP" as its first element.
        If not,  ignore the list and return False
        Else process it.
        :param data_list: Sensor data list
        :return: True if the data is valid. False if it is not.
        """

        reply = ""
        if len(data_list) != self.MAX_SENSOR:
            return False
        elif data_list[0] != "ESP":
            return False
        else:
            data_list.pop(0)
        # for i in range(0, len(data_list) - 1):
        try:
            for i in range(0, len(data_list)):
                # get the key from keys list
                key = self.key_list[i]
                if self.is_single_type(key):
                    self.snap_data[key] = data_list[i]
                    reply += key
                    reply += ' '
                    reply += data_list[i]
                    reply += '\n'
                else:
                    # get major name
                    name = self.multi_map.get(key, None)
                    reply += name
                    reply += "/"
                    self.snap_data[key] = data_list[i]
                    reply += key
                    reply += ' '
                    reply += data_list[i]
                    reply += '\n'

        except TypeError:
            print(
                "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\
                !!!!!!!!!!!!!!!!!!!!\!!!!!!!!!!!!!!!")
            print("Server and Esplora are out of sync. Please reset the Esplora and restart \
            the esp4s server")
            print(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            while 1:
                pass  # place the reply in the deque
        self.command_deque.append([reply, self.snap_data])
        # print("len", len(self.command_deque))
        return True  # noinspection PyExceptClausesOrder

    def set_orientation(self, orientation):
        """
        Set the esplora physical orientation
        :param orientation: "Joystick_On_Left" or "Joystick_On_Right"
        :return:None
        """
        self.orientation = orientation

    def set_temp_units(self, temp_units):
        """
        Set the temperature units
        :param temp_units: Celcius or Fahrenheit
        :return:None
        """
        self.temp_units = temp_units

    def run(self):
        """
        This method continually runs. If an incoming character is available on the serial port
        it is read and placed on the _command_deque
        :return: Never Returns
        """

        my_str = ""
        sensor_data_list = []
        while not self.is_stopped():
            # we can get an OSError: [Errno9] Bad file descriptor when shutting down
            # just ignore it

            try:
                # read in a full cycle of reporter data
                if self.esplora.inWaiting():
                    c = self.esplora.read()
                    if c == ',':
                        sensor_data_list.append(my_str)
                        my_str = ""
                    elif c == '\n':
                        sensor_data_list = self.normalize_data(sensor_data_list)
                        self.create_reporter_reply(sensor_data_list)
                        my_str = ""
                        sensor_data_list = []
                    else:
                        my_str += c
            except OSError:
                pass
            except IOError:
                self.stop()
        self.close()

    def normalize_data(self, sensor_data_list):
        """
        This method adjusts the data for better human consumption
        :param sensor_data_list:
        :return:adjusted sensor_data_list
        """
        # validate length

        if len(sensor_data_list) != self.MAX_SENSOR:
            return []

        # reverse the button data
        for i in range(self.PUSH_BUTTON_DOWN, self.PUSH_BUTTON_RIGHT + 1):
            if sensor_data_list[i] == "0":
                sensor_data_list[i] = "1"
            else:
                sensor_data_list[i] = "0"

        # adjust slider so that left most position return 0

        if self.orientation == "Joystick_On_Left":
            rval = int(sensor_data_list[self.SLIDER])
            sensor_data_list[self.SLIDER] = str(abs(1023 - rval))

        # adjust joystick button
        rval = int(sensor_data_list[self.JOYSTICK_PUSH_BUTTON])
        if rval > 10:
            sensor_data_list[self.JOYSTICK_PUSH_BUTTON] = "0"
        else:
            sensor_data_list[self.JOYSTICK_PUSH_BUTTON] = "1"

        if self.orientation == "Joystick_On_Left":
            # adjust joystick data
            val = int(sensor_data_list[self.JOYSTICK_X_AXIS])
            val *= -1
            sensor_data_list[self.JOYSTICK_X_AXIS] = str(val)

            val = int(sensor_data_list[self.JOYSTICK_Y_AXIS])
            val *= -1
            sensor_data_list[self.JOYSTICK_Y_AXIS] = str(val)

        # adjust accelerometer data
        val = int(sensor_data_list[self.ACCEL_X_AXIS])
        val *= -1
        sensor_data_list[self.ACCEL_X_AXIS] = str(val)

        val = int(sensor_data_list[self.ACCEL_Y_AXIS])
        val *= -1
        sensor_data_list[self.ACCEL_Y_AXIS] = str(val)

        # adjust push buttons
        if self.orientation == "Joystick_On_Right":
            down = sensor_data_list[self.PUSH_BUTTON_DOWN]
            up = sensor_data_list[self.PUSH_BUTTON_UP]
            left = sensor_data_list[self.PUSH_BUTTON_LEFT]
            right = sensor_data_list[self.PUSH_BUTTON_RIGHT]

            sensor_data_list[self.PUSH_BUTTON_DOWN] = up
            sensor_data_list[self.PUSH_BUTTON_UP] = down
            sensor_data_list[self.PUSH_BUTTON_LEFT] = right
            sensor_data_list[self.PUSH_BUTTON_RIGHT] = left

        # adjust temperature
        if self.temp_units == "Fahrenheit":
            ftemp = int(sensor_data_list[self.TEMP])
            ftemp = (ftemp * 9) / 5 + 32
            sensor_data_list[self.TEMP] = str(ftemp)

        return sensor_data_list




