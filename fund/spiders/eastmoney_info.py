# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy_redis.spiders import RedisSpider

from fund.items import EastmoneyFundItem


class EastmoneyInfoSpider(RedisSpider):
    name = "eastmoney_info"
    allowed_domains = ["eastmoney.com"]
    redis_key = f"{name}:start_urls"

    def make_request_from_data(self, data):
        data = eval(data)
        code = data.get("code")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.61",
            "Accept": "*/*",
            "Referer": f"http://fundf10.eastmoney.com/jjjz_{code}.html",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5",
        }
        params = {
            "fundCode": code,
            "pageIndex": "1",
            "pageSize": "20",
            "startDate": "",
            "endDate": "",
        }
        fund_info_url = "http://api.fund.eastmoney.com/f10/lsjz?" + parse.urlencode(params)
        return scrapy.Request(
            url=fund_info_url,
            dont_filter=True,
            meta={"code": code},
            callback=self.parse,
            headers=headers
        )

    def parse(self, response):
        data = response.json()
        total_count = data.get("TotalCount")
        page_size = data.get("PageSize")
        code = response.meta.get("code")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.61",
            "Accept": "*/*",
            "Referer": f"http://fundf10.eastmoney.com/jjjz_{code}.html",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5",
        }
        params = {
            "fundCode": code,
            "pageIndex": "1",
            "pageSize": "20",
            "startDate": "",
            "endDate": "",
        }
        if data.get("ErrCode") != 0:
            params["pageSize"] = str(total_count)
        if total_count and total_count != page_size:
            fund_info_url = "http://api.fund.eastmoney.com/f10/lsjz?" + parse.urlencode(params)
            yield scrapy.Request(
                url=fund_info_url,
                dont_filter=True,
                meta={"code": code},
                callback=self.parse,
                headers=headers,
                priority=100,
            )
        else:
            net_worth = data.get("Data", {}).get("LSJZList", [])
            yield EastmoneyFundItem(code=code, net_worth=net_worth)
