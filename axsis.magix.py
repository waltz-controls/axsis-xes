import asyncio, rx, os, json
from magix_client import MagixHttpClient
from rx.scheduler.eventloop import AsyncIOScheduler

magix_host = os.getenv('MAGIX_HOST', 'http://localhost:8080')


def main():
    loop = asyncio.get_event_loop()
    client = MagixHttpClient(magix_host)
    client.observe().subscribe(lambda event: print(json.loads(event.data)), scheduler=AsyncIOScheduler(loop))
    loop.run_forever()
    pass


if __name__ == "__main__":
    main()
