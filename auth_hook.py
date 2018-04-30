#! /usr/bin/env python3
import os
import time

dns_server_path = os.path.join(os.path.dirname(__file__), 'dns_server.py')
dns_server_log = os.path.join(os.path.dirname(__file__), 'auth_hook.log')
cmd = """bash -c "%s > %s & sleep 10; disown -a" """ % (dns_server_path, dns_server_log)
# os.system(dns_server_path + " > " + dns_server_log +"  &")
# os.system("disown -a")
# time.sleep(10)
os.system(cmd)
print(__name__, ":", os.getenv("CERTBOT_VALIDATION"), os.getenv("CERTBOT_DOMAIN"))