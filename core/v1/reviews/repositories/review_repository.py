# from django.db.models.base import Model
from injector import inject

from ....utils.helpers.orm import BaseRepository
from ..models import Review


class ReviewRepository(BaseRepository):
    @inject
    def __init__(self):
        super().__init__(Review)
