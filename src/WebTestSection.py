#!/usr/bin/env python
"""Represents a test of a web page. Handles images flowing across pages.

@author raphaelluckom@gmail.com
@license GPL v2.0 or later

"""
import math
from PIL import Image as IM
from reportlab.platypus import Image, Paragraph, Spacer
import tempfile

from src.platypus_utils import px_to_std, points_to_std
from src.platypus_utils import std_to_px, std_to_points


class WebTestSection(object):

    """Builds a list of platypus flowables representinng a report section."""

    def __init__(self, heading_head, heading_text, header_style, text_style):
        """constructor.

        @param heading_head (str) : chapter title.
        @param header_text (str) : displayed after the title.
        @param header_style (ParagraphStyle) : style to use for header
        @param text_style (ParagraphStyle) : style to use for text

        """
        self.max_x = 200
        self.max_y = 684
        self.spacer = 20
        self.header_text = heading_text.split('\n')
        self.heading_head = heading_head
        self.header_style = header_style
        self.text_style = text_style
        self.imgs = []
        self.header_offset = (header_style.leading + self.spacer
                              + (text_style.leading * len(self.header_text)))

    def _resize_img_to_scale(self, img):
        """scale down an image until it fits within self.max_x.

        Converts self.max_x and img width to inches (img width @300dpi),
        then downsamples the img if necessary so it fits width @300dpi

        @param img (PIL.Image) : image to resize
        @return PIL.Image : resized image

        """
        width, height = img.size
        scale = 1
        if px_to_std(width) > points_to_std(self.max_x):
            scale = px_to_std(width) / points_to_std(self.max_x)
        return img.resize((int(scale * width), int(scale * height)),
                          IM.ANTIALIAS)

    def chunk_img(self, filename):
        """Flow image across pages, append chunks to self.imgs.

        @filename (str) : full path to img.

        """
        img = self._resize_img_to_scale(IM.open(filename))
        width, height = img.size
        pts_width = int(math.floor(std_to_points(px_to_std(width))))
        vertical_inches = px_to_std(height)
        left = 0
        right = width
        top = 0
        bottom = 0
        pages = self.next_page_height()
        while vertical_inches > 0:
            inches_to_fill = pages.next()
            vertical_inches -= inches_to_fill
            clawback = vertical_inches if vertical_inches < 0 else 0
            chunk_height = inches_to_fill + clawback
            pts_height = int(math.floor(std_to_points(chunk_height)))
            top = bottom
            bottom += int(math.floor(std_to_px(chunk_height)))
            bbox = [left, top, right, bottom]
            self._add_chunk(img.crop(bbox), pts_width, pts_height)

    def _add_chunk(self, chunk, pts_width, pts_height):
        """Add an image chunk to self's list of flowables."""
        chunk_filename = tempfile.mkstemp(suffix='.png')[1]
        chunk.save(chunk_filename, dpi=(200, 200), quality=95)
        self.imgs.append(Image(chunk_filename,
                               width=pts_width,
                               height=pts_height))

    def next_page_height(self):
        """Make a generator that returns the next page height.

        @return generator : __next__ method returns the next page height.

        """
        yield math.floor(points_to_std(self.max_y - self.header_offset))
        while True:
            yield points_to_std(self.max_y)

    def list_elements(self):
        """@return list : list of the self's flowables."""
        head = Paragraph(self.heading_head, self.header_style)
        text = [Paragraph(x, self.text_style) for x in self.header_text]
        return [head] + text + [Spacer(self.max_x, self.spacer)] + self.imgs
