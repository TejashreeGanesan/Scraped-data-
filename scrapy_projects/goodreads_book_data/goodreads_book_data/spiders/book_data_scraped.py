import scrapy
import pandas as pd

class BookDataScrapedSpider(scrapy.Spider):
    name = "book_data_scraped"
    allowed_domains = ["www.goodreads.com"]
    start_urls = ["https://www.goodreads.com/"]
    book_data = []

    def parse(self, response):
        genres_of_interest = ['biography','romance','self-help','mystery','thriller', 'historical-fiction'
                              'young-adult','science-fiction','fantasy','fiction','horror']
        genre_links = response.xpath("//div[@class='left']/a/@href").extract()
        filtered_link = [link for link in genre_links if any(genre in link for genre in genres_of_interest)]
        for link in filtered_link:
            yield response.follow(link, callback=self.parse_links)

    def parse_links(self,response): 
        genre_with_nl=  response.xpath("//div[@class='genreHeader']/h1/text()").get() 
        Genre = genre_with_nl.strip() if genre_with_nl else None
        new_releases_links = response.xpath("//div[@class = 'coverBigBox clearFloats bigBox'][1]/div/h2/a/@href").extract()
        most_read_links = response.xpath("//div[@class = 'coverBigBox clearFloats bigBox'][2]/div/h2/a/@href").extract()
        for category_link in new_releases_links:
            yield response.follow(category_link, callback=self.parse_category_links, meta={'Category': 'New Releases', 'Genre': Genre})
        for category_link in most_read_links:
            yield response.follow(category_link, callback=self.parse_category_links, meta={'Category': 'Most read recently', 'Genre': Genre})    
    
    def parse_category_links(self,response):
        Category = response.meta['Category']
        Genre = response.meta['Genre']
        book_links = response.xpath("//div[@class='coverWrapper']/a/@href").extract()
        base_link = "https://www.goodreads.com/"
        for book_link in book_links:
            real_link = base_link + book_link
            yield scrapy.Request(real_link, callback=self.parse_book_data, meta={'Category': Category,'Genre': Genre, 'real_link': real_link} )

    def parse_book_data(self,response):
        Category = response.meta['Category']
        Genre = response.meta['Genre']
        real_link = response.meta['real_link']
        book_name = response.xpath("//h1[@class='Text Text__title1']/text()").extract_first()
        Author = response.xpath("//span[@class = 'ContributorLink__name']/text()").extract_first()
        no_of_books_by_author_list = response.xpath("//div[@class='FeaturedPerson__infoPrimary']/span[@class='Text Text__body3 Text__subdued']/text()").extract()
        no_of_books_by_author = no_of_books_by_author_list[0] if no_of_books_by_author_list else None
        followers_of_author_list = response.xpath("//div[@class='FeaturedPerson__infoPrimary']/span/span[@class='u-dot-before']/text()").extract()
        followers_of_author = followers_of_author_list[0] if followers_of_author_list else None
        Rating_stars = response.xpath("//div[@class='RatingStatistics__rating']/text()").extract_first()
        Ratings_count_list =  response.xpath("//div[@class='RatingStatistics__meta']/span[1]/text()").extract()
        Ratings_count = Ratings_count_list[0] if Ratings_count_list else None
        No_of_reviews_list = response.xpath("//div[@class='RatingStatistics__meta']/span/text()").extract()
        No_of_reviews = No_of_reviews_list[3] if No_of_reviews_list else None
        Book_details_list = response.xpath("//div[@class='FeaturedDetails']/p/text()").extract()[0]
        Book_details = Book_details_list[0] if Book_details_list else None
        Published_date_elements = response.xpath("//div[@class='FeaturedDetails']/p/text()").extract()
        Published_date = Published_date_elements[1] if len(Published_date_elements) > 1 else None
        description = response.xpath("//div[@class='DetailsLayoutRightParagraph__widthConstrained']/span[@class='Formatted']/text()").extract()
        item = {
            'Category': Category,
            'Genre': Genre,
            'Book_link': real_link,
            'Book_Name': book_name,
            'Author': Author,
            'Number of books by author': no_of_books_by_author,
            'Number of followes of that author': followers_of_author,
            'Rating stars': Rating_stars,
            'Ratings Count': Ratings_count,
            'Number of Reviews': No_of_reviews,
            'Format': Book_details,
            'Published date': Published_date,
            'Description' : description
        }
        self.book_data.append(item)
        yield item
       
    def closed(self,reason):    
        df = pd.DataFrame(self.book_data)
        df.to_excel('Good_reads_book_data.xlsx', index=False)
        self.logger.info("Excel file created successfully.")

        

       

        
    

        








        