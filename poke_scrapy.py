import scrapy
from scrapy import Request
import csv

class PokedexSpider(scrapy.Spider):
    name = 'pokedex_spider'
    start_urls = [
        'https://pokemondb.net/pokedex/national'
    ]
    csv_rows = []

    def parse(self, response, **kwargs):
        info_cards = response.xpath(
            '//span [has-class("infocard-lg-data")]'
        )

        for info_card in info_cards:
            yield Request(
                f"https://pokemondb.net"
                f"{info_card.xpath('a/@href').get()}",
                callback=self.parse_detail_page
            )

    def parse_detail_page(self, response, **kwargs):
        name = response.xpath('//h1/text()').get()
        infos = response.xpath('//table')[0]
        number = infos.xpath(
            'tbody/tr/td/strong/text()'
        ).get()
        type_1 = infos.xpath(
            'tbody/tr[2]/td/a/text()'
        ).get()
        type_2 = infos.xpath(
            'tbody/tr[2]/td/a[2]/text()'
        ).get()

        base_stats = response.xpath(
            '//table'
        )[3]

        hp = base_stats.xpath(
            'tbody/tr/td/text()'
        ).get()
        attack = base_stats.xpath(
            'tbody/tr[2]/td/text()'
        ).get()
        defense = base_stats.xpath(
            'tbody/tr[3]/td/text()'
        ).get()
        sp_attack = base_stats.xpath(
            'tbody/tr[4]/td/text()'
        ).get()
        sp_def = base_stats.xpath(
            'tbody/tr[5]/td/text()'
        ).get()
        speed = base_stats.xpath(
            'tbody/tr[6]/td/text()'
        ).get()
        total = base_stats.xpath(
            'tfoot/tr/td/b/text()'
        ).get()

        self.csv_rows.append([
            name,
            number,
            type_1,
            type_2 if type_2 else '',
            hp,
            attack,
            defense,
            sp_attack,
            sp_def,
            speed,
            total
        ])

    def closed(self, reason):
        f = open('pokedex.csv', 'w')
        writer = csv.writer(f)
        writer.writerow([
            'Name', 'Number', 'Type 1', 'Type 2', 'HP', 'Attack', 'Defense', 'SP Attack', 'SP Defense', 'Speed', 'Total'
        ])

        writer.writerows(self.csv_rows)
