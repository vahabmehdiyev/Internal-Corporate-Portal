from flask import request
from functools import wraps
from api.auth.auth_model import IPAddress
from config.database import db
import json
import time


def get_client_ip(ws=None):
    """
    Returns the client's IP address.
    - For HTTP requests, checks the `X-Forwarded-For` header.
    - For WebSocket connections, uses `ws.environ.get('REMOTE_ADDR')`.
    - Cleans up IPv6-formatted IPs (e.g., `::ffff:192.168.1.10`).
    """
    if ws:  # If it is a WebSocket connection
        ip = ws.environ.get('REMOTE_ADDR', '')
    else:  # If it is a regular HTTP request
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()  # Take the first IP
        else:
            ip = request.remote_addr  # If the header is missing, use remote_addr

    return ip.replace("::ffff:", "")  # Remove IPv6 prefix

def is_ip_allowed(client_ip):
    """
    Checks if the client's IP is allowed.
    - If this IP exists in the database, it is allowed.
    - Otherwise, access is denied.
    """
    return db.session.query(IPAddress).filter_by(ip_address=client_ip).first() is not None

def ip_required(f):
    """
    Decorator for checking IP addresses in HTTP requests.
    - Returns 403 if the IP is not allowed.
    """

    @wraps(f)
    def decorator_function(*args, **kwargs):
        client_ip = get_client_ip()  # Get the client's IP

        if not is_ip_allowed(client_ip):
            return {"message": "У вас недостаточно прав для просмотра этой страницы"}, 403

        return f(*args, **kwargs)

    return decorator_function

def ip_required_ws(f):
    """
    Decorator for checking IP addresses in WebSocket connections.
    - If the IP is not allowed, sends a 403 code and message, then closes the connection.
    """

    @wraps(f)
    def decorator_function(ws, *args, **kwargs):
        client_ip = get_client_ip(ws)  # Get the client's IP for WebSocket

        if not is_ip_allowed(client_ip):
            data = {
                "data": {
                    "code": 403,
                    "message": "У вас недостаточно прав для просмотра этой страницы"
                }
            }

            try:
                ws.send(json.dumps(data, ensure_ascii=False))  #  Ensure Unicode is correctly formatted
                time.sleep(0.5)  #Wait a bit to allow the message to be fully sent
                ws.close()  #Close the WebSocket connection
            except Exception as e:
                print(f"WebSocket send error: {e}")  # Log any errors

            return  #  End function execution, WebSocket will no longer function

        return f(ws, *args, **kwargs)  # If allowed, proceed

    return decorator_function

def pagination(query, current_page, per_page):
    total_items = len(query)
    total_pages = (total_items + per_page - 1) // per_page

    if total_pages == 0:
        return {
            "response": [],
            "is_end": True,
            "current_page": 1,
        }

    if current_page > total_pages:
        current_page = total_pages

    if current_page < 1:
        current_page = 1

    offset = (current_page - 1) * per_page
    data = query[offset:offset + per_page]

    is_end = current_page == total_pages

    return {
        "response": data,
        "is_end": is_end,
        "current_page": current_page,
    }