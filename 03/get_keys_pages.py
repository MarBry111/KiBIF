import numpy as np
from subprocess import getoutput
import sys
import ssl
from OpenSSL import crypto
#https://security.stackexchange.com/questions/16085/how-to-get-public-key-of-a-secure-webpage

hostname = 'www.facebook.com'
port = 443

key = getoutput('openssl s_client -connect '+hostname+':'+str(port)+' | openssl x509 -pubkey -noout')
print(key)

#https://stackoverflow.com/questions/41171891/how-to-download-x509-certificate-using-python
cert = ssl.get_server_certificate((hostname, port))

#https://stackoverflow.com/questions/41172839/how-to-convert-the-x509-get-pubkey-to-hexadecimal-in-python
#https://stackoverflow.com/questions/7689941/how-can-i-retrieve-the-tls-ssl-peer-certificate-of-a-remote-host-using-python
x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
key = crypto.dump_publickey(crypto.FILETYPE_PEM,x509.get_pubkey())
key = key.decode()
print(key)


#https://stackoverflow.com/questions/10362965/how-to-get-public-key-using-pyopenssl
