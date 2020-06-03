# 02장 파이썬 웹 표준 라이브러리

## urlopen()함수 - GET 방식 요청

```python
from urllib.request import urlopen

f = urlopen("http://www.example.com")

print(f.read(500).decode('utf-8'))
```

## urlopen()함수 - POST 방식 요청

```python
from urllib.request import urlopen


data = "language=python&framework=django"
f = urlopen("http://127.0.0.1:8000", bytes(data, encoding='utf-8'))

print(f.read(500).decode('utf-8'))
```

## urlopen() 함수 - Request 클래스로 요청 해더 지정

```python
from urllib.request import urlopen, Request
from urllib.parse import urlencode


url = 'http://127.0.0.1:8000'

data = {
    'name': '김석훈',
    'email': 'shkim@naver.com',
    'url': 'http://www.naver.com',
}
encData = urlencode(data)
postData = bytes(encData, encoding='utf-8')

req = Request(url, data=postData)
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

f = urlopen(req)

print(f.info())
print(f.read(500).decode('utf-8'))
```

## urlopen() 함수 - HTTPBasicAuthHandler 클래스로 인증 요청

```python
from urllib.request import HTTPBasicAuthHandler, build_opener


auth_handler = HTTPBasicAuthHandler()
auth_handler.add_password(realm='ksh', user='shkim', passwd='shkimadmin', uri='http://127.0.0.1:8000/auth/')  # OK
# NOK. auth_handler.add_password(realm='ksh', user='shkim', passwd='shkimadmin', uri='http://127.0.0.1:8000/')
opener = build_opener(auth_handler)
resp = opener.open('http://127.0.0.1:8000/auth/')
print(resp.read().decode('utf-8'))
```

## urlopen() 함수 - HTTPCookieProcessor 클래스로 쿠키 데이터를 포함하여 요청

```python
from urllib.request import Request, HTTPCookieProcessor, build_opener


url = 'http://127.0.0.1:8000/cookie/'

# first request (GET) with cookie handler

# 쿠키 핸들러 생성, 쿠키 데이터 저장은 디폴트로 CookieJar 객체를 사용함
cookie_handler = HTTPCookieProcessor()
opener = build_opener(cookie_handler)

req = Request(url)
res = opener.open(req)

print(res.info())
print(res.read().decode('utf-8'))

# second request (POST)
print("-------------------------------------------------------")

data = "language=python&framework=django"
encData = bytes(data, encoding='utf-8')

req = Request(url, encData)
res = opener.open(req)

print(res.info())
print(res.read().decode('utf-8'))
```

## urlopen()함수 - ProxyHandler 및 ProxyBasicAuthHandler 클래스로 프록시 처리

```python
import urllib.request


url = 'http://www.example.com'
proxyServer = 'http://www.proxy.com:3128/'

# 프록시 서버를 통해 웹서버로 요청을 보냅니다.
proxy_handler = urllib.request.ProxyHandler({'http': proxyServer})

# 프록시 서버 설정을 무시하고 웹서버로 요청을 보냅니다.
# proxy_handler = urllib.request.ProxyHandler({})

# 프록시 서버에 대한 인증을 처리합니다.
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

# 2개의 핸들러를 오프너에 등록합니다.
opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)

# 디폴트 오프너로 지정하면, urlopen() 함수로 요청을 보낼 수 있습니다.
urllib.request.install_opener(opener)

# opener.open() 대신에 urlopen()을 사용했습니다.
f = urllib.request.urlopen(url)

print("geturl():", f.geturl())
print(f.read(300).decode('utf-8'))
```

## urllib.request모듈 예제

> parse_image.py

```python
from urllib.request import urlopen
from html.parser import HTMLParser


class ImageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        for name, value in attrs:
            if name == 'src':
                self.result.append(value)


def parse_image(data):
    parser = ImageParser()
    parser.feed(data)
    dataSet = set(x for x in parser.result)
    return dataSet


def main():
    url = "http://www.google.co.kr"

    with urlopen(url) as f:
        charset = f.info().get_param('charset')
        data = f.read().decode(charset)

    dataSet = parse_image(data)
    print("\n>>>>>>>>> Fetch Images from", url)
    print('\n'.join(sorted(dataSet)))


if __name__ == '__main__':
    main()
```

