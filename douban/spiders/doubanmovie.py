# -*- coding: utf-8 -*-
import scrapy
from douban.items import MovieItem
from bs4 import BeautifulSoup

class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['douban.com']

    # start_urls = ['https://movie.douban.com/subject/26752088/',
    #               'https://movie.douban.com/subject/1432972/']

    def start_requests(self):
        with open('douban_movies_urls.txt') as f:
            urls = f.readlines()
        urls = [i.strip() for i in urls]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        info_html = response.xpath('//*[@id="info"]').get()
        soup = BeautifulSoup(info_html,'lxml')

        info = soup.text
        info = info.strip().split('\n')
        info_dict = {}
        for i in info:
            info_sub = i.split(':')
            try:
                info_sub_one = info_sub[0].strip()
                info_sub_two = info_sub[1].strip()
                info_dict[info_sub_one.split('/')[0]] = info_sub_two
            except Exception as e:
                print(i)
                print(e)
                continue

        name = response.xpath('//*[@id="content"]/h1/span[1]/text()').get()
        subjectId = response.url.split('/')[-2]


        movie = MovieItem()
        movie['subjectId'] = subjectId
        movie['name'] = name

        self.safe_add('director','导演',movie,info_dict)
        self.safe_add('screenwriter','编剧',movie,info_dict)


        movie["Starring"] = info_dict["主演"]
        movie["type"] = info_dict["类型"]
        movie["production_region"] = info_dict["制片国家"]
        movie["Language"] = info_dict["语言"]

        movie['release_date'] = ""
        if '上映日期' in info_dict.keys():
            movie["release_date"] = info_dict["上映日期"]

        movie['first_broadcast_date'] = ""
        if '首播' in info_dict.keys():
            movie['first_broadcast_date'] = info_dict['首播']

        movie['episode'] = ""
        if '集数' in info_dict.keys():
            movie['episode'] = info_dict['集数']

        movie["length"] = ""
        if '片长' in info_dict.keys():
            movie["length"] = info_dict["片长"]

        movie["aka"] = info_dict["又名"]

        movie["imdb_link"] = ''
        if 'IMDb链接' in info_dict.keys():
            movie["imdb_link"] = info_dict["IMDb链接"]


        score = response.xpath('//*[@id="interest_sectl"]').get()
        soup_score = BeautifulSoup(score,'lxml')

        rating_per = soup_score.findAll('span',class_='rating_per')
        rating_per = [i.text for i in rating_per]
        douban_score = soup_score.findAll('strong', class_='ll',attrs={'property':'v:average'})[0].text
        rating_numbers = soup_score.findAll('a',class_='rating_people')[0].findAll('span', attrs={'property':'v:votes'})[0].text
        movie['douban_score'] = douban_score
        movie['rating_numbers'] = rating_numbers
        movie['star5'] = rating_per[0]
        movie['star4'] = rating_per[1]
        movie['star3'] = rating_per[2]
        movie['star2'] = rating_per[3]
        movie['star1'] = rating_per[4]

        return movie

    def safe_add(self,s1, s2, items, info_dict):
        items[s1] = ""
        if s2 in info_dict.keys():
            items[s1] = info_dict[s2]