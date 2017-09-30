# html2canvas-python-proxy 0.1.0
# Copyright (c) 2017 Guilherme Nascimento (brcontainer@yahoo.com.br)
#
# Released under the MIT license

import random
import time
import hashlib
import urllib2
import urlparse
import base64
import json
import re
import os

class html2canvasproxy:
    #Config (If need)
    folder = 'images'
    timeout = 30
    mimetype = 'application/javascript'

    #commons
    ua = ''
    host = ''
    scheme = ''
    ref = ''
    url = ''
    http_username = ''
    http_password = ''
    callback = ''
    data = ''
    response = ''
    status = 0
    route_path = '/'
    save_path = '/'
    prefix = 'htc_'
    real_extension = ''
    real_mimetype = ''
    real_charset = ''
    init_exec = time.time()
    ccache = 60 * 5 * 1000
    cross_domain = False
    mimes = [
        'image/bmp', 'image/windows-bmp', 'image/ms-bmp',
        'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
        'text/html', 'application/xhtml', 'application/xhtml+xml',
        'image/svg+xml', 'image/svg-xml'
    ]

    def __init__(self, callback, url):
        if callback is not None and re.match('[^A-Za-z0-9_[.]\\[\\]]', callback) is not None:
            self.set_response('error:Parameter "callback" contains invalid characters (' + callback + ')')
        elif url == '' or url is None:
            self.set_response('error:No such parameter "url"')
        elif html2canvasproxy.is_http_url(url) == False:
            self.set_response('error:Only http scheme and https scheme are allowed (' + url + ')')
        else:
            self.callback = callback

            o = urlparse.urlparse(url)

            if o.username is not None:
                self.http_username = o.username

            if o.password is not None:
                self.http_password = o.password

            if self.http_username != '' or self.http_password != '':
                uri = (o.netloc.split('@'))[1]
            else:
                uri = o.netloc

            self.url = o.scheme + '://' + uri + o.path

            if o.query != '':
                self.url += '?' + o.query

    def enable_crossdomain(self):
        self.cross_domain = True;

    def initiate(self):
        if self.status != 0:
            return None

        self.download_source()

    def download_source(self):
        headers = { 'User-Agent' : self.ua }

        if self.ref != '':
            o = urlparse.urlparse(self.ref)
            self.scheme = o.scheme
            self.host = o.netloc

            headers['Referer'] = self.ref

        if self.http_username != '' or self.http_password != '':
            auth = self.http_username + ':' + self.http_password
            auth = auth.encode('ascii')
            auth = base64.b64encode(auth)

            headers['Authorization'] = 'Basic ' + auth

        try:
            req = urllib2.Request(self.url, None, headers)
            r = urllib2.urlopen(req)
            h = r.info()

            if h['Content-Type'] != '' and h['Content-Type'] != None:
                if re.match('^(image|text|application)\/', h['Content-Type']) is None:
                    self.set_response('error:Invalid mime-type: ' + h['Content-Type'])
                else:
                    mime = str(re.sub('[;]([\s\S]+)$', '', h['Content-Type'])).strip().lower()
                    mime = re.sub('/x-', '/', mime)

                    if mime in self.mimes:
                        self.data = r.read()

                        extension = re.sub('^(image|text|application)\/', '', mime)
                        extension = re.sub('(windows[-]bmp|ms[-]bmp)', 'bmp', extension)
                        extension = re.sub('(svg[+]xml|svg[-]xml)', 'svg', extension)
                        extension = extension.replace('xhtml[+]xml', 'xhtml')
                        extension = extension.replace('jpeg', 'jpg')

                        self.real_extension = extension
                        self.real_mimetype  = mime

                        cp = h['Content-Type'].find(';');

                        if cp != -1:
                            cp = cp + 1
                            charset = h['Content-Type']
                            self.real_charset = ';' + charset[cp:].strip()

                        self.save_file()
                    else:
                        self.set_response('error:Invalid mime-type: ' + h['Content-Type'])
            else:
                self.set_response('error:No mime-type defined')

            r.close()
        except urllib2.URLError, e:
            self.set_response('error:SOCKET: ' + str(e.reason))

    def remove_old_files(self):
        a = []
        for f in os.listdir(self.save_path):
            if f.find(self.prefix) == 0 and os.path.isfile(self.save_path + f) and ((self.init_exec - os.path.getctime(self.save_path + f))) > (self.ccache * 2):
                os.unlink(self.save_path + f)

    def save_file(self):
        file_name = hashlib.sha1(self.url).hexdigest()
        tmp_ext = str(random.randrange(1000)) + '_' + str(self.init_exec)

        if os.path.isfile(self.save_path + file_name + '.' + tmp_ext):
            self.save_file() #try again
        else:
            f = open(self.save_path + file_name + '.' + tmp_ext, 'wb')
            f.write(self.data)
            f.close()

            if os.path.isfile(self.save_path + file_name + '.' + self.real_extension):
                os.remove(self.save_path + file_name + '.' + self.real_extension)

            os.rename(self.save_path + file_name + '.' + tmp_ext, self.save_path + file_name + '.' + self.real_extension)

            self.set_response(self.scheme + '://' + self.host + self.route_path + file_name + '.' + self.real_extension)

    def hostname(self, url):
        if url == '' or url is None:
            self.set_response('error:No such host in html2canvasproxy.hostname("url")')
        if html2canvasproxy.is_http_url(url) == False:
            self.set_response('error:Only http scheme and https scheme are allowed in html2canvasproxy.hostname(' + url + ')')
        elif self.ref == '':
            o = urlparse.urlparse(url)

            self.scheme = o.scheme
            self.host = o.netloc

    def referer(self, url):
        if url == '' or url is None:
            self.set_response('error:No such referer in html2canvasproxy.referer("url")')

        if html2canvasproxy.is_http_url(url) == False:
            self.set_response('error:Only http scheme and https scheme are allowed in html2canvasproxy.referer(' + url + ')')
        else:
            self.ref = url

            o = urlparse.urlparse(url)

            self.scheme = o.scheme
            self.host = o.netloc

    def route(self, current_path, route):
        if re.match('(^/|[a-zA-Z][:])', current_path) is None:
            self.set_response('error:Invalid current_path (' + current_path + ')')
        else:
            current_path = current_path.replace('\\', '/')

            if not os.path.isdir(current_path):
                self.set_response('error:Not found ' + current_path)
            else:
                self.save_path = html2canvasproxy.fix_path(current_path)
                self.route_path = '/' + route.strip('/') + '/';

    def useragent(self, ua):
        self.ua = ua

    def result(self):
        if self.response == '':
            self.initiate()

        self.remove_old_files()

        if self.callback is None:
            return {
                'mime': self.real_mimetype,
                'data': self.data
            }
        elif self.cross_domain:
            duheader = re.sub('(^"|"$)', '',
                json.dumps(self.real_mimetype + self.real_charset)
            )

            if self.real_extension == 'svg' or re.match('^image/', self.real_mimetype) is None:
                return {
                    'mime': self.mimetype,
                    'data': self.callback + '("data:' + duheader + ',' + html2canvasproxy.ascii_to_inline(self.data) + '");'
                }
            else:
                return {
                    'mime': self.mimetype,
                    'data': self.callback + '("data:' + duheader + ';base64,' + base64.b64encode(self.data) + '");'
                }
        else:
            return {
                'mime': self.mimetype,
                'data': self.callback + '(' + json.dumps(self.response) + ');'
            }

    def set_response(self, resp):
        if self.response == '':
            self.status = 2
            self.response = str(resp)

    def debug_vars(self):
        return self.__dict__

    @staticmethod
    def ascii_to_inline(str):
        i = 0;
        x = {
            '\n': '%0A',
            '\r': '%0D',
            ' ': '%20',
            '"': '%22',
            '#': '%23',
            '&': '%26',
            '\/': '%2F',
            '\\': '%5C',
            ':': '%3A',
            '?': '%3F',
            '\0': '%00',
            '\b': '',
            '\t': '%09'
        }

        for (k, v) in x.items():
            str = str.replace(k, v)

        return str;

    @staticmethod
    def fix_path(path):
        path = re.sub('(\/|\\\\)$', '', path)
        if re.match('[a-zA-Z][:]\\\\', path) is not None:
            return path + '\\'
        else:
            return path + '/'

    @staticmethod
    def resource(current_path, f):
        current_path = html2canvasproxy.fix_path(current_path)

        if os.path.isfile(current_path + f):
            fileName, ext = os.path.splitext(f)

            mime = 'application/octet-stream'

            ext = re.sub('^[.]', '', ext)

            if re.match('^(jp|bm|gi|pn)', ext) is not None:
                mime = 'image/' + ext
            elif ext == 'xhtml':
                mime = 'application/xml+xhtml'
            elif ext == 'svg':
                mime = 'image/svg+xml'
            elif ext == 'html':
                mime = 'text/html'

            fullpath = current_path + '/' + f

            f = open(fullpath, 'rb')
            data = f.read(os.stat(fullpath).st_size)
            f.close()

            return { 'mime': mime, 'data': data }
        else:
            return None

    @staticmethod
    def is_http_url(url):
        return re.match('^http(|s)[:][/][/][a-zA-Z0-9]', url) is not None
