#!/usr/bin/env python3
import subprocess
import dns_server
CERTBOT_COMMAND =  ['./simulate_certbot.py']


def skip_lines(process, ln):
    for i in range(ln):
        line = process.stdout.readline()
        print(line)


def deploy_dns(token):
    print("deploy dns token:", token)
    dns_server.main()



def send(process, txt):
    print(txt)
    process.stdin.write(txt)
    process.stdin.flush()


def main():
    process = subprocess.Popen(CERTBOT_COMMAND, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    try:
        success = False
        state = 0
        while True:
            line = process.stdout.readline()
            print(len(line), line)
            if state == 0:
                if b'Renew & replace the cert' in line:
                    state = 1
                elif b'Would you be willing to share your email address' in line:
                    skip_lines(process, 3)
                    state = 2
                elif b'The IP of this machine will be publicly logged' in line:
                    skip_lines(process, 4)
                    state = 2
                elif b'Please deploy a DNS TXT' in line:
                    skip_lines(process, 2)
                    state = 3
            elif state == 1:
                print(line)
                send(process, b"2\n")
                state = 0
            elif state == 2:
                send(process, b"y\n")
                state = 0
            elif state == 3:
                deploy_dns(line.strip())
                skip_lines(process, 3)
                send(process, b"\n")
                state = 4
            elif state == 4:
                if b'Congratulations!' in line:
                    success = True
                    break
    except:
        raise
    finally:
        print(success)
        process.communicate(timeout=1)

if __name__ == "__main__":
    main()