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



def scrapper(url, fn=None, write_it=None):
    """ scraper
    Scrape the current pages for job details
    """
    soup = BeautifulSoup(urlopen(URL).read(), 'html.parser')
    target_elements = soup.findAll('div', attrs={'data-tn-component': 'organicJob'})

    for x in target_elements:
        company = x.find('span', attrs={"itemprop":"name"})
        if company:
          print ('company:', company.text.strip())

        job = x.find('a', attrs={'data-tn-element': "jobTitle"})
        if job:
          print ('job:', job.text.strip())

        href = x.find('a', attrs={'class':'turnstileLink'})['href']
        job_link = "%s%s" % (home_url, href)
        print  ('job link: ', job_link)

        salary = x.find('nobr')
        if salary:
          print ('salary:', salary.text.strip())


        print ('----------')

""" I like it like this....
How to use:
    python scrapy_indeed.py
    python scrapy_indeed.py "keywords"

    if you want to write the result to a file
    python scrapy_indeed.py "keywords" > <target_filename>

To Do:
   1. Add location in the argv
   2. Add writing to a file
"""
if __name__ == '__main__':

    jobs  = "python"
    if (sys.argv[1:]):
        jobs = sys.argv[1:]

    location = "melbourne"
    home_url = "http://www.indeed.com"
    page_number = "&start="

    pg_num = [0, 10, 20, 30, 40, 50]
    for p in pg_num:
        URL = "https://au.indeed.com/jobs?q=%s&l=%s" % (jobs, location)
        if p == 0:
            page_number = ""
        else:
            page_number = "&start=%i" % p

        URL = URL + page_number
        print("Page %i" % p)

        # lets start scrapping  
        scrapper(url=URL)
