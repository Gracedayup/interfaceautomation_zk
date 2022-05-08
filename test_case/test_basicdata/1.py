

import requests

url = 'http://192.168.0.139/fmw/commonStaff/downloadTemplate'
res = requests.get(url)

print(res.status_code)
print(res.text)


# from urllib import request
#
#
#
# with request.urlopen('http://192.168.0.139/fmw/commonStaff/downloadTemplate') as f:
#     data = f.read()
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', data)
