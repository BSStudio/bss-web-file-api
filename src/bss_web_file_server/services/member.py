"""This module contains all member related service logic."""

from pathlib import Path
from uuid import UUID

from ..models.member import Member
from ..settings import settings
from .image import ImgFormat, create_images
from .paths import child_path


class MemberService:
    """Member service class."""

    def __init__(self, base_path: str = settings.server_base_path):
        self.id_paths_base = Path(base_path, "m")
        self.url_paths_base = Path(base_path, "member")

    def create_folder_structure(self, member: Member):
        """
        This method will create the folder structure for a member.
        /m/{member.id}/profile
        And a symlink to the id folder from the url folder
        /member/{member.url} -> /m/{member.id}
        :param member: the member object
        :return: None
        """
        id_path = self.to_id_path(member.id)
        id_path.mkdir(parents=True, exist_ok=True)
        # create a folder for the profile pictures
        Path(id_path, "profile").mkdir(exist_ok=True)
        self.update_symlink(member)

    def create_profile_picture(self, img_file: bytes, member_id: UUID):
        """
        This method will create the profile picture in different formats
        /m/{member.id}/profile/{size}.{format}
        :param img_file: the image file
        :param member_id: the id of the member
        :return: None
        """
        profile_picture_path = Path(self.to_id_path(member_id), "profile")
        profile_picture_sizes = [
            ImgFormat(1920, 1080, "xl"),
            ImgFormat(1280, 720, "l"),
            ImgFormat(854, 480, "m"),
        ]
        create_images(img_file, profile_picture_path, profile_picture_sizes)

    def update_symlink(self, member: Member):
        """
        This method will update the symlink to the id folder from the url folder
        First it will check if the id folder exists
        Then it will remove all references to the id folder
        Finally it will create a new symlink to the id path
        :param member: the member object
        :return: None
        """
        id_path = self.to_id_path(member.id)
        if not id_path.exists():
            raise FileNotFoundError(f"Member folder {id_path.resolve()} does not exist")
        for url_path in self.url_paths_base.iterdir():
            if url_path.is_symlink() and url_path.readlink().samefile(id_path):
                url_path.unlink(missing_ok=True)
        self.to_url_path(member.url).symlink_to(
            # use the absolute path to the id folder
            target=id_path.resolve(),
            target_is_directory=True,
        )

    # pylint: disable=duplicate-code
    def create_base_path(self):
        """
        This method will create the parent folder for all id and url folders.
        """
        if not self.id_paths_base.exists():
            self.id_paths_base.mkdir(parents=True, exist_ok=True)
        if not self.url_paths_base.exists():
            self.url_paths_base.mkdir(parents=True, exist_ok=True)

    def to_id_path(self, member_id: UUID):
        """
        This method will return the base path
        where the id folders for members are located.
        """
        return child_path(self.id_paths_base, str(member_id))

    def to_url_path(self, member_url: str):
        """
        This method will return the base path
        where the url folders for members are located.
        """
        return child_path(self.url_paths_base, member_url)

    # pylint: enable=duplicate-code
