#!/usr/bin/env python
"""Class for collecting and outputting results to PDF with reportlab."""

from reportlab.platypus import Image, Paragraph, SimpleDocTemplate
from reportlab.rl_config import defaultPageSize
from reportlab.lib import utils
from reportlab.lib.styles import ParagraphStyle

from src.platypus_utils import get_para_style_defaults


class WebTestResults(object):
    """class for collecting and outputting results to pdf with reportlab"""

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
        guesses."""
        self._story = []
        self.max_x, self.max_y = defaultPageSize
        self._heading_style_dict = get_para_style_defaults()
        self._heading_style_dict['fontName'] = 'Helvetica-Bold'
        self._heading_style_dict['fontSize'] = 17.5
        self._heading_style_dict['leading'] = 20
        self.heading_style = ParagraphStyle('head', **self.heading_style)
        self._text_style_dict = get_para_style_defaults()
        self._text_style_dict['fontName'] = "Helvetica"
        self._text_style_dict['fontSize'] = 12.5
        self._text_style_dict['leading'] = 13.5
        self.text_style = ParagraphStyle('text', **self.text_style)

    def add_img_from_file(self, filename):
        """Adds an image from a file to the document. Currently assumes the
        image is already 300 dpi, and scales it to fit in one page.

        TODO:
            Future versions will:
                be generalized to handle PIL and reportlab images
                deal with resolution appropriately
                slice the image across pages semi-intelligently

        @param filename (str) : full path to image file
        """
        img = utils.ImageReader(filename)
        w, h = self._scale_img(*img.getSize())
        self._story.append(Image(filename, width=w, height=h))

    def _scale_img(self, img_x, img_y):
        """returns new image dimensions that will fit inside
        self.max_x and self.max_y.

        TODO:
            Check the dimensions used by platypus for image size. If not px,
            this may be pretty broken

        @param img_x (number) : image width in px
        @param img_y (number) : image height in px
        @return (tuple) : (int_img_x, int_img_y)
        """
        x_scale = 1 if self.max_x > img_x else self.max_x / img_x
        y_scale = 1 if self.max_y > img_y else self.max_y / img_y

        # Take the smallest scale factor, add a little slack for margins
        scale = min(x_scale, y_scale) - .1
        return (int(scale * img_x), int(scale * img_y))

    def add_test_section_header(self, heading, text):
        """Adds opening text describing a test

        A section header is the textual material that precedes the image(s)
        displayed for a test of a particular platform. This is rendered in a
        heading style (for the title) and a subhead style (for the text).
        A reasonable example might be:
        ----
        Internet Explorer 10

        OS: Windows
        UserAgent: Internet Explorer
        Load Time: 00:00:2.700000
        ----
        In that example, the first line would be passed as the heading and the
        remaining lines (as a single string) would be passed as text.

        @param heading (str) : text to be used as heading
        @param text (str) : subheading text
        """
        self.add_heading(heading)
        self.add_text(text)

    def add_heading(self, text):
        """Appends a paragraph of text in the heading style to the story.

        @param text (str) : text to be added as heading.
        """
        self._story.append(Paragraph(text, self.heading_style))

    def add_text(self, text):
        """Appends a paragraph of text in the regular style to the story.

        @param text (str) : text to be added.
        """
        self._story.append(Paragraph(text, self.text_style))

    def write_to_file(self, filename):
        """writes the report to filename.

        @param filename (str) : full path to file to write
        """
        doc = SimpleDocTemplate(filename)
        doc.build(self._story)

    def set_heading_attribute(self, attribute_name, val):
        """Sets an attribute of the style used when adding headings.

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

    def set_text_attribute(self, attribute_name, val):
        """Sets an attribute of the style used when adding headings.

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
