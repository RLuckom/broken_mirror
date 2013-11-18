#!/usr/bin/env python
"""Class for collecting and outputting results to PDF with reportlab."""

from reportlab.platypus import Image, Paragraph, SimpleDocTemplate
from reportlab.rl_config import defaultPageSize
from reportlab.lib import utils
from reportlab.lib.styles import ParagraphStyle

from src.platypus_utils import get_para_style_defaults


class WebTestResults(object):

    def __init__(self):
        self._story = []
        self.max_x, self.max_y = defaultPageSize
        self.heading_style = get_para_style_defaults()
        self.heading_style['fontName'] = 'Helvetica-Bold'
        self.heading_style['fontSize'] = 17.5
        self.heading_style['leading'] = 20
        self.heading_style = ParagraphStyle('head', **self.heading_style)
        self.text_style = get_para_style_defaults()
        self.text_style['fontName'] = "Helvetica"
        self.text_style['fontSize'] = 12.5
        self.text_style['leading'] = 13.5
        self.text_style = ParagraphStyle('text', **self.text_style)

    def add_img_from_file(self, filename):
        img = utils.ImageReader(filename)
        w, h = self._scale_img(*img.getSize())
        self._story.append(Image(filename, width=w, height=h))

    def _scale_img(self, img_x, img_y):
        x_scale = 1 if self.max_x > img_x else self.max_x / img_x
        y_scale = 1 if self.max_y > img_y else self.max_y / img_y

        # Take the smallest scale factor, add a little slack for margins
        scale = min(x_scale, y_scale) - .1
        return (int(scale * img_x), int(scale * img_y))

    def add_test_section_header(self, heading, text):
        self.add_heading(heading)
        self.add_text(text)

    def add_heading(self, text):
        self._story.append(Paragraph(text, self.heading_style))

    def add_text(self, text):
        self._story.append(Paragraph(text, self.text_style))

    def write_to_file(self, filename):
        doc = SimpleDocTemplate(filename)
        doc.build(self._story)
