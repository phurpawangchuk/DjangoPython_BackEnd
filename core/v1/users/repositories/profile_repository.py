from django.db.models.base import Model as Model
from injector import inject

from ....utils.helpers.orm import BaseRepository
from ..models import Role


class ProfileRepository(BaseRepository):
    @inject
    def __init__(self, model: Role):
        super().__init__(model)

    def find_profile_by_user(self, user_id):
        return self.model.objects.get(user__id=user_id)
