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
