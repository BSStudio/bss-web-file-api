"""Member endpoints."""

import re
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, UploadFile, status

from security import authorize

from ..models.member import Member
from ..services.member import MemberService

router = APIRouter(tags=["Member"], prefix="/api/v1/member")
service: MemberService = MemberService()


@router.post("", response_model=Member)
def create_member_folder(
    member: Member, authorized: Annotated[None, Depends(authorize)]
):
    """
    Create a folder structure for a member and return the member object.
    :param member: Member object
    :param authorized: fastapi dependency to authorize the request
    :return: 200 and the original member object
    """
    service.create_folder_structure(member)
    return member


@router.put("", response_model=Member)
def update_member_folder(
    member: Member, authorized: Annotated[None, Depends(authorize)]
):
    """
    Update the folder structure for a member and return the member object.
    If the member does not exist, return a 404.
    :param member: Member object
    :param authorized: fastapi dependency to authorize the request
    :return: 200 and the original member object
    """
    if not service.to_id_path(member.id).exists():
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    service.update_symlink(member)
    return member


@router.post("/{member_id}/profilePicture", response_model=UUID)
async def upload_member_picture(
    member_id: UUID, file: UploadFile, authorized: Annotated[None, Depends(authorize)]
):
    """
    Upload a picture for a member to convert
    and store the profile picture in different formats
    If the member does not exist, return a 404.
    If the file is not an image, return a 500.
    :param member_id: the id of the member
    :param file: the image file
    :param authorized: fastapi dependency to authorize the request
    :return: 200 and the original member_id
    """
    # pylint: disable=duplicate-code
    if not service.to_id_path(member_id).exists():
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if file.content_type is not None and not re.match("image/.+", file.content_type):
        return Response(
            content="Mime is not an image format",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    file_content = await file.read()
    # pylint: enable=duplicate-code
    service.create_profile_picture(file_content, member_id)
    return member_id
