from functools import wraps
import base64
from quartapp.authentification.users import users

from quart import Response, request

secret_key = ''

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return users.get(username) == password

def authenticate():
    """Sends a 401 response that enables basic auth."""
    return Response(
        'Could not verify your login!\n'
        'Please log in with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return authenticate()

        parts = auth.split()
        if parts[0].lower() != 'basic':
            return authenticate()
        elif len(parts) == 1:
            return authenticate()
        elif len(parts) > 2:
            return authenticate()

        try:
            auth_decoded = base64.b64decode(parts[1]).decode('utf-8')
            username, password = auth_decoded.split(':', 1)
        except Exception as e:
            return authenticate()

        if not check_auth(username, password):
            return authenticate()

        return await f(*args, **kwargs)
    return decorated