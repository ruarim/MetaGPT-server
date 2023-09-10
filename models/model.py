class Model:
    def __init__(self, **kwargs):
        # Initialize common attributes
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self.deleted_at = kwargs.get('deleted_at')

    def to_dict(self):
        # Convert the object to a dictionary
        data = {
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
        return data

    def from_dict(self, data):
        # Initialize object attributes from a dictionary
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.deleted_at = data.get('deleted_at')

    def __str__(self):
        # Customize the string representation of the object
        return f'{self.__class__.__name__}({self.to_dict()})'
