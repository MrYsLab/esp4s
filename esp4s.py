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
import os
import sys
import logging
from esp4s_command_handlers import Esp4sCommandHandlers
import serial


# noinspection PyBroadException
def esp4s():
    """
    This is the "main" function of the program.
    """
    # make sure we have a log directory and if not, create it.
    if not os.path.exists('log'):
        os.makedirs('log')

    # turn on logging
    logging.basicConfig(filename='./log/esp4s_debugging.log', filemode='w', level=logging.DEBUG)
    logging.info('esp4s Version 1.0    Copyright(C) 2015 Alan Yorinks    All Rights Reserved ')
    print('esp4s version 1.0   Copyright(C) 2015 Alan Yorinks    All Rights Reserved ')

    # get the com_port from the command line or default if none given
    # if user specified the com port on the command line, use that when invoking PyMata,
    # else use '/dev/ttyACM0'
    if len(sys.argv) == 2:
        com_port = str(sys.argv[1])
    else:
        com_port = '/dev/ttyACM0'
    logging.info('com port = %s' % com_port)

    try:
        # instantiate the command handler
        command_handler = Esp4sCommandHandlers(com_port)
        # start the esp4s_http server
        command_handler.start_http_server()
    except OSError:
        print("\nDid you plug in the Esplora? Can't find " + com_port)
    except serial.SerialException:
        print("")
        print("Could not open serial port" + com_port)
        print("Did you plug in the Esplora?")
    except IndexError:
        print("Reset the Esplora and reset the server.")
    except TypeError:
        print("Reset the Esplora and reset the server.")
    except Exception:
        logging.debug('Exception in esp4s_http.py %s' % str(Exception))
    except KeyboardInterrupt:
        # give control back to the shell that started us
        logging.debug('Exception in esp4s_http.py %s' % str(Exception))

if __name__ == "__main__":
    esp4s()
