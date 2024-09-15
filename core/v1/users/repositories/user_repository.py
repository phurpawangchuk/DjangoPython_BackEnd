from django.db.models.base import Model as Model
from injector import inject

from ....utils.helpers.orm import BaseRepository
from ..models import User


class UserRepository(BaseRepository):
    @inject
    def __init__(self, model: User):
        super().__init__(model)