## http.client 모듈 사용 - GET 방식

```python
from http.client import HTTPConnection

host = 'www.example.com'
conn = HTTPConnection(host)

conn.request('GET', '/')

r1 = conn.getresponse()
print(r1.status, r1.reason)

data1 = r1.read()
# 일부만 읽는 경우
# data1 = r1.read(100)

# 두번째 요청에 대한 테스트
conn.request('GET', '/')

r2 = conn.getresponse()
print(r2.status, r2.reason)

data2 = r2.read()
print(data2.decode())

conn.close()
```

## http.client 모듈 사용 - HEAD 방식 요청

```python
from http.client import HTTPConnection

conn = HTTPConnection('www.example.com')
conn.request('HEAD', '/')

resp = conn.getresponse()
print(resp.status, resp.reason)

data = resp.read()
print(len(data))
print(data == b'')
```

## http.client 모듈 사용 - POST 방식 요청

```python
from http.client import HTTPConnection
from urllib.parse import urlencode


host = '127.0.0.1:8000'
params = urlencode({
    'language': 'python',
    'name': '김석훈',
    'email': 'shkim@naver.com',
})
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain',
}

conn = HTTPConnection(host)
conn.request('POST', '', params, headers)
resp = conn.getresponse()
print(resp.status, resp.reason)

data = resp.read()
print(data.decode('utf-8'))

conn.close()
```

## http.client 모듈 사용 - PUT 방식 요청

```python
from http.client import HTTPConnection
from urllib.parse import urlencode


host = '127.0.0.1:8000'
params = urlencode({
    'language': 'python',
    'name': '김석훈',
    'email': 'shkim@naver.com',
})
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain',
}

conn = HTTPConnection(host)
conn.request('PUT', '', params, headers)
resp = conn.getresponse()
print(resp.status, resp.reason)

data = resp.read(300)
print(data.decode('utf-8'))

conn.close()
```

## http.client 모듈 예제

> download_image.py

```python
import os
from http.client import HTTPConnection
from urllib.parse import urljoin, urlunparse
from urllib.request import urlretrieve
from html.parser import HTMLParser


class ImageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        for name, value in attrs:
            if name == 'src':
                self.result.append(value)


def download_image(url, data):

    if not os.path.exists('DOWNLOAD'):
        os.makedirs('DOWNLOAD')

    parser = ImageParser()
    parser.feed(data)
    dataSet = set(x for x in parser.result)

    for x in sorted(dataSet) :
        imageUrl = urljoin(url, x)
        basename = os.path.basename(imageUrl)
        targetFile = os.path.join('DOWNLOAD', basename)

        print("Downloading...", imageUrl)
        urlretrieve(imageUrl, targetFile)


def main():
    host = "www.google.co.kr"

    conn = HTTPConnection(host)
    conn.request("GET", '')
    resp = conn.getresponse()

    charset = resp.msg.get_param('charset')
    data = resp.read().decode(charset)
    conn.close()

    print("\n>>>>>>>>> Download Images from", host)
    url = urlunparse(('http', host, '', '', '', ''))
    download_image(url, data)


if __name__ == '__main__':
    main()
```

## 간단한 웹 서버 만들기

> my_httpserver.py

```python
from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200, 'OK')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello World")


if __name__ == '__main__':
    server = HTTPServer(('', 8888), MyHandler)
    print("Started WebServer on port 8888...")
    print("Press ^C to quit WebServer.")
    server.serve_forever()
```

## CGI 웹 서버 시험용 CGI 스크립트

> cgi_client.py

```python
from urllib.request import urlopen
from urllib.parse import urlencode


url = "http://127.0.0.1:8888/cgi-bin/script.py"
data = {
    'name': '김석훈',
    'email': 'shkim@naver.com',
    'url': 'http://www.naver.com',
}
encData = urlencode(data)
postData = encData.encode('ascii')

f = urlopen(url, postData)   # POST
print(f.read().decode('cp949'))
```
