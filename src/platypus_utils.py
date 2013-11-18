"""Utility functions for using platypus."""

from reportlab.lib import colors
from reportlab.lib import enums


def get_para_style_defaults():
    """@return (dict) : dict of default platypus style attributes."""
    return {'fontName': 'Times-Roman',
            'fontSize': 10,
            'leading': 12,
            'leftIndent': 0,
            'rightIndent': 0,
            'firstLineIndent': 0,
            'alignment': enums.TA_LEFT,
            'spaceBefore': 0,
            'spaceAfter': 0,
            'bulletFontName': 'Times-Roman',
            'bulletFontSize': 10,
            'bulletIndent': 0,
            'textColor': colors.black,
            'backColor': None,
            'wordWrap': None,
            'borderWidth': 0,
            'borderPadding': 0,
            'borderColor': None,
            'borderRadius': None,
            'allowWidows': 1,
            'allowOrphans': 0}
