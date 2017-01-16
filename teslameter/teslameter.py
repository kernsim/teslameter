# -*- coding: utf-8 -*-
"""
Teslameter

Open Source Initiative OSI - The MIT License

http://www.opensource.org/licenses/mit-license.php

Copyright 2017 Simon Kern

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import os
import Tkinter as tk
import serial
import serial.tools.list_ports
import tkMessageBox
import math

class App(tk.Frame):
    """
    Serial Monitor for ARduino-Nano-Teslameter with Honeywell SS495A Linear Hall Sensor

    Arduino sends ASCII-VAlues. Each line one value in mT.
    Baudrate: 9600
    """
    def __init__(self, parent, title, serialPort):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.serialPort = serialPort
        self.npoints = 200
        self.Line1 = [0 for x in range(self.npoints)]
        parent.wm_title(title)
        parent.wm_geometry("800x600")
        parent.iconbitmap(resource_path('Icons8-Windows-8-Science-Scale.ico'))
        self.txt = tk.Label(self, text='{0:7.2f} mT'.format(0),
                            font=("Courier", 80),
                            justify=tk.RIGHT)
        self.txt.pack(fill=tk.BOTH)
        self.txt_cnt = 0

        self.canvas = tk.Canvas(self, background="black")
        self.canvas.bind("<Configure>", self.on_resize)
        self.gridpos = range(-80, 81, 20)
        self.gridtags = ['GRID{0:d}'.format(i) for i in range(len(self.gridpos))]
        for gt in self.gridtags:
            self.canvas.create_line((0, 0, 0, 0), tag=gt,
                                    fill='darkgrey', dash=(4, 4), width=1)
        self.canvas.create_line((0, 0, 0, 0), tag='X', fill='white', width=1)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.pack(fill=tk.BOTH, expand=1)
        # statusbar
        self.statusbar = tk.Frame(self)
        tk.Label(self.statusbar, text='<Esc>: Quit', width=15).pack(
            side=tk.LEFT)
        tk.Label(self.statusbar, text='<Return>: Toggle Fullscreen', width=20).pack(
            side=tk.LEFT, fill=tk.BOTH)
        tk.Label(self.statusbar, text='<F2>: Change Unit', width=20).pack(
            side=tk.LEFT, fill=tk.BOTH)
        tk.Label(self.statusbar, text='<F1>: Info', width=15).pack(
            side=tk.RIGHT, fill=tk.X)
        # tk.Label(self.statusbar, text='Teslameter (c) 2017 Simon Kern', width=30).pack(
        #    side=tk.RIGHT, fill=tk.X)
        self.statusbar.pack(fill=tk.BOTH)

        parent.bind('<Escape>', lambda e: parent.destroy())
        parent.bind('<Return>', lambda e: self.toggle_fullscreen())
        parent.bind('<F2>', lambda e: self.change_unit())
        parent.bind('<F1>', lambda e: self.show_info())

        self.fullscreen = False
        self._unit_idx = 0
        #                fmt         scale, scale_for_grid
        self.units = (('{0:7.2f} mT', 1.0, 1.0),
                      ('{0:6.1f} G', 10., 1.0),
                      ('{0:6.1f} A/cm', 7.9577, 10./7.9577),
                     )

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.parent.attributes('-fullscreen', self.fullscreen)

    def on_resize(self, event):
        self.replot()

    def change_unit(self):
        self._unit_idx += 1
        if self._unit_idx >2:
            self._unit_idx = 0

    def format_(self, b):
        fmt, scale = self.units[self._unit_idx][:2]
        return fmt.format(b*scale)

    def read_serial(self):
        """
        Check for input from the serial port. On fetching a line, parse
        the sensor values and append to the stored data and post a replot
        request.
        """
        while self.serialPort.inWaiting() != 0:
            line = self.serialPort.readline()
            v = int(line.strip())
            # Calculate flux density with 31.25 mV/mT
            u = (5000./1023.) * v
            b = (u-2500) / 31.25 # mV/(mV/mT)
            # Update the cached data lists with new sensor values.
            self.Line1.append(float(b))
            self.Line1 = self.Line1[-1 * self.npoints:]
            self.after_idle(self.replot)
        # Arduino sends all 50 ms
        self.after(20, self.read_serial)

    def replot(self):
        """
        Update the canvas graph lines from the cached data lists.
        The lines are scaled to match the canvas size as the window may
        be resized by the user.
        """
        scale_for_grid = self.units[self._unit_idx][2]

        self.txt_cnt += 1
        if self.txt_cnt>10:
            val = sum(self.Line1[-10:])/10.
            self.txt.config(text= self.format_(val))
            self.txt_cnt = 0
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        max_y = 180
        coordsX =  []
        for n in range(0, self.npoints):
            x = (w * n) / self.npoints
            coordsX.append(x)
            coordsX.append(h - (h * (self.Line1[n]+max_y/2) / max_y))
        self.canvas.coords('X', *coordsX)
        #coordsX0 = [0, h/2., w, h/2.]
        #self.canvas.coords('X0', *coordsX0)

        for p, gt in zip(self.gridpos, self.gridtags):
            y = h - h*(p*scale_for_grid + max_y/2)/max_y
            coords = [0, y, w, y]
            self.canvas.coords(gt, *coords)

    def show_info(self):
        tkMessageBox.showinfo('Teslameter',
"""Teslameter

Open Source Initiative OSI - The MIT License
http://www.opensource.org/licenses/mit-license.php
Copyright 2017 Simon Kern

App-Icon from https://icons8.com/
""")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main(args = None):
    if args is None:
        args = sys.argv
    port, baudrate = None, 9600
    if len(args) > 1:
        port = args[1]
#    if len(args) > 2:
#        baudrate = int(args[2])

    if port is None:
#        ports = list(serial.tools.list_ports.comports())
        for p, label, dummy in serial.tools.list_ports.comports():
            if 'CH340' in label:
                port = p
                break
    root = tk.Tk()

    if port is None:
        root.withdraw()
        tkMessageBox.showerror('Teslameter: Error',
                               'No COM-port with a label containing "CH340" '
                               +' found. Install CH341-driver or check USB connection. '
                               +'or call with COM-port as command line arguement: '
                               +'"teslameter.exe COM4".')
        return 1

    if port == 'demo':
        s = MockSerial()
    else:
        try:
            s = serial.Serial(port, baudrate)
            s.flushInput()  # clear inputbuffer
            s.readline()  # Make sure that buffer starts after newline
        except serial.SerialException, e:
            root.withdraw()
            tkMessageBox.showerror('Teslameter: Error', e)
            return 1

    app = App(root, "Teslameter", s)
    app.read_serial()
    app.mainloop()
    return 0


class MockSerial(object):
    def __init__(self):
        self.val = 0
        self.dir = 10
        self.cnt = 0

    def readline(self):
        self.val += self.dir
        if self.val <= 0:
            self.val = 0
            self.dir = -self.dir
        if self.val >= 1023:
            self.val = 1023
            self.dir = -self.dir
        #return '{0:d}'.format(511 if self.val > 512 else 512)
        return '{0:d}'.format(self.val)
#        return '{0:d}\n'.format(int(80.*math.sin(self.phi)))

    def inWaiting(self):
        self.cnt += 1
        return (self.cnt % 2) == 0
#        return True

if __name__ == '__main__':
    main()