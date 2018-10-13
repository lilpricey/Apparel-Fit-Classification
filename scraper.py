from selenium import webdriver
import pandas
import time
import pickle
import csv

class Scraper():
    def __init__(self):
        self.url = "https://needsupply.com/mens/clothing?p='1'"
        self.driver_path = './chromedriver'
        self.driver = webdriver.Chrome(self.driver_path)
        self.product_links = []
        self.write_row = []

    def _get_url(self):
        self.driver.get(self.url)


    def _get_product_urls(self):
        print("Getting product links...")
        self.product_links = self.driver.find_elements_by_class_name('image-link')


    def _get_pictures(self):
        element = self.driver.find_elements_by_class_name('product-thumbs')[0]
        image_tags = element.find_elements_by_tag_name('img')

        image_urls = [tag.get_attribute('src') for tag in image_tags]

        self.write_row.extend(image_urls)

        #for i, tag in enumerate(image_tags):
        #    print(tag.get_attribute('src'))
        #    self.product_object["thumbnail-{}".format(i)] = tag.get_attribute('src')
        #print("Product thumbs: {}".format(element))
        print(image_urls)
        self.write_row.extend(image_urls)
        print('WRITE ROW: {}'.format(self.write_row))

    def _get_sizing_info(self):
        # write sizing info to object
        sizing_element = self.driver.find_elements_by_class_name('sizing')[0]
        unclean_sizing_element = sizing_element.get_attribute('innerHTML')
        unclean_sizing_element = self._clean_inner_html(unclean_sizing_element)
        self.write_row.append(unclean_sizing_element)
        print(unclean_sizing_element)
    
    def _clean_inner_html(self, unclean_sizing_element):
        unclean_sizing_element = unclean_sizing_element.replace('\n', '')
        unclean_sizing_element = unclean_sizing_element.replace('\t', '')
        unclean_sizing_element = unclean_sizing_element.split('<br>')
        unclean_sizing_element = " ".join([i for i in unclean_sizing_element if i is not ''])
        return unclean_sizing_element


    def _write_csv(self, row=None):
        """
        params
        row:[] scraped data for the page
        """
        if not row:
            row = self.write_row
            self.write_row = []

        csv_file = 'data.csv'
        with open(csv_file, mode='a') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(row)
            print('Writing to {}..'.format(csv_file))

    
    def start(self):
        self._get_url()
        self._get_product_urls()

        n_links = len(self.product_links)

        print('Number of Product Links: {}'.format(n_links))

        for i in range(n_links):
            print('Scraping data for link {0}/{1}..'.format(i, n_links))
            self.product_links[i].click()

            self._get_pictures()
            self._get_sizing_info()

            #self._build_dataframe()
            #self._csv_checkpoint()

            self._write_csv()
            self._get_url()
            self._get_product_urls()



if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()
