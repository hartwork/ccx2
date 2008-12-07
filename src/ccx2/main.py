# Copyright (c) 2008, Pablo Flouret <quuxbaz@gmail.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met: Redistributions of
# source code must retain the above copyright notice, this list of conditions and
# the following disclaimer. Redistributions in binary form must reproduce the
# above copyright notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
# Neither the name of the software nor the names of its contributors may be
# used to endorse or promote products derived from this software without specific
# prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys

import urwid
import urwid.curses_display

from ccx2 import playlist
from ccx2 import statusbar
from ccx2 import xmms

from ccx2.config import keybindings

xs = xmms.get()

class Ccx2(object):
  palette = [
    ('body','dark cyan','black', 'standout'),
    ('reverse','black','dark cyan', 'standout'),
    ('current_song','light red','black', 'standout'),
    ('statusbar','light gray', 'black'),
    ('key','light cyan', 'black', 'underline'),
    ('title', 'white', 'black',),
    ]
    
  def __init__(self):
    self.playlist = playlist.Playlist()
    self.statusbar = statusbar.StatusBar()
    self.view = urwid.Frame(urwid.AttrWrap(self.playlist, 'body'), footer=self.statusbar.widget)

  def main(self):
    self.ui = urwid.curses_display.Screen()
    self.ui.register_palette(self.palette)
    self.ui.set_input_timeouts(max_wait=0.1)
    self.ui.run_wrapper(self.run)

  def redraw(self):
    canvas = self.view.render(self.size, focus=1)
    self.ui.draw_screen(self.size, canvas)

  def run(self):
    self.size = self.ui.get_cols_rows()

    while 1:
      self.redraw()

      keys = None
      while not keys:
        keys = self.ui.get_input()
        xs.ioin()
        if xs.have_ioin:
          self.redraw()

      for k in keys:
        if k == 'window resize':
          self.size = self.ui.get_cols_rows()
        elif k in keybindings['general']['quit']:
          return

        self.view.keypress(self.size, k)

if __name__ == '__main__':
  Ccx2().main()

