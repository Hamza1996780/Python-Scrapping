from requests_html import HTMLSession
import bs4
from bs4 import BeautifulSoup
import pandas as pd

l=[]
l1=[]
l2=[]
l3=[]
coun=0
def getdata(url):
    r=s.get(url)
    r.html.render(sleep=8)
    soup=BeautifulSoup(r.html.html,"html.parser")
    return soup

def getnextpage(soup):
    page=soup.find("span",{"class": "s-pagination-strip"})
    if page.find('span',{ 'class':'s-pagination-item s-pagination-next s-pagination-disabled'}) is None:
        url='https://www.amazon.com'+ str(page.find('a',{'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
        return url
    else:
        return

def datatofile(soup):
    global coun
    global l,l1,l2,l3
    y=soup.find("div", class_="s-main-slot s-result-list s-search-results sg-row")
    x=y.find_all("div", class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small gsx-ies-anchor sg-col-12-of-16")
    for item in x:
        if type(item) is not bs4.element.NavigableString:
            if item is not None:
                z=item.find("div", class_="puisg-row")
                j=z.find("img", class_="s-image s-image-optimized-rendering")['src']
                if j is not None:
                    l.append(j)   
                d1=z.find("div", class_="puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right")
                d2=d1.find("div", class_="a-section a-spacing-none puis-padding-right-small s-title-instructions-style")
                d3=d2.find("h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2").find("span", class_="a-size-medium a-color-base a-text-normal").text
                if d3 is not None:
                    l1.append(d3)
                d4=z.find("div",class_="a-section a-spacing-none a-spacing-top-micro")
                if d4 is not None:
                    d5=d4.find("div",class_="a-row a-size-small")
                    if d5 is not None:
                        d6=d5.find("span").text
                        l2.append(d6)
                    else:
                        l2.append("No Value Found")
                else:
                    l2.append("No Value Found")
                d7=z.find("div", class_="s-csa-instrumentation-wrapper alf-search-csa-instrumentation-wrapper")
                if d7 is not None:
                    d8=d7.find("span", class_="a-size-base s-underline-text")
                    if d8 is not None:
                        l3.append(d8.text)
                    else:
                        l3.append("Value not found")
                else:
                    l3.append("value not found")
                coun = coun+1;

url="https://www.amazon.com/s?k=iphone&crid=229MCQY8ERZUT&qid=1718056028&sprefix=iph%2Caps%2C432&ref=sr_pg_1"
s=HTMLSession()
while True:
    soup=getdata(url)
    url=getnextpage(soup)
    datatofile(soup)
    if url is None:
       break
Dta=pd.DataFrame(list(zip(l,l1,l2,l3)))
Dta.columns=['Image','Description','Rating','Total Reviews']
print(Dta)
Dta.to_csv('Data.csv')