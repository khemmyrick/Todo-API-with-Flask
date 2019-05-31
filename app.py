from flask import Flask, render_template

from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

import config
import models
from resources.todos import todos_api

app = Flask(__name__)
app.register_blueprint(todos_api, url_prefix='/api/v1')


limiter = Limiter(
    app,
    global_limits=[config.DEFAULT_RATE],
    key_func=get_ipaddr
)
limiter.limit(
    '100/day',
    per_method=True,
    methods=['post', 'put', 'delete']
)(todos_api)


@app.route('/')
def my_todos():
    return render_template('index.html')


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
