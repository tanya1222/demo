from flask import Flask
from config import SECRET_KEY
from pillow.filterbp import filter_bp
from exception import internal_server_error

app = Flask(__name__)
app.config[''] = SECRET_KEY

app.register_blueprint(filter_bp)


app.register_error_handler(500, internal_server_error)

if __name__ == '__main__':
    app.run()
