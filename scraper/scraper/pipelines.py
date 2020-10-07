""" Pipeline for parliament table with data for Rest API"""
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
import sqlite3


class ParliamentPipeline:
    """ Pipeline for parliament table with data for Rest API"""

    def __init__(self):
        self.create_connection()
        # self.create_table()

    def create_connection(self):
        """ connect to DB """
        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, "db.sqlite3")
        self.conn = sqlite3.connect(db)
        self.curr = self.conn.cursor()

    def process_item(self, item):
        """ process_item """
        self.store_db(item)
        return item

    def store_db(self, item):
        """ insert it to database"""
        self.curr.execute(
            """insert into Parliament1 values (NULL,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                item["name"],
                item["date_born"],
                item["place_born"],
                item["profession"],
                item["lang"],
                item["party"],
                item["email"],
                item["fb"],
                item["url"],
                item["pp"],
                item["dob"],
            ),
        )
        self.conn.commit()
