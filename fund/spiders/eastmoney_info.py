# -*- coding: utf-8 -*-
import execjs
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
        fund_info_url = f"http://fund.eastmoney.com/pingzhongdata/{code}.js"
        return scrapy.Request(url=fund_info_url, dont_filter=True, meta={"code": code}, callback=self.parse, )

    def parse(self, response, **kwargs):
        code = response.meta.get("code")
        js_content = execjs.compile(response.text)
        date_map = {
            "source_rate": "fund_sourceRate",
            "rate": "fund_Rate",
            "minimum_purchase_amount": "fund_minsg",
            "stock_codes": "stockCodes",
            "zq_codes": "zqCodes",
            "new_stock_codes": "stockCodesNew",
            "new_zq_codes": "zqCodesNew",
            "annual_income": "syl_1n",
            "half_year_income": "syl_6y",
            "quarterly_revenue": "syl_3y",
            "monthly_income": "syl_1y",
            "position_calculation_chart": "Data_fundSharesPositions",
            "net_worth_trend": "Data_netWorthTrend",
            "cumulative_net_worth_trend": "Data_ACWorthTrend",
            "cumulative_rate_of_return_trend": "Data_grandTotal",
            "rate_in_similar_type": "Data_rateInSimilarType",
            "rate_in_similar_persent": "Data_rateInSimilarPersent",
            "fluctuation_scale": "Data_fluctuationScale",
            "holder_structure": "Data_holderStructure",
            "asset_allocation": "Data_assetAllocation",
            "performance_evaluation": "Data_performanceEvaluation",
            "current_fund_manager": "Data_currentFundManager",
            "buy_sedemption": "Data_buySedemption",
            "swith_same_type": "swithSameType",
            "million_copies_income": "Data_millionCopiesIncome",
            "seven_days_year_income": "Data_sevenDaysYearIncome",
            "asset_allocation_currency": "Data_assetAllocationCurrency",
        }
        item = EastmoneyFundItem(code=code)
        for key, name in date_map.items():
            try:
                item[key] = js_content.eval(name)
            except Exception as e:
                item[key] = None
        yield item
