from selfsigned import generate_selfsigned_cert
from ipaddress import IPv4Address

if __name__ == '__main__':
    hostname = 'zkz.me'
    public_ip, private_ip = [IPv4Address('127.0.0.1')]*2
    files = dict()
    files['cert.pem'], files['key.pem'] = generate_selfsigned_cert(hostname, public_ip, private_ip)
    for filename, content in files.items():
        with open(filename, 'wb') as f:
            f.write(content)
