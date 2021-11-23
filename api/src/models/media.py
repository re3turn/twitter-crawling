class Media:
    media_type: str
    url: str

    def __init__(self, media_type: str, url: str):
        self.media_type = media_type
        self.url = url
