from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions

app = Flask(__name__)
app.config['DEBUG'] = True

def json_errorhandler(exception):
    """Create a JSON-encoded flask Response from an Exception."""

    if isinstance(exception, HTTPException):
        message = exception.description
        error_code = exception.code
    else:
        message = 'Internal server error'
        error_code = 500

    response = jsonify({'message': message, 'error': True})
    response.status_code = error_code

    return response


for code in default_exceptions:
    app.register_error_handler(code, json_errorhandler)
