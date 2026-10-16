"""This module contains all video related service logic."""

from pathlib import Path
from uuid import UUID

from ..models.video import Video
from ..settings import settings
from .image import ImgFormat, create_images
from .paths import child_path


class VideoService:
    """Video service class."""

    def __init__(self, base_path: str = settings.server_base_path):
        self.id_paths_base = Path(base_path, "v")
        self.url_paths_base = Path(base_path, "video")

    def create_folder_structure(self, video: Video):
        """
        This method will create the folder structure for a video.
        /v/{video.id}/thumbnail
        And a symlink to the id folder from the url folders
        /video/{video.url[0]} -> /v/{video.id}
        /video/{video.url[1]} -> /v/{video.id}
        ...
        :param video: the video object
        :return: None
        """
        id_path = self.to_id_path(video.id)
        id_path.mkdir(parents=True, exist_ok=True)
        # create a folder for the thumbnails
        Path(id_path, "thumbnail").mkdir(exist_ok=True)
        self.update_symlinks(video)

    def create_thumbnails(self, img_file: bytes, video_id: UUID):
        """
        This method will create the thumbnails in different formats
        /v/{video.id}/thumbnail/{size}.{format}
        :param img_file: the image file
        :param video_id: the id of the video
        :return: None
        """
        thumbnail_path = Path(self.to_id_path(video_id), "thumbnail")
        poster_sizes = [
            ImgFormat(1920, 1080, "fhd"),
            ImgFormat(1280, 720, "hd"),
            ImgFormat(854, 480, "sd"),
        ]
        create_images(img_file, thumbnail_path, poster_sizes)

    def update_symlinks(self, video: Video):
        """
        This method will update the symlinks to the id folder from the url folders
        First it will remove all references to the id folder
        Then it will create new symlinks to the id path
        :param video: the video object
        :return: None
        """
        id_path = self.to_id_path(video.id)
        if not id_path.exists():
            raise FileNotFoundError(f"Video folder {id_path.resolve()} does not exist")
        for p in self.url_paths_base.glob("*/"):
            if p.is_symlink() and p.readlink().samefile(id_path):
                p.unlink(missing_ok=True)
        for url_path in [self.to_url_path(url) for url in video.urls]:
            url_path.symlink_to(
                # use the absolute path to the id folder
                target=id_path.resolve(),
                target_is_directory=True,
            )

    # pylint: disable=duplicate-code
    def create_base_path(self):
        """This method will create the parent folder for all id and url folders."""
        if not self.id_paths_base.exists():
            self.id_paths_base.mkdir(parents=True, exist_ok=True)
        if not self.url_paths_base.exists():
            self.url_paths_base.mkdir(parents=True, exist_ok=True)

    def to_id_path(self, video_id: UUID):
        """
        This method will return the base path
        where the id folders for videos are located.
        """
        return child_path(self.id_paths_base, str(video_id))

    def to_url_path(self, video_url: str):
        """
        This method will return the base path
        where the url folders for videos are located.
        """
        return child_path(self.url_paths_base, video_url)

    # pylint: enable=duplicate-code
