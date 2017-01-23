#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "altamob"
__mtime__ = "2016/9/1"
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
┏┓ ┏┓
┏┛┻━━━┛┻┓
┃ ☃ ┃
┃ ┳┛ ┗┳ ┃
┃ ┻ ┃
┗━┓ ┏━┛
┃ ┗━━━┓
┃ 神兽保佑 ┣┓
┃　永无BUG！ ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫ ┃┫┫
┗┻┛ ┗┻┛
"""
import json
import logging
import os
import sys
import re
import time
import requests
from scrapy import Spider, Selector, Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from taobao_spider.items import *

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
chromedriver = "C:\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
user_name = "139...."


class TaoBaoSpider(Spider):
    logger = logging.getLogger()
    """爬取w3school标签"""
    # log.start("log",loglevel='INFO')
    name = "taobao_spider"
    allowed_domains = ["list.tmall.com", "baidu.com"]
    start_urls = [
        "http://list.tmall.com/search_product.htm?spm=a3204.7933263.0.0.V25MRU&cat=50514008&user_id=725677994&at_topsearch=1&search_condition=1&q="
    ]

    category_driver = webdriver.Chrome(chromedriver)
    product_driver = webdriver.Chrome(chromedriver)

    def get_cookies(self):
        with open('cookies.txt') as data_file:
            cookies = json.load(data_file)
        return cookies

    def login_tb(self, driver):
        driver.switch_to.frame('J_loginIframe')
        driver.find_element_by_css_selector('#J_QRCodeLogin > div.login-links >a').click()
        driver.find_element_by_id('TPL_username_1').send_keys(user_name)
        driver.find_element_by_id('TPL_password_1').send_keys("xxxxx")
        driver.find_element_by_id('J_SubmitStatic').click()
        for i in range(15):
            if "login.tmall.com" not in driver.current_url:
                break
            time.sleep(3)

    def parse(self, response):
        url = "http://list.tmall.com/search_product.htm?spm=a3204.7933263.0.0.V25MRU&cat=50514008&user_id=725677994&at_topsearch=1&search_condition=1&q="
        host = "https://list.tmall.com/search_product.htm"
        self.logger.info(response.url)
        driver = self.category_driver
        driver.get(self.start_urls[0])
        driver.delete_all_cookies()
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie['domain'] in driver.current_url.split('?')[0]:
                driver.add_cookie(cookie)
        driver.get(url)
        if "login.tmall.com" in driver.current_url:
            self.login_tb(driver)
        page_source = driver.page_source
        sel = Selector(text=page_source)
        sites = sel.xpath('//*[@id="content"]/div[@class="side"]/div[@class="category"]/div/ul/li')
        for site in sites:
            try:
                item = TaobaoCategoryItem()
                category_id = site.xpath("@data-param").extract()[0].split("=")[-1]
                category_name = site.xpath("a/text()").extract()[0].strip("\n").strip().encode('utf-8')
                category_url = site.xpath("a/@href").extract()[0]
                item['category_id'] = category_id
                item['parent_id'] = ""
                item['category_name'] = category_name
                item['category_url'] = host + category_url
                yield item
            except Exception, e:
                self.logger.exception(e)
                self.logger.warn("出现错误...")

            sub_url = "https://list.tmall.com/ajax/getSubCatsOfChaoshi.htm?user_id=725677994&cat={0}"
            response2 = requests.get(sub_url.format(category_id))
            sel2 = Selector(text=response2._content.decode(response2.encoding))
            sub_sites = sel2.xpath('//ul/li')
            for sub_site in sub_sites:
                try:
                    item2 = TaobaoCategoryItem()
                    item2['category_id'] = sub_site.xpath("@data-param").extract()[0].split("=")[-1]
                    item2['category_name'] = sub_site.xpath("a/text()").extract()[0].strip("\n").strip().encode('utf-8')
                    item2['category_url'] = host + sub_site.xpath("a/@href").extract()[0]
                    item2['parent_id'] = category_id
                    self.logger.info("开始收集商品信息....:%s" % (item2['category_name']))
                    yield Request("http://www.baidu.com/",
                                  meta={"url": item2['category_url'], "page_limit": 5, "cookies": driver.get_cookies(),
                                        "category_id": item2['category_id']},
                                  callback=self.parse_product, dont_filter=True)
                    yield item2
                except Exception, e:
                    self.logger.exception(e)
                    self.logger.warn("出现错误...")

    def parse_product(self, response):
        page_limit = 2
        page_num = 1
        if "page_limit" in response.meta:
            page_limit = response.meta['page_limit']
        if "page_num" in response.meta:
            page_num = response.meta['page_num']
        url = response.meta['url']
        cookies = response.meta['cookies']
        category_id = response.meta['category_id']
        driver = self.product_driver
        if driver.current_url.split("?")[0] not in url:
            driver.delete_all_cookies()
            driver.get(url)
            for cookie in cookies:
                if cookie['domain'] in driver.current_url.split('?')[0]:
                    driver.add_cookie(cookie)
        driver.get(url)
        while page_num <= page_limit:
            if "login.tmall.com" in driver.current_url:
                self.login_tb(driver)
            for i in range(1, 11):
                step = 500
                js = "var q=document.body.scrollTop=" + str(step * i)
                driver.execute_script(js)
                time.sleep(3)
            sel = Selector(text=driver.page_source)
            sites = sel.xpath('//*[@id="J-listContainer"]/ul/li')
            for site in sites:
                try:
                    product_item = TaobaoProductItem()
                    product_id = site.xpath('@data-itemid').extract()[0]
                    product_name = site.xpath('div/h3/a/text()').extract()[0].strip('\n').strip()
                    product_link = site.xpath('div/h3/a/@href').extract()[0].strip('\n').strip()
                    product_price = site.xpath('div/div/div[@class="item-price"]/span/strong/text()').extract()[0]
                    product_sum = site.xpath('div/div/div[@class="item-sum"]/strong/text()').extract()[0]
                    product_img = site.xpath('div/div/a/img/@src').extract()[0]
                    if not str(product_img).startswith('//'):
                        product_img = site.xpath('div/div/a/img/@data-ks-lazyload').extract()[0]
                    product_item['product_id'] = product_id
                    product_item['category_id'] = category_id
                    product_item['product_name'] = product_name
                    product_item['product_price'] = product_price
                    product_item['product_sum'] = product_sum
                    product_item['product_img'] = product_img
                    product_item['product_link'] = product_link
                    yield product_item
                except Exception, e:
                    self.logger.exception(e)
                    self.logger.warn("出现错误...")
            try:
                nex_button = driver.find_element_by_css_selector(
                    "#content > div.main > div > div.list-bottom").find_element_by_xpath(
                    'div/div/a[@class="page-next"]')
                if nex_button.get_attribute("href"):
                    nex_button.click()
                    page_num += 1
                else:
                    break
            except Exception, e:
                self.logger.exception(e)
                self.logger.warn("出现错误...")
                break




if __name__ == "__main__":
    TaoBaoSpider().get_cookies()
