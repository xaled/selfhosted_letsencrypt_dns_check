#! /usr/bin/env python3
#  coding=utf-8
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
CREDITS: https://gist.github.com/andreif/6069838 (Andrei Fokau)
"""
import datetime
import sys
import threading
import traceback
import socketserver
from dnslib import *


DOMAIN = os.getenv("CERTBOT_DOMAIN")
if DOMAIN.startswith("*."):
    DOMAIN = DOMAIN[2:]
if DOMAIN.endswith("."):
    DOMAIN = DOMAIN[:-1]
print(DOMAIN)
# IP = '10.1.1.1'
TTL = 60 * 5
PORT = 53
SLEEP = 60 * 1
RECORDS = {
    'TXT': ('TXT', TXT(os.getenv("CERTBOT_VALIDATION").encode())),
}


def dns_response(data):
    request = DNSRecord.parse(data)

    # print(request)

    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]
    # print(qn)
    print(qn, qt)
    if qn.endswith(DOMAIN) or qn.endswith(DOMAIN+'.'):
        print(request)
        # print(DOMAIN)
        # for name, rrs in records.iteritems():
        # if name == qn:
        # for rdata in rrs:
        #     rqt = rdata.__class__.__name__
        #     if qt in ['*', rqt]:
        if qt in RECORDS:
            reply.add_answer(RR(rname=qname, rtype=QTYPE.__getattr__(RECORDS[qt][0]), rclass=1, ttl=TTL, rdata=RECORDS[qt][1]))

        # for rdata in ns_records:
        #     reply.add_ns(RR(rname=D, rtype=QTYPE.NS, rclass=1, ttl=TTL, rdata=rdata))
        #
        # reply.add_ns(RR(rname=D, rtype=QTYPE.SOA, rclass=1, ttl=TTL, rdata=soa_record))

        print("---- Reply:\n", reply)

    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
                                               self.client_address[1]))
        try:
            data = self.get_data()
            # print(len(data), repr(data)) # repr(data).replace('\\x', '')[1:-1]
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):

    def get_data(self):
        data = self.request.recv(8192).strip()
        sz = int(data[:2].encode('hex'), 16)
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        sz = hex(len(data))[2:].zfill(4).decode('hex')
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


def main():
    print("Starting nameserver...")

    servers = [
        socketserver.ThreadingUDPServer(('', PORT), UDPRequestHandler),
        socketserver.ThreadingTCPServer(('', PORT), TCPRequestHandler),
    ]
    for s in servers:
        thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print("%s server loop running in thread: %s" % (s.RequestHandlerClass.__name__[:3], thread.name))

    try:

        time.sleep(SLEEP)
        sys.stderr.flush()
        sys.stdout.flush()

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        sys.exit(0)
    finally:
        print("Shutting Down.")
        for s in servers:
            s.shutdown()


if __name__ == '__main__':
    main()
