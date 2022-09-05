from flask import Flask
from flask_restful import Api
from flask_caching import Cache
from flask_cors import CORS, cross_origin

from app.mono import MonoHandler

app = Flask(__name__)
CORS(app)
api = Api(app)
mono = MonoHandler()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)


@app.route("/api/transactions")
@cache.cached(timeout=60)
@cross_origin()
def last_transactions():
    return mono.get_last_transactions()


@app.route("/api/best")
@cache.cached(timeout=60)
@cross_origin()
def best_donate():
    return {'donate': mono.get_best_donate()}
