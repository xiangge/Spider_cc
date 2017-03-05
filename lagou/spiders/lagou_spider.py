# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem
#from scrapy_redis.spiders import RedisSpider


class LagoupositonSpider(scrapy.Spider):
    name = "LagouSpider"
    #allowed_domains = ["lagou.com/zhaopin/"]
    start_urls = ('http://www.lagou.com/zhaopin/')
    totalPageCount = 0
    curpage = 1
    curkd = 1 #当前关键字
    position_url = 'http://www.lagou.com/jobs/positionAjax.json?'
    #http://www.lagou.com/jobs/positionAjax.json?pn=1

    #city = u'北京'
    #kds = [u'java','python','PHP','.NET','JavaScript','C#','C++','C','VB','Dephi','Perl','Ruby','Go','ASP','Shell']
    #kds = [u'大数据',u'云计算',u'docker',u'中间件','Node.js',u'数据挖掘',u'自然语言处理',u'搜索算法',u'精准推荐',u'全栈工程师',u'图像处理',u'机器学习',u'语音识别']
    #kds = ['HTML5','Android','iOS',u'web前端','Flash','U3D','COCOS2D-X']
    #kds = [u'spark','MySQL','SQLServer','Oracle','DB2','MongoDB' 'ETL','Hive',u'数据仓库','Hadoop']
    #kds = [u'大数据',u'云计算',u'docker',u'中间件']
    #kd = kds[0]

    def start_requests(self):
        # for self.kd in self.kds:
        #
        #     scrapy.http.FormRequest(self.position_url,
        #                                 formdata={'pn':str(self.curpage),'kd':self.kd},callback=self.parse)
        #     也可以是city
        #查询特定关键词的内容，通过request
        # return [scrapy.http.FormRequest(self.position_url,
        #                                 formdata={'pn': str(self.curpage)}, #第一页
        #                                 callback=self.parse)]
        yield scrapy.Request(self.position_url+"pn=%d"%self.curpage, dont_filter=True, callback=self.parse)

    def parse(self, response):
        #print response.body
        print("===============%s"%response.body)
        item = LagouItem()
        jdict = json.loads(response.body)
        jcontent = jdict["content"]
        jposresult = jcontent["positionResult"]
        jresult = 5000 #jposresult["result"]
        #print(jposresult['totalCount'])  #最新数据# 231405, # 这是爬虫蜜罐，基本是无效的重复数据，直接设置为5000吧
        
        self.totalPageCount = jposresult['totalCount'] / 15 + 1 #/15正常，/150用于测试
        print(self.totalPageCount)
        for each in jresult:
            item['city'] = each['city']
            item['positionId'] = each['positionId']
            item['companyLogo'] = each['companyLogo']
            item['workYear'] = each['workYear']
            item['education'] = each['education']
            item['jobNature'] = each['jobNature']
            item['financeStage'] = each['financeStage']
            item['district'] = each['district']
            item['deliver'] = each['deliver']
            item['createTime'] = each['createTime']
            item['industryField'] = each['industryField']
            #item['showCount'] = each['showCount']
            item['pcShow'] = each['pcShow']
            item['appShow'] = each['appShow']
            item['score'] = each['score']
            item['companyShortName'] = each['companyShortName']
            item['companySize'] = each['companySize']
            item['positionName'] = each['positionName']
            #item['positionType'] = each['positionType']
            salary = each['salary']
            salary = salary.split('-')
            #把工资字符串（ak-bk）转成最大和最小值(a,b)
            #todo:写成单独函数：util
            if len(salary) == 1:
                item['salaryMax'] = int(salary[0][:salary[0].find('k')])
            else:
                item['salaryMax'] = int(salary[1][:salary[1].find('k')])
            item['salaryMin'] = int(salary[0][:salary[0].find('k')])
            item['salaryAvg'] = (item['salaryMin'] + item['salaryMax']) / 2
            item['positionAdvantage'] = each['positionAdvantage']
            item['companyLabelList'] = each['companyLabelList']
            # item['keyword'] = self.kd
            yield item
        if self.curpage <= self.totalPageCount:
            self.curpage += 1 #继续爬下一页
            #if self.curpage == 335:
            #    self.curpage = 5000
            print(u"当前页{}".format(self.curpage))
            yield scrapy.http.FormRequest(
                self.position_url,
                # formdata = {'pn': str(self.curpage), 'kd': self.kd},callback=self.parse)
                formdata={'pn': str(self.curpage)}, #pn 从335到5000 是空的
                callback=self.parse)
        # 爬多个关键字
        '''
        elif self.curkd < len(self.kds):
            self.curpage = 1
            self.totalPageCount = 0
            self.curkd += 1  #当前关键字，名字不好
            self.kd = self.kds[self.curkd]
            yield scrapy.http.FormRequest(self.position_url,
                                        formdata = {'pn': str(self.curpage), 'kd': self.kd},callback=self.parse)
        '''
