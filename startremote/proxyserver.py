from flask import Flask, request, Response
import requests

app = Flask(__name__)
server_map = {
    '/dan':'http://192.168.1.66',
    '/jonathan':'http://192.168.1.70',
    '/mypc':'http://192.168.1.65',
}

def proxy_request(path, target_url):
    """Proxy the request to the target URL."""
    url = f"{target_url}{path}"
    headers = {key: value for key, value in request.headers if key != 'Host'}

    # Forward the request method and data to the target server
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    # Build a Flask response object
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(response.content, response.status_code, headers)
    return response

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    """Route the request to the appropriate server based on the path prefix."""
    for prefix, target_url in server_map.items():
        if path.startswith(prefix.lstrip('/')):
            new_path = path[len(prefix):]
            return proxy_request(new_path, target_url)
    return "Path not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
