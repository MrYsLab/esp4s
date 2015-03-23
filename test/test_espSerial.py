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
from collections import deque

from esp4s_serial import EspSerial


class TestEspSerial(TestCase):
    def test_stop(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        transport.stop()
        stop = transport.is_stopped()
        self.assertNotEquals(stop, False)
        transport.close()

    def test_is_stopped(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        stop = transport.is_stopped()
        self.assertNotEquals(stop, True)
        transport.close()

    def test_open(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        self.assertNotEquals(transport, None)
        transport.close()

    def test_close(self):
        command_deque = deque()
        EspSerial('/dev/ttyACM0', command_deque)

    def test_write(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        rval = transport.write("*()")
        self.assertEqual(rval, 3)
        transport.close()

    def test_is_single_type(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        rval = transport.is_single_type("light")
        self.assertEqual(rval, True)
        rval = transport.is_single_type("xyz")
        self.assertEqual(rval, False)
        transport.close()

    def test_create_reporter_reply(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        test_list = ["ESP", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "\n"]
        test_list2 = ["z"]
        rval = transport.create_reporter_reply(test_list)
        self.assertEqual(rval, True)
        rval = transport.create_reporter_reply(test_list2)
        self.assertEqual(rval, False)

    def test_set_orientation(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        transport.set_orientation("abc")
        self.assertEqual(transport.orientation, "abc")

    def test_set_temp_units(self):
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        transport.set_temp_units("abc")
        self.assertEqual(transport.temp_units, "abc")

    def test_run(self):
        # fake test for an endless loop
        data = 3
        self.assertNotEqual(data, 0)

    def test_normalize_data(self):
        a = ['ESP', '1', '1', '1', '1', '430', '973', '17', '0', '1023', '-1', '3', '17', '21', '157', '376', '8']
        command_deque = deque()
        transport = EspSerial('/dev/ttyACM0', command_deque)
        transport.open()
        b = transport.normalize_data(a)
        self.assertEqual(b, ['ESP', '0', '0', '0', '0', '593', '973', '17', '0', '0', '1', '-3', '-17', '-21', '157',
                             '376', '8'])
