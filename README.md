html2canvas-python-proxy 0.0.8
========================

Python Proxy for html2canvas (tested in Python 2.7.3)

Although I have just added an example with "Flask" is library works with any "Python Web framework." Soon I'll add examples with other frameworks.

### Others scripting language ###

You do not use PHP, but need html2canvas working with proxy, see other proxies:

* [html2canvas proxy in php](https://github.com/brcontainer/html2canvas-php-proxy)
* [html2canvas proxy in asp.net (csharp)](https://github.com/brcontainer/html2canvas-csharp-proxy)
* [html2canvas proxy in asp classic (vbscript)](https://github.com/brcontainer/html2canvas-asp-vbscript-proxy)

### Provisional documentation:

Module | Description
--- | ---
`html2canvasproxy([callback get param], [url get param])` | Config html2canvasproxy
`html2canvasproxy.enable_crossdomain()` | Enable the use of ["Data URI scheme"](http://en.wikipedia.org/wiki/Data_URI_scheme)
`html2canvasproxy.useragent([user agent])` | Config webbrowser user-agent
`html2canvasproxy.hostname([url])` | Config current URL (requires scheme and port)
`html2canvasproxy.referer([referer])` | Config referer page (If needed)
`html2canvasproxy.route([real path], [virtual path])` | Config "route" for images and real path (folder to save images). Note: "real path" is absolute path eg. `/home/user/project1/images`, "virtual path" should be as you want it to appear in the "address bar", eg. `/images`
`html2canvasproxy.debug_vars()` | Get variables values for DEBUG
`html2canvasproxy.result()` | Run proxy/Get response and mime-type by proxy.
`html2canvasproxy.resource([real path], [image])` | Get resource saved and mime-type by proxy "real path" is same in `html2canvas.route([real path], [virtual path])`. Read [Get resources with proxy](https://github.com/brcontainer/html2canvas-python-proxy#get-results-with-proxy)

### How to use
A simple example of usage

```python
from html2canvasproxy import * #Load html2canvasproxy

#Set GET variables
h2c = html2canvasproxy(request.args.get("callback"), request.args.get("url"))

#Uncomment next line to enable "data URI scheme" (optional)
#h2c.enable_crossDomain()

#Set user-aget browser
if request.headers['user_agent']:
    h2c.useragent(request.headers['user_agent'])
else:
    h2c.useragent('Mozilla/5.0')

#Set current page
h2c.hostname(request.url)

#Set referer (If needed)
if request.referer:
    h2c.referer(request.referer)

#Set route (real path and virtual path)
h2c.route('/home/guilherme/projects/site/images', '/images')

#Results
print 'Debug:'
print h2c.debug_vars()
print '---------'

result = h2c.request()

print 'mime: ' + result['mime']
print 'data: ' + result['data']
print '=========\n'
```

### Get results with proxy
Run proxy/Get response and mime-type by proxy (returns `application/javascript`)

```python
r = h2c.result()

print r['mime']
print r['data']
```

### Get resources with proxy
Get resource saved and mime-type by proxy (returns images or html)

```python
res = html2canvasproxy.resource(real_path, image)

print res['mime']
print res['data']
```
