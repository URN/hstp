import sys
import requests

for line in sys.stdin:
    [url, path] = line.split()

    a = requests.get(url, allow_redirects=True)
    if a.status_code != 200 or a.headers['Content-length'] == 94:
        print(f"{url}\t{path}")
    else:
        with open(path, 'wb') as f:
            f.write(a.content)
