class BaseRepository:
    def __init__(self, model):
        self.model = model

    def find_by_id(self, record_id):
        return self.model.objects.get(id=record_id)

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, record_id, **kwargs):
        obj = self.find_by_id(record_id)
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, record_id):
        obj = self.find_by_id(record_id)
        if obj:
            obj.delete()
            return True
        return False

    def find_all(self, **filters):
        try:
            queryset = self.model.objects.filter(**filters)
            return queryset
        except Exception as e:
            raise e
