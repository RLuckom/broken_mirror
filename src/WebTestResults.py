#!/usr/bin/env python
"""Class for collecting and outputting results to PDF with reportlab.

@author raphael.luckom
@license GPL v2.0 or later

"""

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import ParagraphStyle

from src.platypus_utils import get_para_style_defaults
from src.WebTestSection import WebTestSection


class WebTestResults(object):

    """collects and outputs results to pdf with reportlab."""

    def __init__(self):
        """constructor.

        The constructor takes no arguments, and sets defaults for the heading
        and text styles to use when adding text to the result report. The
        type of self.heading_style and self.text_style is
        reportlab.lib.styles.ParagraphStyle. Those members can be overridden
        with preferred styles, or to override single attributes use
        set_text_attribute and set_heading_attribute. For an overview of
        available style attributes, see the reportlab documentation, or
        look at platypus_utils.get_para_style_defaults and make educated
        guesses.

        """
        self._story = []
        self._heading_style_dict = get_para_style_defaults()
        self._heading_style_dict['fontName'] = 'Helvetica-Bold'
        self._heading_style_dict['fontSize'] = 17.5
        self._heading_style_dict['leading'] = 20
        self.heading_style = ParagraphStyle('head', **self._heading_style_dict)
        self._text_style_dict = get_para_style_defaults()
        self._text_style_dict['fontName'] = "Helvetica"
        self._text_style_dict['fontSize'] = 12.5
        self._text_style_dict['leading'] = 13.5
        self.text_style = ParagraphStyle('text', **self._text_style_dict)

    def write_to_file(self, filename):
        """write the report to filename.

        @param filename (str) : full path to file to write

        """
        doc = SimpleDocTemplate(filename)
        doc.build(self._story)

    def set_heading_style_attribute(self, attribute_name, val):
        """Set an attribute of the style used when adding headings.

        For a reference to the allowable styles, see the reportlab
        docs or look at platypus_utils.get_para_style_defaults.

        @param attribute_name (str) : name of attribute to set
        @param val (str) : value to set attribute to. Note that some
                           attributes, such as alignment and textColor,
                           take special values defined by reportlab. This
                           method does NOT convert val argument types to
                           the types expected by reportlab.

        """
        self._heading_style_dict[attribute_name] = val
        self.heading_style = ParagraphStyle('head', **self.heading_style)

    def set_texti_style_attribute(self, attribute_name, val):
        """Set an attribute of the style used when adding headings.

        For a reference to the allowable styles, see the reportlab
        docs or look at platypus_utils.get_para_style_defaults.

        @param attribute_name (str) : name of attribute to set
        @param val (str) : value to set attribute to. Note that some
                           attributes, such as alignment and textColor,
                           take special values defined by reportlab. This
                           method does NOT convert val argument types to
                           the types expected by reportlab.

        """
        self._text_style_dict[attribute_name] = val
        self.text_style = ParagraphStyle('head', **self.text_style)

    def add_section(self, header, text, imgfile):
        sec = WebTestSection(header, text, self.heading_style,
                             self.text_style)
        sec.chunk_img(imgfile)
        self._story += sec.list_elements()
