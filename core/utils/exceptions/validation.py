class ValidationException(Exception):
    def __init__(self, detail=None):
        self.detail = detail or {"non_field_errors": ["Invalid input."]}
