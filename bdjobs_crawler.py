import requests
import time
import sys
import re
from bs4 import BeautifulSoup

lang_dt = {'php' : 0, 'python': 0, 'c++': 0, 'c#': 0, 'java': 0, 'ruby': 0, 'asp': 0, 'perl': 0}


def get_content(url, pdata=None):
    if pdata:
        r = requests.post(url, data = pdata)
    else:
        r = requests.get(url)
        
    content = r.text.encode('utf-8', 'ignore')
    content = content.replace("\r", "")
    content = content.replace("\n", "")
    
    return content.lower()
    

def parse_job_description(url):
    print "Parsing job description for", url
    content = get_content(url)
    time.sleep(1)
    soup = BeautifulSoup(content)
    text = soup.find("div", attrs={"class":"job_detail_left_wrapper"}).text
    for lang in lang_dt.keys():
        pattern_lang = re.compile(r'\W({})\W'.format(re.escape(lang)))
        result = re.findall(pattern_lang, text)
        #print lang, result      
        if len(result) > 0:
            lang_dt[lang] += 1
            
                        
def process_job_urls(content):
    soup = BeautifulSoup(content)
    job_list = soup.find_all("div", attrs={"class":"job_title_text"})
    for item in job_list:
        job_url = 'http://joblist.bdjobs.com/' + item.find('a')['href']
        parse_job_description(job_url)
    return content
    
    
def visit_next_page(content):
    print "visiting next page"
    pattern = re.compile(r'<li><a href="javascript:GoPage\((\d+)\)" class="prevnext">Next', re.IGNORECASE)
    result = re.findall(pattern, content)
    print result
    if len(result) == 0:
        print "next page not found"
        return None
        
    post_data = {} # you have to find the post data
    
    url = 'http://joblist.bdjobs.com/JobSearch.asp'
    content = get_content(url, post_data)
    
    return content
    
   
def main(url):
    content = get_content(url)
    
    while True:
        process_job_urls(content)
        content = visit_next_page(content)
        if content is None:
            print "Site Crawling Complete"
            break
        time.sleep(1)
        print lang_dt
        
          
if __name__ == "__main__":
    print "Program started"
    url = 'http://joblist.bdjobs.com/' 
    main(url)
    for item in lang_dt:
        print item, lang_dt[item]
