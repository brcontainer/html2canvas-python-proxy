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

#### Import modules

For import module, add this in your .py file (on top):

`from html2canvasproxy import *`

Config html2canvasproxy (`h2c` is an variable):

`h2c = html2canvasproxy([callback get param], [url get param])`

Config webbrowser user-agent:

`h2c.userAgent([user agent])`

Config referer page (If needed):

`h2c.referer([referer])`

Config "route" for images and real path (folder to save images):

`h2c.route([real path], [virtual path])`

Run proxy:

`r = h2c.result()`

Get response and mime-type by proxy:

```py
r = h2c.result()

print r['mime']
print r['data']
```

Get resource saved:
`res = html2canvasproxy.resource(real_path, image)`

Get resource and mime-type saved by proxy:

```py
res = html2canvasproxy.resource(real_path, image)

print res['mime']
print res['data']
```
