import urllib3, os

magix_host = os.getenv('MAGIX_HOST')


class MagixHttpClient():
    def __init__(self):
        self.http = urllib3.PoolManager()

    def broadcast(self, message):

        pass

    def subscribe(self):
        pass