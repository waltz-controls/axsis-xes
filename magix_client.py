import urllib3, os, json, sseclient, rx, asyncio
from rx.scheduler import NewThreadScheduler
import rx.operators as ops


magix_host = os.getenv('MAGIX_HOST', 'http://localhost:8080')
magix_broadcast = magix_host +'/magix/api/broadcast'
magix_subscribe = magix_host +'/magix/api/subscribe'


scheduler = NewThreadScheduler()

class MagixHttpClient():
    def __init__(self):
        self.http = urllib3.PoolManager()
        response = self.http.request('GET',
                                     magix_subscribe,
                                     preload_content=False)
        sse = sseclient.SSEClient(response)
        self.stream = rx.from_iterable(sse.events(), scheduler=scheduler).pipe(
            ops.publish()
        )
        self.stream.connect()

    def broadcast(self, message):
        print("in broadcast")
        global magix_host
        encoded_message = json.dumps(message).encode('utf-8')
        #TODO fire and forget
        self.http.request('POST',
            magix_broadcast,
            body=encoded_message,
            headers={'Content-Type': 'application/json'})
        pass

    def observe(self, channel='message'):
        return self.stream.pipe(
            ops.filter(lambda event: event.event == channel)
        )


async def main():
    client = MagixHttpClient()

    client.observe().subscribe(lambda event: print(json.loads(event.data)))
    client.observe().subscribe(lambda event: print(json.loads(event.data)))
    client.observe().subscribe(lambda event: print(json.loads(event.data)))
    client.broadcast({'hello':'world'})
    await asyncio.sleep(30)


asyncio.run(main())