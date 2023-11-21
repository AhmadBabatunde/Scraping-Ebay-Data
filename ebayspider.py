import scrapy


class EbayspiderSpider(scrapy.Spider):
    name = "ebayspider"
    allowed_domains = ["www.ebay.com"]
    page_count = 0  # Counter to keep track of pages crawled
    def start_requests(self):
        # Replace 'your_search_query' with the actual query you want to search for on eBay
        search_query = 'iphone'
        sort_parameter = 'Top_rated_seller'
        ebay_search_url = f'https://www.ebay.com/sch/i.html?_nkw={search_query}&_sop={sort_parameter}'

        yield scrapy.Request(url=ebay_search_url, callback=self.parse_search_result)


    def parse_search_result(self, response):
        iphones = response.css('li.s-item')
        for iphone in iphones:
            iphone_url = iphone.css('a.s-item__link ::attr(href)').get()
            
            yield response.follow(iphone_url, callback=self.parse_iphone_page)
            
        self.page_count += 1  # Increment the page count
        if self.page_count < 50:  # Limit to 50 pages    
            next_page_url = response.css('a.pagination__next.icon-link ::attr(href)').get()
            if next_page_url is not None:
                next_page = next_page_url
                yield response.follow(next_page, callback= self.parse)
            
            
    def parse_iphone_page(self, response):
        feedback_data = []
        item_spec = response.css('div.ux-layout-section-evo__col')
        feedback = response.css('a.fdbk-detail-list__tabbed-btn ::attr(href)').get()
        if feedback:
            feedback_url = response.urljoin(feedback)
            yield scrapy.Request(feedback_url, callback=self.parse_feedback, meta={'feedback_data': feedback_data})    
            
        
        yield {
            'url' : response.url,
            'product_title' : response.css('h1.x-item-title__mainTitle span::text').get(),
            'product_price' : response.css('div.x-price-primary  span::text').get(),
            'Condition' : item_spec[0].css('div.ux-labels-values__values-content span::text').get(),
            'Processor' : item_spec[1].css('div.ux-labels-values__values-content span::text').get(),
            'Screen Size' : item_spec[2].css('div.ux-labels-values__values-content span::text').get(),
            'Chipset Model' : item_spec[3].css('div.ux-labels-values__values-content span::text').get(),
            'Lock Status' :item_spec[4].css('div.ux-labels-values__values-content span::text').get(),
            'SIM Card Slot' : item_spec[5].css('div.ux-labels-values__values-content span::text').get(),
            'Brand' : item_spec[6].css('div.ux-labels-values__values-content span::text').get(),
            'Manufacturer Warranty' : item_spec[7].css('div.ux-labels-values__values-content span::text').get(),
            'Network' : item_spec[8].css('div.ux-labels-values__values-content span::text').get(),
            'Model' : item_spec[9].css('div.ux-labels-values__values-content span::text').get(),
            'Connectivity' : item_spec[10].css('div.ux-labels-values__values-content span::text').get(),
            'Style' : item_spec[11].css('div.ux-labels-values__values-content span::text').get(),
            'Operating System' : item_spec[12].css('div.ux-labels-values__values-content span::text').get(),
            'Features' : item_spec[13].css('div.ux-labels-values__values-content span::text').get(),
            'Storage Capacity' : item_spec[14].css('div.ux-labels-values__values-content span::text').get(),
            'Contract' : item_spec[15].css('div.ux-labels-values__values-content span::text').get(),
            'Camera Resolution': item_spec[16].css('div.ux-labels-values__values-content span::text').get(),
            'RAM' : item_spec[17].css('div.ux-labels-values__values-content span::text').get(),
            'feedback' : feedback_data
        }


    def parse_feedback(self, response):
        feedback_data = response.meta['feedback_data']
        feedback_list = response.css('div.card__feedback span::text').getall()
        for value in feedback_list:
            feedback_data.append(value)

        yield {
            'url': response.url,
            'feedback': feedback_data
        }
