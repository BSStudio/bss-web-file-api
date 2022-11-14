from collections import namedtuple
from io import BytesIO
from pathlib import Path
from uuid import UUID

import pillow_avif
from PIL import Image

from app.config import settings
from app.models.member import Member

ImgFormat = namedtuple("ImgFormat", ["width", "height", "name"])
short_path = Path(settings.server_base_path, "m")
long_path = Path(settings.server_base_path, "member")


def create_folder_structure(member: Member, with_symlinks=True):
    main_path = member_path(member.id)
    main_path.mkdir(parents=True, exist_ok=True)
    main_path.chmod(0o755)
    if with_symlinks:
        sym_member_path(member.url).symlink_to(
            main_path.resolve(), target_is_directory=True
        )


def create_thumbnails(content: bytes, member_id: UUID):
    path = member_path(member_id)
    with Image.open(BytesIO(content)) as image:
        image.copy().save(Path(path, "lg.avif"))
        image.copy().save(Path(path, "lg.webp"))
        image.copy().save(Path(path, "lg.jpeg"))


def update_symlinks(member: Member):
    main_path = member_path(member.id)
    for p in Path(settings.server_base_path, "m").glob("*/"):
        if p.is_symlink() and p.readlink().samefile(main_path):
            p.unlink(missing_ok=True)
    sym_member_path(member.url).symlink_to(
        main_path.resolve(), target_is_directory=True
    )


def member_path(member_id: UUID):
    return Path(short_path, str(member_id))


def sym_member_path(member_url: str):
    return Path(long_path, member_url)
