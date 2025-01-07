import json
import socket

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
access_token = '714929766-NjHvCoaEiec12uy9B5WP1d1KX6qIDk5x7QEoaig5'
access_secret = 'ar3lNyuiBEhlfxIDYs1Z9HKolEwgpcmOZ7YOe4ameoiG2'
consumer_key = 'AcBJMMpRLafo45psEKMNuFiZi'
consumer_secret = 'L1tcFX8JUAnY992OUNz5zoFZUONUb4932pgQqeIYJchYUgx1eB'


class TweetsListener(StreamListener):
    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            msg = json.loads(data)
            print(msg['text'].encode('utf-8'))
            # print(msg['user']['name'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def send_data(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['freepalestine'])


s = socket.socket()
host = "127.0.0.1"
port = 9892
s.bind((host, port))
print("listening on port: %s" % str(port))
s.listen(5)
c, addr = s.accept()
print("Received request from: " + str(addr))

send_data(c)
