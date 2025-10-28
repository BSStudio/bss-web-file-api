"""This module contains the logic for the image service."""

from collections import namedtuple
from io import BytesIO
from pathlib import Path

from PIL import Image

ImgFormat = namedtuple("ImgFormat", ["width", "height", "name"])
img_formats = ["avif", "webp", "jpeg"]


def create_images(img_file: bytes, image_path: Path, image_sizes: list[ImgFormat]):
    """
    This method will create the images in three formats: avif, webp and jpeg
    The files will be created in the given image_path with the given image_sizes
    :param img_file: the image file
    :param image_path: the path where the images will be saved
    :param image_sizes: the sizes of the images
    :return: None
    """
    with Image.open(BytesIO(img_file)) as image:
        for size in image_sizes:
            i = image.copy()
            i.thumbnail(size=(size.width, size.height))
            for img_format in img_formats:
                i.save(Path(image_path, size.name + "." + img_format))
