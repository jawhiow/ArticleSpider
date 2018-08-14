# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item["front_image_path"] = image_file_path
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_close(self, spider):
        self.file.close()


class JsonExporterPipeLine(object):
    # 调用scrapy提供的json export 导出json文件
    def __init__(self):
        self.file = open('article_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeLine(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'scrapy')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = "insert into jobble_article(title, url, create_date, fav_nums, url_object_id)values (%s, %s, %s, %s)"
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums'], item['url_object_id']))
        self.conn.commit()


