import uuid


class Request:

    def __init__(self, request_type, authors=None, title=None, key_words=None,
                 annotation=None, ref=None):
        self.request_type = request_type
        self.authors = authors
        self.title = title
        self.key_words = key_words
        self.annotation = annotation
        self.ref = ref
        self.request_id = str(uuid.uuid4())

    def __str__(self):
        return f'{type(self).__name__}: Request type = {self.request_type},' \
            f' Authors = {self.authors}, Title = {self.title}, ' \
            f'Key words = {self.key_words}, Annotation = {self.annotation}, ' \
            f'Ref = {self.ref}, request id = {self.request_id}'
