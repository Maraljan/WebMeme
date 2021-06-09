import uuid
from pathlib import Path
from typing import Union

from PIL.Image import Image
from werkzeug.datastructures import FileStorage

from config import IMAGES_DIR


class ImageStorage:
    """
    Save all pictures for user.
    """

    def __init__(self, folder: Path):
        self.folder = folder
        self.full_path = IMAGES_DIR.joinpath(folder)
        if not self.full_path.exists():
            self.full_path.mkdir(parents=True)

    def save(self, image: Union[FileStorage, Image]) -> Path:

        if isinstance(image, FileStorage):
            filename = self.generate_filename(self.extension(image.filename))
            file_path = self.full_path.joinpath(filename)
            with file_path.open('wb') as file:
                file.write(image.stream.read())
        elif isinstance(image, Image):
            filename = self.generate_filename('jpg')
            file_path = self.full_path.joinpath(filename)
            image.save(file_path)
        else:
            raise TypeError(f'{type(image)} is not supported')
        # returning relative path
        return self.folder.joinpath(filename)

    @staticmethod
    def extension(filename: str) -> str:
        return filename.split('.')[-1]

    @staticmethod
    def generate_filename(extension: str) -> str:
        new_filename = uuid.uuid4()
        return f'{new_filename}.{extension}'

    def remove(self, image_relative_path: str):
        abs_path = self.get(image_relative_path)

        # deleting image from file_storage
        abs_path.unlink()

    @staticmethod
    def get(image_relative_path: str) -> Path:
        abs_file_path = IMAGES_DIR.joinpath(image_relative_path)
        if not abs_file_path.exists():
            raise FileNotFoundError
        return abs_file_path
