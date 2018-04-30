#! /usr/bin/env python3
import sys

def quitt(r, t):
    if r.lower() != t.lower():
        print("exiting...")
        sys.exit(0)

print("""Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator manual, Installer None
Cert not yet due for renewal

You have an existing certificate that has exactly the same domains or certificate name you requested and isn't close to expiry.
(ref: /etc/letsencrypt/renewal/example.com.conf)

What would you like to do?
-------------------------------------------------------------------------------
1: Keep the existing certificate for now
2: Renew & replace the cert (limit ~5 per 7 days)
-------------------------------------------------------------------------------
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): """, end="")
resp = input()
quitt(resp, "2")
print("""
-------------------------------------------------------------------------------
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about EFF and
our work to encrypt the web, protect its users and defend digital rights.
-------------------------------------------------------------------------------
(Y)es/(N)o: """, end="")
resp = input()
quitt(resp, "y")
print("""Renewing an existing certificate
Performing the following challenges:
dns-01 challenge for example.com

-------------------------------------------------------------------------------
NOTE: The IP of this machine will be publicly logged as having requested this
certificate. If you're running certbot in manual mode on a machine that is not
your server, please ensure you're okay with that.

Are you OK with your IP being logged?
-------------------------------------------------------------------------------
(Y)es/(N)o: """, end="")
resp = input()
quitt(resp, "y")
print("""
-------------------------------------------------------------------------------
Please deploy a DNS TXT record under the name
_acme-challenge.example.com with the following value:

XVhgIIfI7iG2j7UXDjjbLRf0PdYkZLGy8chLu2_2tjU

Before continuing, verify the record is deployed.
-------------------------------------------------------------------------------
Press Enter to Continue""", end="")
input()
print("""
Before continuing, verify the record is deployed.
-------------------------------------------------------------------------------
Press Enter to Continue
Waiting for verification...
Cleaning up challenges
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/example.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/example.com/privkey.pem
   Your cert will expire on 2018-07-29. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot-auto
   again. To non-interactively renew *all* of your certificates, run
   "certbot-auto renew"
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
""", end="")