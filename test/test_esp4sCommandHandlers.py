#!/usr/bin/env python

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

from unittest import TestCase
from esp4s_command_handlers import Esp4sCommandHandlers


class TestEsp4sCommandHandlers(TestCase):
    def test_start_http_server(self):
        rval = None
        self.assertEqual(rval, None)

    def test_do_command(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.do_command(["poll"])
        self.assertEqual(rval, "okay")
        rval = command_handler.set_board_led(['board_led', 'Off'])
        self.assertEqual(rval, "okay")

    def test_execute_command(self):
        # this method is tested by a call from test_do_command
        rval = None
        self.assertEqual(rval, None)

    def test_orientation(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.orientation(["a", "b"])
        self.assertEqual(rval, "okay")

    def test_temp_units(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.temp_units(["a", "b"])
        self.assertEqual(rval, "okay")

    def test_poll(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.do_command(["poll"])
        self.assertEqual(rval, "okay")

    def test_pop_status(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.pop_status()
        self.assertEqual(rval, False)

    # noinspection PyPep8
    def test_send_cross_domain_policy(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        #noinspection PyUnusedLocal
        rval = None
        rval = command_handler.send_cross_domain_policy("crossdomain.xml")
        self.assertNotEqual(rval, None)

    def test_reset_esplora(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.reset_esplora("abc")
        self.assertEqual(rval, "okay")

    def test_set_board_led(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.set_board_led(['board_led', 'On'])
        self.assertEqual(rval, "okay")
        rval = command_handler.set_board_led(['board_led', 'Off'])
        self.assertEqual(rval, "okay")

    def test_set_leds(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.set_leds(['leds', 'Red', '240'])
        self.assertEqual(rval, "okay")
        rval = command_handler.set_leds(['leds', 'Red', '0'])
        self.assertEqual(rval, "okay")
        rval = command_handler.set_leds(['leds', 'Blue', '240'])
        self.assertEqual(rval, "okay")
        rval = command_handler.set_leds(['leds', 'Blue', '0'])
        self.assertEqual(rval, "okay")
        rval = command_handler.set_leds(['leds', 'Green', '240'])
        self.assertEqual(rval, "okay")
        rval = command_handler.set_leds(['leds', 'Green', '0'])
        self.assertEqual(rval, "okay")

    def test_play_tone(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        # noinspection PyUnusedLocal
        rval = command_handler.play_tone(['play_tone', 'C'])
        rval = command_handler.play_tone(['play_tone', 'Note_Off'])
        self.assertEqual(rval, "okay")

    def test_continuous_tone(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        command_handler.continuous_tone(['tone2', '1000'])
        rval = command_handler.play_tone(['play_tone', 'Note_Off'])
        self.assertEqual(rval, "okay")

    def test_tinker_output(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.tinker_output(['tinker_out', 'A', '200'])
        self.assertEqual(rval, "okay")
        rval = command_handler.tinker_output(['tinker_out', 'B', '200'])
        self.assertEqual(rval, "okay")
        rval = command_handler.tinker_output(['tinker_out', 'A', '0'])
        self.assertEqual(rval, "okay")
        rval = command_handler.tinker_output(['tinker_out', 'B', '0'])
        self.assertEqual(rval, "okay")

    def test_get_snap_status(self):
        command_handler = Esp4sCommandHandlers('/dev/ttyACM0')
        rval = command_handler.get_snap_status(["light"])
        self.assertEqual(rval, "okay")