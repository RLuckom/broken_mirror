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

    def __init__(self, heading_head, heading_text, header_style, text_style):
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
        width, height = img.size
        scale = 1
        if px_to_std(width) > points_to_std(self.max_x):
            scale = px_to_std(width) / points_to_std(self.max_x)
        return img.resize((int(scale * width), int(scale * height)),
                          IM.ANTIALIAS)

    def chunk_img(self, fn):
        img = self._resize_img_to_scale(IM.open(fn))
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
            chunk = img.crop(bbox)
            chunk_filename = tempfile.mkstemp(suffix='.png')[1]
            chunk.save(chunk_filename, dpi=(200, 200), quality=95)
            self.imgs.append(Image(chunk_filename,
                                   width=pts_width,
                                   height=pts_height))

    def next_page_height(self):
        yield math.floor(points_to_std(self.max_y - self.header_offset))
        while True:
            yield points_to_std(self.max_y)

    def list_elements(self):
        head = Paragraph(self.heading_head, self.header_style)
        text = [Paragraph(x, self.text_style) for x in self.header_text]
        return [head] + text + [Spacer(self.max_x, self.spacer)] + self.imgs
