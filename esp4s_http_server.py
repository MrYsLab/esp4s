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
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from string import split


class GetHandler(BaseHTTPRequestHandler):
    """
    This class contains the HTTP server that Scratch2 or Snap! communicates with.
    Scratch/Snap! sends HTTP GET requests and this class processes the requests.

    HTTP GET requests are accepted and the appropriate command handler is
    called to process the command.
    """

    # tcp server port - must match that in the .s2e descriptor file
    port = 50209

    # instance handle for the scratch command handler
    scratch_command_handler = None

    # indicator so that we can tell user Scratch is ready to go
    waiting_for_first_scratch_poll = True

    # this is a 'classmethod' because we need to set data before starting
    # the HTTP server.
    # noinspection PyMethodParameters

    @classmethod
    def set_items(self, scratch_command_handler):
        """
        This method instantiates the command handler
        :param scratch_command_handler: command handler instance
        :return: None
        """
        self.command_handler = scratch_command_handler

    # noinspection PyPep8Naming
    def do_GET(self):
        """
        Scratch2 only sends HTTP GET commands. This method processes them.
        It differentiates between a "normal" command request and a request
        to send policy information to keep Flash happy on Scratch.
        (This may change when Scratch is converted to HTML 5
        :return: None
        """

        # skip over the / in the command
        cmd = self.path[1:]

        # create a list containing the command and all of its parameters
        cmd_list = split(cmd, '/')

        # execute the command
        s = self.command_handler.do_command(cmd_list)
        self.send_resp(s)

    # we can't use the standard send_response since we don't conform to its
    # standards, so we craft our own response handler here
    def send_resp(self, response):
        """
        This method sends Scratch an HTTP response to an HTTP GET command.
        :param response: Response string sent to Scratch or Snap1
        :return: None
        """

        crlf = "\r\n"
        # http_response = str(response + crlf)
        http_response = "HTTP/1.1 200 OK" + crlf
        http_response += "Content-Type: text/html; charset=ISO-8859-1" + crlf
        http_response += "Content-Length" + str(len(response)) + crlf
        http_response += "Access-Control-Allow-Origin: *" + crlf
        http_response += crlf
        # add the response to the nonsense above
        if response != 'okay':
            http_response += str(response + crlf)
        # send it out the door to Scratch
        self.wfile.write(http_response)
        # end of GetHandler class


def start_server(command_handler):
    """
       This function populates class variables with essential data and
       instantiates the HTTP Server
        :param command_handler: Command handler instance
        :return: None - this method never returns
    """

    GetHandler.set_items(command_handler)
    try:
        server = HTTPServer(('localhost', 50209), GetHandler)
        print('Starting HTTP Server!')
        print('Use <Ctrl-C> to exit the extension\n')
        print('Please start Scratch or Snap!')
    except Exception:
        logging.debug('Exception in esp4s_http_server.py: HTTP Socket may already be in use - restart Scratch')
        print('HTTP Socket may already be in use - restart Scratch')
        raise
    try:
        # start the server
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('esp4s_http_server.py: keyboard interrupt exception')
        print("You Hit Control-C.  Goodbye !")
        raise KeyboardInterrupt
    except Exception:
        logging.debug('esp4s_http_server.py: Exception %s' % str(Exception))
        raise