from bs4 import BeautifulSoup

def make_soup(source):
    soup = BeautifulSoup(source,'html.parser')
    return soup
