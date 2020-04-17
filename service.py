import flask
import os
import rq
import redis
from mam import single


redis_conn = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost'))
q = rq.Queue('mam', connection=redis_conn)  # no args implies the default queue

app = flask.Flask('MAM')

@app.route('/')
def hello_world():
    return 'Nothing Here'


@app.route('/<document_id>', methods=['GET', 'POST'])
def trigger_mam(document_id):
    q.enqueue(single, document_id)
    return 'OK'
