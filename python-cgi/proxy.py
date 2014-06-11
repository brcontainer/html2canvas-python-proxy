#!C:\\Python27\\python.exe

"""
	Copy html2canvasproxy.py to this folder
	Replace `#!C:\\Python27\\python.exe`
"""

from html2canvasproxy import *

import os
import cgi
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

url = form.getvalue('url')
callback = form.getvalue('callback')
debug_vars = form.getvalue('debug_vars')

real_path = os.path.dirname(os.path.realpath(__file__)) + '\\images'
virtual_path = 'cgi-bin/html2canvas/images'

h2c = html2canvasproxy(callback, url)

if 'HTTP_HOST' in os.environ:
    host = 'http://' + os.environ['HTTP_HOST']
else:
    host = 'http://localhost' #alternative HOST, define your domain eg. http://mywebsite.io

h2c.hostName(host)

#if 'HTTP_REFERER' in os.environ:
#h2c.referer('http://' + os.environ['HTTP_REFERER'])
h2c.referer('http://localhost')

if 'HTTP_USER_AGENT' in os.environ:
    user_agent = os.environ['HTTP_USER_AGENT']
else:
    h2c.userAgent('Mozilla/5.0')

h2c.route(real_path, virtual_path)

if debug_vars:
    print 'Content-Type: text/plain\r\n'
    print h2c.debug_vars()
else:
    r = h2c.result()

    print 'Content-Type: ' + r['mime'] + '\r\n'
    print r['data']
