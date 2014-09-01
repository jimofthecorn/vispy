# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" Fast and failsafe GL console """

# Code translated from glumpy

import numpy as np

from ..shaders import ModularProgram
from .visual import Visual
from ...gloo import VertexBuffer, set_state, _check_valid
from ...color import Color
from ...ext.six import string_types


# Translated from
# http://www.piclist.com/tecHREF/datafile/charset/
#     extractor/charset_extractor.htm
__font_6x8__ = np.array([
    (0x00, 0x00, 0x00, 0x00, 0x00, 0x00), (0x10, 0xE3, 0x84, 0x10, 0x01, 0x00),
    (0x6D, 0xB4, 0x80, 0x00, 0x00, 0x00), (0x00, 0xA7, 0xCA, 0x29, 0xF2, 0x80),
    (0x20, 0xE4, 0x0C, 0x09, 0xC1, 0x00), (0x65, 0x90, 0x84, 0x21, 0x34, 0xC0),
    (0x21, 0x45, 0x08, 0x55, 0x23, 0x40), (0x30, 0xC2, 0x00, 0x00, 0x00, 0x00),
    (0x10, 0x82, 0x08, 0x20, 0x81, 0x00), (0x20, 0x41, 0x04, 0x10, 0x42, 0x00),
    (0x00, 0xA3, 0x9F, 0x38, 0xA0, 0x00), (0x00, 0x41, 0x1F, 0x10, 0x40, 0x00),
    (0x00, 0x00, 0x00, 0x00, 0xC3, 0x08), (0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
    (0x00, 0x00, 0x00, 0x00, 0xC3, 0x00), (0x00, 0x10, 0x84, 0x21, 0x00, 0x00),
    (0x39, 0x14, 0xD5, 0x65, 0x13, 0x80), (0x10, 0xC1, 0x04, 0x10, 0x43, 0x80),
    (0x39, 0x10, 0x46, 0x21, 0x07, 0xC0), (0x39, 0x10, 0x4E, 0x05, 0x13, 0x80),
    (0x08, 0x62, 0x92, 0x7C, 0x20, 0x80), (0x7D, 0x04, 0x1E, 0x05, 0x13, 0x80),
    (0x18, 0x84, 0x1E, 0x45, 0x13, 0x80), (0x7C, 0x10, 0x84, 0x20, 0x82, 0x00),
    (0x39, 0x14, 0x4E, 0x45, 0x13, 0x80), (0x39, 0x14, 0x4F, 0x04, 0x23, 0x00),
    (0x00, 0x03, 0x0C, 0x00, 0xC3, 0x00), (0x00, 0x03, 0x0C, 0x00, 0xC3, 0x08),
    (0x08, 0x42, 0x10, 0x20, 0x40, 0x80), (0x00, 0x07, 0xC0, 0x01, 0xF0, 0x00),
    (0x20, 0x40, 0x81, 0x08, 0x42, 0x00), (0x39, 0x10, 0x46, 0x10, 0x01, 0x00),
    (0x39, 0x15, 0xD5, 0x5D, 0x03, 0x80), (0x39, 0x14, 0x51, 0x7D, 0x14, 0x40),
    (0x79, 0x14, 0x5E, 0x45, 0x17, 0x80), (0x39, 0x14, 0x10, 0x41, 0x13, 0x80),
    (0x79, 0x14, 0x51, 0x45, 0x17, 0x80), (0x7D, 0x04, 0x1E, 0x41, 0x07, 0xC0),
    (0x7D, 0x04, 0x1E, 0x41, 0x04, 0x00), (0x39, 0x14, 0x17, 0x45, 0x13, 0xC0),
    (0x45, 0x14, 0x5F, 0x45, 0x14, 0x40), (0x38, 0x41, 0x04, 0x10, 0x43, 0x80),
    (0x04, 0x10, 0x41, 0x45, 0x13, 0x80), (0x45, 0x25, 0x18, 0x51, 0x24, 0x40),
    (0x41, 0x04, 0x10, 0x41, 0x07, 0xC0), (0x45, 0xB5, 0x51, 0x45, 0x14, 0x40),
    (0x45, 0x95, 0x53, 0x45, 0x14, 0x40), (0x39, 0x14, 0x51, 0x45, 0x13, 0x80),
    (0x79, 0x14, 0x5E, 0x41, 0x04, 0x00), (0x39, 0x14, 0x51, 0x55, 0x23, 0x40),
    (0x79, 0x14, 0x5E, 0x49, 0x14, 0x40), (0x39, 0x14, 0x0E, 0x05, 0x13, 0x80),
    (0x7C, 0x41, 0x04, 0x10, 0x41, 0x00), (0x45, 0x14, 0x51, 0x45, 0x13, 0x80),
    (0x45, 0x14, 0x51, 0x44, 0xA1, 0x00), (0x45, 0x15, 0x55, 0x55, 0x52, 0x80),
    (0x45, 0x12, 0x84, 0x29, 0x14, 0x40), (0x45, 0x14, 0x4A, 0x10, 0x41, 0x00),
    (0x78, 0x21, 0x08, 0x41, 0x07, 0x80), (0x38, 0x82, 0x08, 0x20, 0x83, 0x80),
    (0x01, 0x02, 0x04, 0x08, 0x10, 0x00), (0x38, 0x20, 0x82, 0x08, 0x23, 0x80),
    (0x10, 0xA4, 0x40, 0x00, 0x00, 0x00), (0x00, 0x00, 0x00, 0x00, 0x00, 0x3F),
    (0x30, 0xC1, 0x00, 0x00, 0x00, 0x00), (0x00, 0x03, 0x81, 0x3D, 0x13, 0xC0),
    (0x41, 0x07, 0x91, 0x45, 0x17, 0x80), (0x00, 0x03, 0x91, 0x41, 0x13, 0x80),
    (0x04, 0x13, 0xD1, 0x45, 0x13, 0xC0), (0x00, 0x03, 0x91, 0x79, 0x03, 0x80),
    (0x18, 0x82, 0x1E, 0x20, 0x82, 0x00), (0x00, 0x03, 0xD1, 0x44, 0xF0, 0x4E),
    (0x41, 0x07, 0x12, 0x49, 0x24, 0x80), (0x10, 0x01, 0x04, 0x10, 0x41, 0x80),
    (0x08, 0x01, 0x82, 0x08, 0x24, 0x8C), (0x41, 0x04, 0x94, 0x61, 0x44, 0x80),
    (0x10, 0x41, 0x04, 0x10, 0x41, 0x80), (0x00, 0x06, 0x95, 0x55, 0x14, 0x40),
    (0x00, 0x07, 0x12, 0x49, 0x24, 0x80), (0x00, 0x03, 0x91, 0x45, 0x13, 0x80),
    (0x00, 0x07, 0x91, 0x45, 0x17, 0x90), (0x00, 0x03, 0xD1, 0x45, 0x13, 0xC1),
    (0x00, 0x05, 0x89, 0x20, 0x87, 0x00), (0x00, 0x03, 0x90, 0x38, 0x13, 0x80),
    (0x00, 0x87, 0x88, 0x20, 0xA1, 0x00), (0x00, 0x04, 0x92, 0x49, 0x62, 0x80),
    (0x00, 0x04, 0x51, 0x44, 0xA1, 0x00), (0x00, 0x04, 0x51, 0x55, 0xF2, 0x80),
    (0x00, 0x04, 0x92, 0x31, 0x24, 0x80), (0x00, 0x04, 0x92, 0x48, 0xE1, 0x18),
    (0x00, 0x07, 0x82, 0x31, 0x07, 0x80), (0x18, 0x82, 0x18, 0x20, 0x81, 0x80),
    (0x10, 0x41, 0x00, 0x10, 0x41, 0x00), (0x30, 0x20, 0x83, 0x08, 0x23, 0x00),
    (0x29, 0x40, 0x00, 0x00, 0x00, 0x00), (0x10, 0xE6, 0xD1, 0x45, 0xF0, 0x00)
], dtype=np.float32)

VERTEX_SHADER = """
uniform vec2 u_pos;
uniform float u_scale;
uniform vec2 u_px_scale;
uniform vec4 u_color;

attribute vec2 a_position;
attribute vec3 a_bytes_012;
attribute vec3 a_bytes_345;

varying vec4 v_color;
varying vec3 v_bytes_012, v_bytes_345;

void main (void)
{
    vec4 pos = $transform(vec4(u_pos, 0.0, 1.0));
    gl_Position = pos + vec4(a_position * u_px_scale * u_scale, 0., 0.);
    gl_PointSize = 8.0 * u_scale;
    v_color = u_color;
    v_bytes_012 = a_bytes_012;
    v_bytes_345 = a_bytes_345;
}
"""

FRAGMENT_SHADER = """
float segment(float edge0, float edge1, float x)
{
    return step(edge0,x) * (1.0-step(edge1,x));
}

varying vec4 v_color;
varying vec3 v_bytes_012, v_bytes_345;

void main(void)
{
    vec2 uv = floor(gl_PointCoord.xy * 8.0);
    if(uv.x > 5.0) discard;
    if(uv.y > 7.0) discard;
    float index  = floor( (uv.y*6.0+uv.x)/8.0 );
    float offset = floor( mod(uv.y*6.0+uv.x,8.0));
    float byte = segment(0.0,1.0,index) * v_bytes_012.x
               + segment(1.0,2.0,index) * v_bytes_012.y
               + segment(2.0,3.0,index) * v_bytes_012.z
               + segment(3.0,4.0,index) * v_bytes_345.x
               + segment(4.0,5.0,index) * v_bytes_345.y
               + segment(5.0,6.0,index) * v_bytes_345.z;
    if( floor(mod(byte / (128.0/pow(2.0,offset)), 2.0)) > 0.0 )
        gl_FragColor = v_color;
    else
        discard;
}
"""


class Console(Visual):
    """Fast and failsafe text console

    Parameters
    ----------
    pos : tuple
        Position (x, y) of the console.
    color : instance of Color
        Color to use.
    scale : int
        Scale factor for the text.
    rows : int
        Number of rows.
    cols : int
        Nmuber of columns.
    orientation : str
        Either "scroll-up" (like a terminal), or "scroll-down".
        In "scroll-up", the most recent message is at the bottom.
    border : color
        Color to use for the border.
    parent : instance of Entity
        The parent of the Text visual.
    """
    def __init__(self, pos=(0, 0), color='black', scale=1, rows=24, cols=80,
                 orientation='scroll-up', anchor_x='left', anchor_y='top',
                 **kwargs):
        _check_valid('orientation', orientation, ('scroll-up', 'scroll-down'))
        _check_valid('anchor_x', anchor_x, ('left', 'right', 'center'))
        _check_valid('anchor_y', anchor_y, ('top', 'middle', 'center',
                                            'bottom'))
        Visual.__init__(self, **kwargs)
        # Harcoded because of font above and shader program
        self.color = color
        self.scale = scale
        self.pos = pos
        self._rows, self._cols = rows, cols
        self._cwidth = 6
        self._cheight = 10
        self._row = -1
        self._ori = orientation
        self._program = ModularProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        # Initialize glyph position (they won't move)
        self._bytes_012 = np.zeros((self.rows, self.cols, 3), np.float32)
        self._bytes_345 = np.zeros((self.rows, self.cols, 3), np.float32)
        C, R = np.meshgrid(np.arange(self.cols), np.arange(self.rows))
        # by default we are in left, bottom orientation
        x_off = 0.
        if anchor_x in ('right', 'center'):
            x_off = -self._cwidth * self.cols
            if anchor_x == 'center':
                x_off /= 2.
        if anchor_y in ('top', 'center', 'middle'):
            y_off = -self._cheight * self.rows
            if anchor_y in ('center', 'middle'):
                y_off /= 2.
        pos = np.empty((self.rows, self.cols, 2), np.float32)
        pos[..., 0] = 4.0 + self._cwidth * C + x_off
        pos[..., 1] = 4.0 + self._cheight * R + y_off
        self._position = VertexBuffer(pos)

    @property
    def pos(self):
        """ The position of the text anchor in the local coordinate frame
        """
        return self._pos

    @pos.setter
    def pos(self, pos):
        pos = [float(p) for p in pos]
        assert len(pos) == 2
        self._pos = tuple(pos)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = Color(color)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = int(max(scale, 1))

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def draw(self, event):
        if event is not None:
            xform = event.render_transform.shader_map()
            px_scale = event.framebuffer_cs.transform.scale[:2]
        else:
            xform = self.transform.shader_map()
            # Rather arbitrary scale
            px_scale = 0.01, 0.01
        self._program.vert['transform'] = xform
        self._program.prepare()
        self._program['u_px_scale'] = px_scale
        self._program['u_color'] = self.color.rgba
        self._program['u_scale'] = self.scale
        self._program['u_pos'] = self.pos
        self._program['a_position'] = self._position
        self._program['a_bytes_012'] = VertexBuffer(self._bytes_012)
        self._program['a_bytes_345'] = VertexBuffer(self._bytes_345)
        set_state(depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))
        self._program.draw('points')

    def clear(self):
        """ Clear console """
        self._bytes_012.fill(0)
        self._bytes_345.fill(0)
        self._row = -1

    def write(self, line=''):
        """Write text and scroll

        Parameters
        ----------
        line : str
            Line of text to write. ``''`` can be used for a blank line.
        """
        # Clear line
        if not isinstance(line, string_types):
            raise TypeError('text must be a string')
        # ensure we only have ASCII chars
        line = line.encode('utf-8').decode('ascii', errors='replace')
        # Update row and scroll if necessary
        n = self.rows
        self._row += 1 if self._ori == 'scroll-down' else -1
        if self._row >= n:
            self._bytes_012[:-1] = self._bytes_012[1:]
            self._bytes_345[:-1] = self._bytes_345[1:]
            self._row = n - 1
        elif self._row < 0:
            self._bytes_012[1:] = self._bytes_012[:-1]
            self._bytes_345[1:] = self._bytes_345[:-1]
            self._row = 0
        self._bytes_012[self._row] = 0
        self._bytes_345[self._row] = 0
        line = line[:self._cols]  # Crop text if necessary
        I = np.array([ord(c) - 32 for c in line])
        I = np.clip(I, 0, len(__font_6x8__)-1)
        b = __font_6x8__[I]
        self._bytes_012[self._row, :len(line)] = b[:, :3]
        self._bytes_345[self._row, :len(line)] = b[:, 3:]
