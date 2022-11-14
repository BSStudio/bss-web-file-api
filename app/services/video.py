from collections import namedtuple
from io import BytesIO
from pathlib import Path
from uuid import UUID

from PIL import Image

from app.config import settings
from app.models.video import Video

Poster = namedtuple("Poster", ["width", "height", "name"])
short_path = Path(settings.server_base_path, "v")
long_path = Path(settings.server_base_path, "video")


def create_folder_structure(video: Video, with_symlinks=True):
    main_path = long_video_path(video.id)
    for p in [main_path, Path(main_path, "poster")] + [
        Path(main_path, "gear" + str(pp)) for pp in range(1, 10)
    ]:
        p.mkdir(parents=True, exist_ok=True)
        p.chmod(0o755)
    if with_symlinks:
        update_symlinks(video)


def create_thumbnails(content: bytes, video_id: UUID):
    poster_path = Path(long_video_path(video_id), "poster")
    with Image.open(BytesIO(content)) as image:
        for poster in [
            Poster(1920, 1080, "fhd"),
            Poster(1280, 720, "hd"),
            Poster(854, 480, "sd"),
        ]:
            i = image.copy()
            i.thumbnail((poster.width, poster.height))
            i.save(Path(poster_path, poster.name + ".jpeg"))


def update_symlinks(video: Video):
    main_path = long_video_path(video.id)
    for p in Path(settings.server_base_path, "v").glob("*/"):
        if p.is_symlink() and p.readlink().samefile(main_path):
            p.unlink(missing_ok=True)
    # create a new symlink to the long path
    short_video_path(video.url).symlink_to(
        main_path.resolve(), target_is_directory=True
    )


def long_video_path(video_id: UUID):
    return Path(short_path, str(video_id))


def short_video_path(video_url: str):
    return Path(long_path, video_url)
