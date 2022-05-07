import scrapy
import time
from ..items import TripadvisorItem

from selenium import webdriver
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings

class AttractionSpider(scrapy.Spider):
    name = 'attraction'
    allowed_domains = ['tripadvisor.com.sg']
    start_urls = [
        'https://www.tripadvisor.com.sg/Attraction_Review-g294264-d2439664-Reviews-Universal_Studios_Singapore-Sentosa_Island.html',
        #'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d2149128-Reviews-Gardens_by_the_Bay-Singapore.html',
        #'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d310900-Reviews-Singapore_Botanic_Gardens-Singapore.html',
        #'https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html'    
    ]

    def parse(self, response):
        
        # Setup selenium configs
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-popup-blocking')
        options.add_argument('--log-level=1')
        driver = webdriver.Chrome(driver_path, options = options)
        driver.get(response.url)
        docId = 1
        time.sleep(3)
        
        # Loop until there is no more next
        while True:
            a_docId = docId
            a_url = driver.current_url
            a_reviewer_name = 'NA'
            a_reviewer_location = 'NA'
            a_reviewer_contribution = 'NA'
            a_comment_upvotes = 'NA'
            a_comment_date = 'NA'
            a_rating = 'NA'
            a_title_comment = 'NA'
            a_content_comment = 'NA'
            num_comments_items = 0
            comments = None
            
            # Find if there are any reviews available
            try:
                comments = driver.find_elements_by_xpath('//div[@data-automation="reviewCard"]')
                num_comments_items = len(comments)
            except:
                item = TripadvisorItem()
                item['a_docId'] = a_docId
                item['a_url'] = a_url
                item['a_reviewer_name'] = a_reviewer_name
                item['a_reviewer_location'] = a_reviewer_location
                item['a_reviewer_contribution'] = a_reviewer_contribution
                item['a_comment_upvotes'] = a_comment_upvotes
                item['a_comment_date'] = a_comment_date
                item['a_rating'] = a_rating
                item['a_title_comment'] = a_title_comment
                item['a_content_comment'] = a_content_comment
                
                a_docId += 1
                yield item
        
            # Searches through all the possible paths to find the correct thing to parse (all the div / spans are manually found on website)
            for j in range(num_comments_items):
                try:
                    a_reviewer_name = comments[j].find_element_by_xpath('.//div[@class="cjhIj"]').find_element_by_xpath('.//a[@target="_self"]').text
                except:
                    a_reviewer_name = 'Failed'  
                      
                try:
                    profile_items = comments[j].find_element_by_xpath('.//div[@class="cjhIj"]//div[@class="ddOtn"]//div[@class="WlYyy diXIH bQCoY"]')
                    profile_item = [profile_text.text for profile_text in profile_items.find_elements_by_css_selector('span')]
                    
                    if len(profile_item) == 1:
                        a_reviewer_contribution = profile_item[0]
                        a_reviewer_location = 'Failed'
                    elif len(profile_item) == 2:
                        a_reviewer_location = profile_item[0]
                        a_reviewer_contribution = profile_item[1]
                    else:
                        raise Exception()
                except:
                    a_reviewer_location = 'Failed'   
                    a_reviewer_contribution = 'Failed'
                    
                try:
                    a_comment_upvotes = comments[j].find_element_by_xpath('.//button[@class="dfuux u j z _F ddFHE bLQvU dQDUG"]//span[@class="eKtLG"]//span[@class="WlYyy bTDWl"]').text
                except:
                    a_comment_upvotes = 'Failed'
                    
                try:
                    dates = comments[j].find_element_by_xpath('.//div[@class="eRduX"]').text
                    date = [comment_date.strip() for comment_date in dates.split(" ")]
                    a_comment_date = date[0] + " " + date[1]
                except:
                    a_comment_date = 'Failed'
                    
                try:
                    a_rating = comments[j].find_element_by_xpath('.//*[local-name()=\'svg\' and @class="RWYkj d H0"]').get_attribute('title')
                except:
                    a_rating = 'Failed'
                    
                try:
                    a_title_comment = comments[j].find_element_by_xpath('.//a[@target="_blank"]').find_element_by_xpath('.//span[@class="NejBf"]').text
                except:
                    a_title_comment = 'Failed'
                    
                try:
                    a_content_comment = comments[j].find_element_by_xpath('.//div[@class="duhwe _T bOlcm"]//div[@class="pIRBV _T KRIav"]//div[@class="WlYyy diXIH dDKKM"]').find_element_by_xpath('.//span[@class="NejBf"]').text
                    
                except:
                    try:
                        comment_text = comments[j].find_element_by_xpath('.//div[@class="duhwe _T bOlcm dMbup"]//div[@class="pIRBV _T KRIav"]//div[@class="WlYyy diXIH dDKKM"]').find_element_by_xpath('.//span[@class="NejBf"]').get_attribute("innerHTML")
                        split_text = [comment.strip() for comment in comment_text.split("<br>")]
                        a_content_comment = " ".join(split_text)
                    except:
                        a_content_comment = 'Failed'
                    
                item = TripadvisorItem()
                item['a_docId'] = a_docId
                item['a_url'] = a_url
                item['a_reviewer_name'] = a_reviewer_name
                item['a_reviewer_location'] = a_reviewer_location
                item['a_reviewer_contribution'] = a_reviewer_contribution
                item['a_comment_upvotes'] = a_comment_upvotes
                item['a_comment_date'] = a_comment_date
                item['a_rating'] = a_rating
                item['a_title_comment'] = a_title_comment
                item['a_content_comment'] = a_content_comment
                
                a_docId += 1
                yield item
            
            # Parse the page to find the things
            try:
                driver.find_element_by_xpath('//a[@data-smoke-attr="pagination-next-arrow"]').click()
                
                time.sleep(3)
            except:
                break
        
        driver.quit()
        pass
