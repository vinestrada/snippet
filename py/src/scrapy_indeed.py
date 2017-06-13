import os
import sys
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin

from pprint import pprint
import csv
from datetime import datetime

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
    now = datetime.now()

    if fn == None: fn = "jb_scrapy.csv"

    current_path = os.getcwd()
    csv_file = "%s/%s.csv" % (current_path, fn)

    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        fileptr = csv.writer(open(csv_file, "a"))
    else:
        fileptr = csv.writer(open(csv_file, "a"))
        fileptr.writerow(['job', 'company', 'salary', 'url', 'date_when_scrape'])


    soup = BeautifulSoup(urlopen(URL).read(), 'html.parser')
    target_elements = soup.findAll('div', attrs={'data-tn-component': 'organicJob'})

    for ele in target_elements:
        company = ele.find('span', attrs={"itemprop":"name"})
        if company != None:
           company = company.text.strip()
        else: company = ""

        job = ele.find('a', attrs={'data-tn-element': "jobTitle"})
        if job != None:
           job = job.text.strip()
        else: job = ""

        href = ele.find('a', attrs={'class':'turnstileLink'})['href']
        if href != None:
           job_link = "%s%s" % (home_url, href)
        else: job_link = ""

        salary = ele.find('nobr')
        if salary != None:
           salary = salary.text.strip()
        else: salary = ""

        # write to csv
        fileptr.writerow([job, company, salary, job_link, str(now)])





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
        jobs = sys.argv[1]

    print(jobs)
    location = "melbourne"
    home_url = "https://au.indeed.com"
    page_number = "&start="

    pg_num = [0, 10, 20, 30, 40, 50]
    for p in pg_num:
        URL = "%s/jobs?q=%s&l=%s" % (home_url, jobs, location)
        if p == 0:
            page_number = ""
        else:
            page_number = "&start=%i" % p

        URL = URL + page_number
        print("Page %i" % p)

        # lets start scrapping
        scrapper(url=URL,
                 fn = jobs)
