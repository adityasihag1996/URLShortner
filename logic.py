import string

class URLShortener:
    def __init__(self):
        self.charset = string.digits + string.ascii_letters  # Base62 charset

    def encode_id(self, uid):
        # Encodes a UID to a base62 string
        base62 = []
        while uid > 0:
            uid, remainder = divmod(uid, 62)
            base62.append(self.charset[remainder])

        return ''.join(reversed(base62))

    def decode_id(self, base62):
        # Decodes a base62 string to a UID
        uid = 0
        for char in base62:
            uid = uid * 62 + self.charset.index(char)

        return uid


    