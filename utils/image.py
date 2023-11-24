import os
from PIL import Image
from uuid import uuid4
from pydantic import validator, BaseModel
from typing import Union, Optional
from enum import Enum
from fastapi import UploadFile


from core.exeptions.schemas import ThisFileIsNotPicture, FailedCreate


class PathnameUrl(BaseModel):
    small_path: str
    big_path: str


class ReturnedImageCreaterModel(BaseModel):
    is_create: bool
    pathname_url: Union[PathnameUrl, None]


class SizeImage(str, Enum):
    SMALL = 'thrumb_image'
    BIG = "image"


EXTENSION_IMAGE = {'png', 'jpg', 'jpeg', 'wepb'}


def is_contains_extension_accessed_image(filename: Union[str, None]) -> bool:
    if filename != None:
        is_access = None
        for extension in EXTENSION_IMAGE:
            if is_access:
                break
            else:
                is_access = filename.__contains__(extension)
        return is_access

    return False


class ImageModelBasic(BaseModel):
    pathname_big: str = os.path.join(
        os.getcwd(), f"static/pub_image/{SizeImage.BIG.value}")
    pathname_small: str = os.path.join(
        os.getcwd(), f"static/pub_image/{SizeImage.SMALL.value}")

    def __str__(self):
        return f"{self.__class__.__name__}(pathname={self.pathname_big})"


class ImageCreaterModel(ImageModelBasic):
    image: Optional[UploadFile] = None

    @validator("image")
    def validator_image(cls, imageUpload: Optional[UploadFile] = None):
        if imageUpload != None:
            if not is_contains_extension_accessed_image(filename=imageUpload.filename):
                raise ThisFileIsNotPicture
            return imageUpload
        return None

    @property
    def check_directory_static(self):
        if not os.path.exists(self.pathname_big):
            os.makedirs(self.pathname_big)
        if not os.path.exists(self.pathname_small):
            os.makedirs(self.pathname_small)

    async def create_image(self, scale_params: int = 5, width: Optional[int] = None, height: Optional[int] = None) -> ReturnedImageCreaterModel:
        POSITION_WIDTH_INSIDE_PILLOW_SIZE = 0
        POSITION_HEIGHT_INSIDE_PILLOW_SIZE = 1
        self.check_directory_static
        if self.image != None:
            big_image = Image.open(self.image.file)
            if big_image.mode in ("RGBA", "P"):
                big_image = big_image.convert("RGB")

            if width != None or height != None:
                big_image = big_image.resize((width, height))

            small_path = f"{self.pathname_small}/{uuid4()}.webp"
            big_path = f"{self.pathname_big}/{uuid4()}.webp"

            small_image = big_image.resize(
                resize_option(scale_params=scale_params,
                              width=big_image.size[POSITION_WIDTH_INSIDE_PILLOW_SIZE],
                              height=big_image.size[POSITION_HEIGHT_INSIDE_PILLOW_SIZE]))
            small_image.save(small_path, 'WEBP')
            big_image.save(big_path, 'WEBP')

            return ReturnedImageCreaterModel(is_create=True,
                                             pathname_url=PathnameUrl(small_path=small_path, big_path=big_path))
        else:
            raise FailedCreate(issue="picture")

    @property
    def get_pathname_cls(self) -> dict:
        return {"small": self.pathname_small, "big": self.pathname_big}


class DeleterImages(ImageModelBasic):
    def __init__(self, pathname_big: str, pathname_small: str):
        self.pathname_big = pathname_big
        self.pathname_small = pathname_small


def resize_option(scale_params: int, width: int, height: int) -> tuple[int, int]:
    scale_params = scale_params if scale_params < 5 else 5
    return (round(width / scale_params), round(height / scale_params))
