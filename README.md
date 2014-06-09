html2canvas-proxy-python
========================

Python Proxy for html2canvas (tested in Python 2.7.3)

Although I have just added an example with "Flask" is library works with any "Python Web framework." Soon I'll add examples with other frameworks.

### Others scripting language ###

You do not use PHP, but need html2canvas working with proxy, see other proxies:

* [html2canvas proxy in php](https://github.com/brcontainer/html2canvas-php-proxy)
* [html2canvas proxy in asp.net (csharp)](https://github.com/brcontainer/html2canvas-csharp-proxy)
* [html2canvas proxy in asp classic (vbscript)](https://github.com/brcontainer/html2canvas-asp-vbscript-proxy)

### Provisional documentation:

Module | Description | Usage/Example
--- | --- | ---
* | For import module, add this in your .py file (on document top) | `from html2canvasproxy import *`
html2canvasproxy([callback get param], [url get param]) | Config html2canvasproxy | `h2c = html2canvasproxy(request.args.get("callback"), request.args.get("url"))`
html2canvasproxy.userAgent([user agent]) | Config webbrowser user-agent | `h2c.userAgent(request.headers['user_agent'])`
`html2canvasproxy.referer([referer])` | Config referer page (If needed) | `h2c.referer(request.referer)`
`html2canvasproxy.route([real path], [virtual path])` | Config "route" for images and real path (folder to save images). Note: "real path" is absolute path eg. `/home/user/project1/images`, "virtual path" should be as you want it to appear in the "address bar", eg. `/images` | `h2c.route('/home/guilherme/projects/site/images', '/images')`
`html2canvasproxy.result()` | Run proxy/Get response and mime-type by proxy | Read [Get results with proxy]
`html2canvasproxy.resource([real path], [image])` | Get resource saved and mime-type by proxy "real path" is same in `html2canvas.route([real path], [virtual path])` | Read [Get resources with proxy]

#Get results with proxy

```python
r = h2c.result()

print r['mime']
print r['data']
```

### Get results with proxy
Get resource saved and mime-type by proxy

```python
res = html2canvasproxy.resource(real_path, image)

print res['mime']
print res['data']
```
