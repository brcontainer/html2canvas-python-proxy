# Example with flask
#
# Usage:
# Copy html2canvasproxy.py to project folder
# In terminal: python main.py
# Open browser with: http://127.0.0.1:5000/test-case/

from html2canvasproxy import * #include html2canvasproxy in your application
from flask import Flask, request, Response, render_template
import urlparse
import os
import re

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['DEBUG'] = True

h2c = None
real_path = os.getcwd() + '/images'
virtual_path = '/test-case/html2canvas/images/'

#Index/Root page
@app.route('/')
def index():
    return 'Index Page'

#Page for test-case http://127.0.0.1:5000/test-case/
@app.route('/test-case/')
def test_case():
    return app.send_static_file('test-case.html')

#Copy html2canvas.js to static folder (If not use cdns)
@app.route('/test-case/html2canvas.js')
def html2canvas_js():
    return app.send_static_file('html2canvas.js')

#Proxy url, http://127.0.0.1:5000/test-case/html2canvas-proxy?callback=function&url=http://page
@app.route('/test-case/html2canvas-proxy')
def html2canvas_proxy():
    h2c = html2canvasproxy(request.args.get('callback'), request.args.get('url'))
    h2c.userAgent(request.headers['user_agent'])

    if request.referrer is not None:
        h2c.referer(request.referrer)

    h2c.route(real_path, virtual_path)

    r = h2c.result()

    return Response(r['data'], mimetype=r['mime'])

#Get images saved by html2canvasproxy
@app.route('/test-case/html2canvas/images/<image>')
def images(image):
    res = html2canvasproxy.resource(real_path, image)

    if res is None:
        return '', 404
    else:
        return res['data']

if __name__ == '__main__':
    app.run()
