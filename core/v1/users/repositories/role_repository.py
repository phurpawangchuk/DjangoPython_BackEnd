from django.db.models.base import Model as Model
from injector import inject

from ....utils.helpers.orm import BaseRepository
from ..models import Role


class RoleRepository(BaseRepository):
    @inject
    def __init__(self, model: Role):
        super().__init__(model)

    def exists(self, role_id):
        return self.model.objects.filter(id=role_id).exists()
