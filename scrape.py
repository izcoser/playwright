import json

# Pegar todos notebooks Lenovo ordenando do mais barato para o mais caro. Pegar todos os dados disponíveis dos produtos.
url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
domain = 'https://webscraper.io'

from playwright.sync_api import sync_playwright

results = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page_main = browser.new_page()
    page_item = browser.new_page()
    page_main.goto(url)
    for element in page_main.query_selector_all('.thumbnail'):
        # Data from main page.
        img_src = element.query_selector('img').get_attribute('src')
        caption = element.query_selector('.caption')
        item_link = caption.query_selector('a').get_attribute('href')
        title = caption.query_selector('a').get_attribute('title')
        
        if 'Lenovo' not in title:
            continue
        
        desc = caption.query_selector('.description').inner_text()
        ratings_element = element.query_selector('.ratings')
        reviews = ratings_element.query_selector('.pull-right').inner_text().split()[0]
        rating = ratings_element.query_selector('[data-rating]').get_attribute('data-rating')
        prices = []
        hdd_availability = []

        # Data from item's page.
        page_item.goto(domain + item_link)
        info_element = page_item.query_selector('.col-lg-10')
        caption_inner = info_element.query_selector('.caption')
        price = caption_inner.query_selector('.price')
        swatches = info_element.query_selector('.swatches')
        for s in swatches.query_selector_all('button'):
            s.click()
            prices.append(price.inner_text())
            if not ('disabled' in s.get_attribute('class')):
                hdd_availability.append(s.inner_text())

        data = {
            'image': img_src,
            'prices': prices,
            'hdd_availability': hdd_availability,
            'item_link': item_link,
            'title': title,
            'description': desc,
            'reviews': reviews,
            'rating': rating,
        }

        results.append(data)
    browser.close()

sorted_results = sorted(results, key=lambda d: float(d['prices'][0].replace('$', '')))

if len(results) > 0:
    with open('lenovo_computers.json', 'w') as f:
        f.write(json.dumps(results, indent=4))