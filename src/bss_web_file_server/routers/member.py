"""Module for /api/v1/member related routes."""

import re
from uuid import UUID
from fastapi import APIRouter, Response, UploadFile, status
from ..models.member import Member
from ..services.member import (
    create_folder_structure,
    create_profile_picture,
    update_symlink,
    to_id_path,
)

router = APIRouter(tags=["Member"], prefix="/api/v1/member")


@router.post("", response_model=Member)
def create_member_folder(member: Member):
    """
    Create a folder structure for a member and return the member object.
    :param member: Member object
    :return: 200 and the original member object
    """
    create_folder_structure(member)
    return member


@router.put("", response_model=Member)
def update_member_folder(member: Member):
    """
    Update the folder structure for a member and return the member object.
    If the member does not exist, return a 404.
    :param member: Member object
    :return: 200 and the original member object
    """
    if not to_id_path(member.id).exists():
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    update_symlink(member)
    return member


@router.post("/{member_id}/profilePicture", response_model=UUID)
async def upload_member_picture(member_id: UUID, file: UploadFile):
    """
    Upload a picture for a member to convert
    and store the profile picture in different formats
    If the member does not exist, return a 404.
    If the file is not an image, return a 500.
    :param member_id: the id of the member
    :param file: the image file
    :return: 200 and the original member_id
    """
    if not to_id_path(member_id).exists():
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    # pylint: disable=duplicate-code
    if not re.match("image/.+", file.content_type):
        return Response(
            content="Mime is not an image format",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    # pylint: disable=duplicate-code
    file_content = await file.read()
    create_profile_picture(file_content, member_id)
    return member_id
