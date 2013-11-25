#!/usr/bin/env python
"""Represents a test of a web page. Handles images flowing across pages.

@author raphaelluckom@gmail.com
@license GPL v2.0 or later

"""
from collections import namedtuple
import math
from PIL import Image as IM
from reportlab.platypus import Image, Paragraph, Spacer, PageBreak
import tempfile

from src.ImageProcessingMixin import ImageProcessingMixin

Div = namedtuple('Div', ['height', 'flowable'])


class WebTestSection(ImageProcessingMixin):

    """Builds a list of platypus flowables representing a report section."""

    def __init__(self, heading_head, heading_text, header_style, text_style):
        """constructor.

        @param heading_head (str) : chapter title.
        @param header_text (str) : displayed after the title.
        @param header_style (ParagraphStyle) : style to use for header
        @param text_style (ParagraphStyle) : style to use for text

        """
        self.max_width = 435
        self.max_y = 684
        self.space = 20
        self.px_per_inch = 200
        text = [Div(text_style.leading, Paragraph(x, text_style))
                for x in heading_text.split('\n')]
        head = Div(header_style.leading, Paragraph(heading_head, header_style))
        space = Div(self.space, Spacer(self.max_width, self.space))
        self._flowables = [head] + text + [space]
        super(WebTestSection, self).__init__()

    def chunk_img(self, filename):
        """Flow image across pages, append chunks to self.imgs.

        @filename (str) : full path to img.

        """
        img = self.resize_img_to_width(IM.open(filename))
        width, height = img.size
        pts_width = int(math.floor(self.std_to_points(self.px_to_std(width))))
        vertical_inches = self.px_to_std(height)
        left = 0
        right = width
        top = 0
        bottom = 0
        while vertical_inches > 0:
            vertical_inches -= self.inches_to_fill()
            clawback = vertical_inches if vertical_inches < 0 else 0
            chunk_height = self.inches_to_fill() + clawback
            pts_height = int(math.floor(self.std_to_points(chunk_height)))
            top = bottom
            bottom += int(math.floor(self.std_to_px(chunk_height)))
            bbox = [left, top, right, bottom]
            self._add_chunk(img.crop(bbox), pts_width, pts_height)

    def _add_chunk(self, chunk, pts_width, pts_height):
        """Add an image chunk to self's list of flowables."""
        chunk_filename = tempfile.mkstemp(suffix='.png')[1]
        chunk.save(chunk_filename, dpi=(200, 200), quality=95)
        self._flowables.append(Div(pts_height,
                                   Image(chunk_filename,
                                         width=pts_width,
                                         height=pts_height)))

    def inches_to_fill(self):
        """@return (int) : std units left to fill on the current page."""
        total_height = sum([x.height for x in self._flowables])
        return self.points_to_std(self.max_y
                                  - (total_height % int(self.max_y)))

    def list_elements(self):
        """@return list : list of the self's flowables."""
        return [x.flowable for x in self._flowables] + [PageBreak()]
