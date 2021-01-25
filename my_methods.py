from requests_html import HTMLSession
import pandas as pd

def get_spec_dict(spec_list):
    spec_dict = {}
    for row in spec_list:
        
        row = row.split('\n')
        key = row[0]
        try:
            val = str(row[1])
        except:
            val = None
        spec_dict[key] = val

    return spec_dict

def get_xpath_list():

    xpath_base = r'//*[@id="product-specification-table"]/tbody/tr[1]'
    xpath_first_half = r'//*[@id="product-specification-table"]/tbody/tr['
    xpath_second_half = r']'

    xpath_list = []
    for i in range(1,20):
        xpath = xpath_first_half + str(i) + xpath_second_half
        xpath_list.append(xpath)
        
    return xpath_list

def getPrice(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    #get product_dict
    product = {}
    product['title'] = r.html.xpath('//*[@id="productTitle"]', first=True).text
    product['price'] = r.html.xpath('//*[@id="priceblock_ourprice"]', first=True).text
    try:
        product['shipping'] = r.html.xpath('//*[@id="price-shipping-message"]/b', first=True).text
    except:
        product['shipping'] = 'unable to get shipping info'
    # get spec_list
    spec_list = []
    xpath_list = get_xpath_list()
    for xpath_item in xpath_list:
        try:
            data = r.html.xpath(xpath_item, first=True).text
            spec_list.append(data)
        except:
            break
    spec_dict = get_spec_dict(spec_list)    
    
    product.update(spec_dict)
    
    return product

def get_product_spec(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    spec_list = []
    xpath_list = get_xpath_list()
    for xpath_item in xpath_list:
        try:
            data = r.html.xpath(xpath_item, first=True).text
            spec_list.append(data)
        except:
            break
    # product['row_1'] = r.html.xpath('//*[@id="product-specification-table"]/tbody/tr[1]', first=True).text

    spec_dict = get_spec_dict(spec_list)
    
    return spec_dict

# define fn that gets number of pages

# define fn that gets all search url pages from dept url
def get_search_urls(dept_url, num_pages = 155):

    url_list = []
    for i in range(1,num_pages):
        url = dept_url + str(i)
        url_list.append(url)
        
    return url_list

# define fn that gets all product_urls from a search_url
def get_prod_ulrs(search_url):

    s = HTMLSession()
    r = s.get(search_url)
    r.html.render(sleep=1)

    xpath = r'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div'

    deeper_xpath = r'//*[@id="search"]/div[1]/div[2]/div/span[3]/div/div/div/span/div/div/div/div/span/a'
    results_page = r.html.xpath(deeper_xpath)

    prod_url_list = []
    for node in results_page:
        
        url_end = node.attrs['href']
        url_base = r'https://www.amazon.com'
        prod_url = url_base + url_end
        prod_url_list.append(prod_url)


    return prod_url_list

# define fn that gets all dept urls from all search