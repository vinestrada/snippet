#!/usr/bin/env python
"""
__author__ = "Alvin Estrada"
__copyright__ = "Free-for-all"
__license__ = "GPL"
"""
import os
import sys
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin

# Make sure we have install BeautifulSoup
# pip install bs4
try:
    from bs4 import BeautifulSoup    # make HTML parsing easy
except ImportError:
    print("[*] - Please download and install BeautifulSoup!")
    sys.exit(0)


#
# Description: Download multiple files in the target website
#
def file_scraper(url, dl_path, ext='.pdf', debug_mode=False):
    """file_scraper
    Download files from the web.
    """
    if len(url) == 0: return
    if len(dl_path) == 0: return

    # Prentding to be a browser
    # User-Agent details found in http://www.useragentstring.com
    headers = {"User-Agent": "Mozilla/5.0 (Window NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
    try:
        i = 0
        request = Request(url, None, headers)
        page = urlopen(request).read()
        soup = BeautifulSoup(page)

        # We are interested in finding ALL the 'a' tag elements
        tag_link = soup.findAll('a')

        for tag in tag_link:
            tag['href'] = urljoin(url, tag['href'])
            #
            # Make sure we only going to download target files from the server, i.e pdf, docs, etc
            if os.path.splitext(os.path.basename(tag['href']))[1] == ext:

                if not debug_mode:
                    p = urlopen(tag['href'])

                print("\n[*] Downloading: %s" % (os.path.basename(tag['href'])))

                # Build download location
                fn = "%s%s" % (dl_path, os.path.basename(tag['href']))

                if not debug_mode:
                    with open(fn, "wb") as f:
                        f.write(p.read())
                        f.close()
                i += 1

        print("\n[**] Downloaded %d files" %(i + 1))
        input("[+] Press any key to exit....")


    except KeyboardInterrupt:
        print("[*] Exiting....")
        return 1
    except URLError as e:
        print("[*] Count not get information from server!")
        return 2
    except:
        print("I don't know the problem, sorry!")
        return 3

    return 0


if __name__ == "__main__":
    IS_DEBUG = True
    url = input("[+] Enter the url: ")
    local_path = input("[+] Enter the download path in full: ")
    ext = ".pdf"

    e = file_scraper(url = url,
                    dl_path = local_path,
                    ext = ext,
                    debug_mode = IS_DEBUG)

    if e != 0:
        sys.exit(e)
