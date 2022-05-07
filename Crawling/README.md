# Crawling
Requirements:
1. Selenium
2. Scrapy

If you are using a MAC, please change the chromedriver currently given to a MAC installation, if not this program will not work

How to run the crawler:
1. Open a cmd prompt
2. cd ..\TripAdvisor\TripAdvisor
3. enter 'scrapy crawl attraction -o output.csv' (this will output the results into a csv)

# Insert / Word count
The 2 Java files are meant to be used with solrj and maven
SolrjInsert - Inserts data into solr through a json file
WordCounter - Counts the unique words and total words in solr