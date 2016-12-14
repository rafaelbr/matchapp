import scrapy
import numpy as np
from urllib.parse import urlparse
from urllib.parse import quote

class AstroThemeSpider(scrapy.Spider):

    name = "AstroTheme"
    dataset = []

    def start_requests(self):
        urls = [
            'http://www.astrotheme.com/celebrities_horoscopes/A.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/B.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/C.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/D.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/E.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/F.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/G.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/H.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/I.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/J.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/K.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/L.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/M.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/N.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/O.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/P.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/Q.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/R.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/S.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/T.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/U.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/V.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/W.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/X.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/Y.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/Z.htm',
            'http://www.astrotheme.com/celebrities_horoscopes/Other.htm',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.css("div.corpsTexte div a::attr(href)").extract()
    def parse(self, response):
        page = response.url.split("/")[-1].split(".")[0]
        filename = 'names-%s.csv' % page
        #with open(filename, 'wb') as f:
            #f.write(response.body)
        #self.log('Saved file %s' % filename)
        for name in response.css("div.corpsTexte div")[5].css("a"):

            name_url = str(name.css("a::attr(href)").extract());
            name_p = name_url.split("/")[-1];
            name_quote = quote(name_p);
            name_url = name_url.replace(name_p, name_quote);
            self.log(name_url);
            request = scrapy.Request(name_url, self.parse_name)
            yield request

        np.savetxt(filename, dataset, delimiter=";")

    def parse_name(self, response):
        person_name = response.css("div.titreFiche a::text").extract()
        birth_date =  response.css("div.corpsTexte div")[2].css("div div")[7].css("table tr")[0].css("td a::text").extract() + response.css("div.corpsTexte div")[2].css("div div")[7].css("table tr")[0].css("td::text")[1].extract()
        sun = response.css("div.corpsTexte div")[2].css("div div")[7].css("table tr")[2].css("td a::text").extract()
        moon = response.css("div.corpsTexte div")[2].css("div div")[7].css("table tr")[3].css("td a::text").extract()
        dominants = response.css("div.corpsTexte div")[2].css("div div")[7].css("table tr")[4].css("td a::text").extract()
        chinese_astro = response.css("div.corpsTexte div")[2].css("div div")[7].css("table tr")[5].css("td::text")[1].extract()
        numerology = response.css("div.corpsTexte div")[2].css("div div")[7].css("table tr")[6].css("td::text").extract()

        dataset = np.concatenate(dataset, [person_name, birth_date, sun, moon, dominants, chinese_astro, numerology])
