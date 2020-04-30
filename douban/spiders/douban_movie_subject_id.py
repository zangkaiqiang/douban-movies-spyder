# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class DoubanMovieSubjectIdSpider(scrapy.Spider):
    name = 'douban_movie_subject_id'
    allowed_domains = ['m.douban.com']
    # start_urls = ['https://m.douban.com/search/?query=我不是药神']
    # url = 'https://m.douban.com/search/?query=我不是药神&type=movie'

    def start_requests(self):
        with open('movies_name.txt') as f:
            movies = f.readlines()
        for movie in movies:
            url = 'https://m.douban.com/search/?query=%s&type=movie'%movie.strip()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.body)
        soup = BeautifulSoup(response.body,'lxml')
        href = soup.findAll('ul',class_='search_results_subjects')[0].findAll('a')[0]['href']
        result_url = 'https://movie.douban.com/subject/%s/'%href.strip().split('/')[-2]

        with open('movies_url.txt','a') as f:
            f.writelines(result_url+'\n')
