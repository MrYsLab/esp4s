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

import logging
import datetime
from collections import deque

from esp4s_serial import EspSerial
import esp4s_http_server


class Esp4sCommandHandlers:
    """
    This class processes any command received from Scratch 2.0

    If commands need to be added in the future, a command handler method is
    added to this file and the command_dict at the end of this file is
    updated to contain the method. Command names must be the same in the json .s2e Scratch
    descriptor file.
    """
    # class variables
    port_id = ""
    baud_rate = 57600
    timeout = 1
    esplora = None
    report = []
    snap_report = {}
    scratch_report = []

    def __init__(self, com_port):
        """
        Instantiate the command handler
        :param com_port: Communications port for esplora communication
        :return: None
        """
        self.com_port = com_port
        self.first_poll_received = False
        self.first_command_received = False
        self.command_deque = deque()
        self.debug = 0
        # open the serial interface and start the receive thread
        self.esplora = EspSerial(com_port, self.command_deque)
        self.esplora.open()
        self.esplora.start()

    def start_http_server(self):
        """
        Start up the HTTP server
        :return: None
        """
        esp4s_http_server.start_server(self)

    def do_command(self, command):
        """
        This method looks up the command that resides in element zero of the command list
        within the command dictionary and executes the method for the command.
        Each command returns string that will be eventually be sent to Scratch
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        if not self.first_command_received:
            # start the sensor data flowing
            self.esplora.write("C")
            self.first_command_received = True

        method = self.command_dict.get(command[0])

        if command[0] != "poll":
            # turn on debug logging if requested
            if self.debug == 'On':
                debug_string = "DEBUG: "
                debug_string += str(datetime.datetime.now())
                debug_string += ": "
                for data in command:
                    debug_string += "".join(map(str, data))
                    debug_string += ' '
                logging.debug(debug_string)
                print (debug_string)
        rval = self.execute_command(method, command)
        return rval

    def execute_command(self, method, command):
        """
        Look up the command in command table and return it's method.
        :param method: The method to execute
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        return method(self, command)

    def orientation(self, command):
        """
        Set the orientation of the esplora
        :param command:
        :return:"okay"
        """
        self.esplora.set_orientation(command[1])
        return 'okay'

    def temp_units(self, command):
        """
        Set the temperature units
        :param command:
        :return:"okay"
        """
        self.esplora.set_temp_units(command[1])
        return 'okay'

    # noinspection PyUnusedLocal
    def poll(self, command):
        """
        This method scans the data tables and assembles data for all reporter
        blocks and returns the data to the caller.
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        if not self.first_poll_received:
            logging.info('Scratch detected! Ready to rock and roll...')
            print ('Scratch detected! Ready to rock and roll...')
            self.first_poll_received = True

        # retrieve sensor status from the esplora
        responses = ''
        if self.pop_status():
            responses = ''.join(self.scratch_report)
            if responses == '':
                responses = 'okay'
            return responses
        else:
            return 'okay'

    def pop_status(self):
        """
        Get the latest status from the deque
        :return: True if status is available, False if it is not
        """
        while len(self.command_deque) != 0:
            self.report = self.command_deque.popleft()
        if len(self.report) != 0:
            self.scratch_report = self.report[0]
            self.snap_report = self.report[1]
            return True
        else:
            return False

    # noinspection PyUnusedLocal
    def send_cross_domain_policy(self, command):
        """
        This method returns cross domain policy back to Scratch upon request.
        It keeps Flash happy. It is here as a place holder if Scratch allows
        the HTTP extensions to be used on the on-line version
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        policy = "<cross-domain-policy>\n"
        policy += "  <allow-access-from domain=\"*\" to-ports=\""
        policy += str(self.com_port)
        policy += "\"/>\n"
        policy += "</cross-domain-policy>\n\0"
        return policy

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def reset_esplora(self, command):
        """
        Kill tone
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        self.esplora.write("T0")
        return "okay"

    # noinspection PyMethodMayBeStatic
    def set_board_led(self, command):
        """
        This method control the D13 board LED
        :param command: Command sent from Scratch/Snap!f
        :return: HTTP response string
        """
        if command[1] == 'On':
            self.esplora.write("L 1")
        else:
            self.esplora.write("L 0")
        return 'okay'
        # normal esp4s_http return for commands

    # noinspection PyMethodMayBeStatic
    def set_leds(self, command):
        """
        This method controls the RGB LEDs
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        command_string = None
        if command[1] == "Red":
            command_string = "R"
        elif command[1] == "Green":
            command_string = "G"
        elif command[1] == "Blue":
            command_string = "B"
        if command_string is not None:
            command_string += command[2]
            self.esplora.write(command_string)
        return 'okay'

    # noinspection PyMethodMayBeStatic
    def play_tone(self, command):
        """
        This will play a tone continuously at the specified frequency.
        To Turn off tone, set the frequency to 0.
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        tone_chart = {"C": "523", "C_Sharp--D_Flat": "554", "D": "587", "D_Sharp--E_Flat": "622",
                      "E": "659", "F": "698", "F_Sharp--G_Flat": "740", "G": "783",
                      "G_Sharp--A_Flat": "831",
                      "A": "880", "A_Sharp--B_Flat": "932", "B": "958", "Note_Off": "0"}

        command_string = "T"
        command_string += tone_chart[command[1]]
        self.esplora.write(command_string)
        return 'okay'

    def continuous_tone(self, command):
        command_string = "T"
        command_string += command[1]
        self.esplora.write(command_string)
        return 'okay'

    # noinspection PyMethodMayBeStatic
    def tinker_output(self, command):
        """
        Output data to the tinkerKit A or B output channel
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        if command[1] == 'A':
            command_string = 'Y'
            command_string += command[2]
        else:
            command_string = 'Z'
            command_string += command[2]

        self.esplora.write(command_string)
        return 'okay'

    def get_snap_status(self, command):
        """
        This method allows status retrieval for the non-polling Snap! application
        :param command: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        if self.pop_status():
            if len(self.snap_report) != 0:
                if len(command) == 1:
                    report_entry = self.snap_report[command[0]]
                else:
                    report_entry = self.snap_report[command[1]]
                return report_entry
            else:
                return 'okay'
        else:
            return 'okay'

    # This table must be at the bottom of the file because Python does not provide forward referencing for
    # the methods defined above.
    # noinspection PyPep8
    command_dict = {'crossdomain.xml': send_cross_domain_policy, 'reset_all': reset_esplora,
                    'board_led': set_board_led, 'leds': set_leds, 'tinker_out': tinker_output,
                    'play_tone': play_tone, 'tone2': continuous_tone, 'orientation': orientation,
                    'temp_units': temp_units, 'poll': poll,
                    'buttons': get_snap_status, 'joystick': get_snap_status,
                    'accel': get_snap_status, 'slider': get_snap_status, 'light': get_snap_status,
                    'temp': get_snap_status, 'sound': get_snap_status, 'tkInput': get_snap_status
                    }
