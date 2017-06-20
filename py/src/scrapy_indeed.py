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

    # ?? Is there a better way of doing this
    soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
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




def do_scrapy(url, job_keyword, location='None' ,sorted_by='date' ,page_number=11):

    start_page = "&start="

    # include the job keywords we want to scrap
    base_url = "%s%s" % (url, job_keyword)

    if location != None: base_url += "&l=%s" % location

    base_url += "&sort=%s" % (sorted_by)   # &fromage=last sort by date, priorty new job bosted
    base_url += start_page

    for page in range(1, page_number):   # loop through 10 pages
        page = (page -1) * 10   # indeed display in lots of 10s

        this_url = "%s%d" % (base_url, page)
        print(this_url)

        # lets start scrapping
        scrapper(url = this_url,
                 fn = job_keyword)


""" I like it like this....
How to use:
    python scrapy_indeed.py
    python scrapy_indeed.py "keywords"

"""
if __name__ == '__main__':

    jobs  = "python"
    if (sys.argv[1:]):
        jobs = sys.argv[1]

    location = "melbourne"
    home_url = "https://au.indeed.com/jobs?q="

    do_scrapy(url = home_url,
              job_keyword = jobs,
              location='Melbourne',
              sorted_by='date',
              page_number=11)
