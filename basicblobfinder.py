#!/usr/bin/env python3
# Joshua Wright jwright@hasborg.com
import sys
import socket
import requests
import xml.etree.ElementTree as ET
import re

HOSTSUFFIX=".blob.core.windows.net"
URLPARAM="?restype=container&comp=list"

def print_blobs(xmlstr):
    root = ET.fromstring(xmlstr)
    for blob in root[0]:
        print(f"    {blob[1].text}") # URL to blob object

def resolve_name(hostname):
    try:
        socket.gethostbyname_ex(hostname)
    except:
        return False
    return True

if (len(sys.argv) != 2):
    print("""Test for the presence of Azure Blob resources.
This is a naive PoC to test for the presence of Azure Blob resources which could
certainly benefit from threading and other performance improvements.\n""")

    print(f"Usage: {sys.argv[0]} <name list file>")
    print("""
The name list file should be in the format storageaccount:containername or a
single string that is used as both the storage account and container name.
(ex. falsimentis:falsimentis-container or falsimentis). Invalid names are skipped.
""")
    sys.exit(0)

with open(sys.argv[1]) as fp:
    for cnt,line in enumerate(fp):
        line=line.rstrip()
        if (not ":" in line):
            # Treat the string in the line as both storage acct name and blob name
            storacct = line
            cntrname = line
        else:
            storacct,cntrname = line.split(":")

        # "The field can contain only lowercase letters and numbers. Name must
        # be between 3 and 24 characters."
        if (re.search("[^a-z0-9]", storacct) or len(storacct) < 3 or len(storacct) > 24):
            print(f"Invalid storage account name {storacct}, skipping.")
            continue

        # "This name may only contain lowercase letters, numbers, and hyphens,
        # and must begin with a letter or a number. Each hyphen must be
        # preceded and followed by a non-hyphen character. The name must also
        # be between 3 and 63 characters long."
        if (re.search("[^a-z0-9\-]", cntrname) or "--" in cntrname or len(cntrname) < 3 or len(cntrname) > 63):
            print(f"Invalid container name {cntrname}, skipping.")
            continue

        # Unlike other cloud storage providers, Azure doesn't do a wildcard DNS resolver
        # Before we look for the blob with an HTTP request, resolve the DNS name of
        # the storage account.
        if (not resolve_name(f"{storacct}{HOSTSUFFIX}")):
            #print(f"Skipping storage account {storacct} (does not resolve)")
            continue
        url = f"https://{storacct}{HOSTSUFFIX}/{cntrname}{URLPARAM}"
        try:
            r = requests.get(url)
        except requests.ConnectionError:
            print("failed to connect")
        if (r.status_code == 200):
            print(f"\nValid storage account and container name: {line}")
            print("Blob data objects:")
            print_blobs(r.text)
        #else:
            #print(f"Invalid account and blob: {line}")

