- Replace `#!C:\\Python27\\python.exe` by your python path
- Configure your apache-cgi like this:

```
<Directory "c:/wamp/cgi-bin"> #your cgi path
    AllowOverride None
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Order allow,deny
    Allow from all
    AddHandler cgi-script .py
	AddHandler default-handler .xhtml .html .htm .gif .png .bmp .jpg .svg #added support for images and "xml/html"
</Directory>
```
