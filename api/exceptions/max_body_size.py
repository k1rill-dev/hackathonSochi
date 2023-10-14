class MaxBodySizeException(Exception):
    def __init__(self, body_len: int):
        self.body_len = body_len
