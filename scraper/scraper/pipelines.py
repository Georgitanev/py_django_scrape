# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3


class ParliamentPipeline:

    def __init__(self):
        self.create_connection()
        # self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("D:\\git\\24_09_2019_download_repos\\py\\MyApi\\db.sqlite3")
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into Parliament1 values (NULL,?,?,?,?,?,?,?,?,?,?,?)""", (
            item['name'],
            item['date_born'],
            item['place_born'],
            item['profession'],
            item['lang'],
            item['party'],
            item['email'],
            item['fb'],
            item['url'],
            item['pp'],
            item['dob']

        ))
        self.conn.commit()

