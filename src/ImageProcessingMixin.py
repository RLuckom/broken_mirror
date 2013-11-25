"""
Mixin tp provide methods for dealing with images.

@author raphaelluckom@gmail.com
@license GPL v2 or later

"""
from PIL import Image as IM


class ImageProcessingMixin(object):

    """Provides methods for dealing with images."""

    def __init__(self):
        """constructor."""
        if not hasattr(self, 'pts_per_inch'):
            self.pts_per_inch = 72.0
        if not hasattr(self, 'px_per_inch'):
            self.px_per_inch = 300.0

    def resize_img_to_width(self, img_filename, width=None):
        """scale down an image until it fits within self.max_width.

        Converts self.max_width and img width to inches (at self.px_per_inch),
        then downsamples the img if necessary so it fits width at
        self.px_per_inch

        @param img_filename (str) : filename of image to resize
        @return PIL.Image : resized image

        """
        img = IM.open(img_filename)
        if width is None:
            width = self.max_width
        img_width, img_height = img.size
        scale = 1
        if self.px_to_std(img_width) > self.points_to_std(width):
            scale = self.px_to_std(width) / self.points_to_std(width)
        return img.resize((int(scale * img_width), int(scale * img_height)),
                          IM.ANTIALIAS)

    def px_to_std(self, px):
        """@return float: std units (inches, probably)."""
        return float(px) / self.px_per_inch

    def points_to_std(self, pts):
        """@return float: std units (inches, probably)."""
        return float(pts) / self.pts_per_inch

    def std_to_points(self, std):
        """@return float: points."""
        return float(std) * self.pts_per_inch

    def std_to_px(self, std):
        """@return float: pixels."""
        return float(std) * self.px_per_inch
