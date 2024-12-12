import os
import requests
from datetime import datetime
from app.db.dao import PostsDao
from app.util import sign_util, crawl_util
from zoneinfo import ZoneInfo

class NewsCrawler:

    def __init__(self):
        self.api_key1 = os.getenv("GNEWS_API_KEY1")
        self.api_key2 = os.getenv("GNEWS_API_KEY2")

    def general(self):
        self.request_handler('general', self.api_key1)

    def world(self):
        self.request_handler('world', self.api_key1)

    def nation(self):
        self.request_handler('nation', self.api_key1)

    def business(self):
        self.request_handler('business', self.api_key1)

    def technology(self):
        self.request_handler('technology', self.api_key2)

    def entertainment(self):
        self.request_handler('entertainment', self.api_key2)

    def sports(self):
        self.request_handler('sports', self.api_key2)

    def science(self):
        self.request_handler('science', self.api_key2)

    def request_handler(self, categories, access_key):
        api = 'https://gnews.io/api/v4/top-headlines'
        request_url = api + '?apikey=' + access_key + '&category=' + categories + '&lang=en'
        # 发送 GET 请求到指定的 URL
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            dao = PostsDao()
            for item in data['articles']:
                # 处理发布时间的时区，统一为东八区 2024-01-26T11:01:11Z
                published_at_str = item['publishedAt']
                # 解析原始字符串为datetime对象，并指定其为UTC时间
                # 注意这里使用了%z来解析时区信息，对于'Z'我们可以在strptime之前替换为空字符串或者直接使用'%Y-%m-%dT%H:%M:%S%z'
                published_at_utc = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%S%z")

                # 将UTC时间转换为北京时区（东八区）
                beijing_tz = ZoneInfo('Asia/Shanghai')
                published_at_beijing = published_at_utc.astimezone(beijing_tz)

                # 格式化为MySQL DATETIME所需的格式
                formatted_published_at = published_at_beijing.strftime("%Y-%m-%d %H:%M:%S")

                #处理logo
                domain = crawl_util.get_main_domain(item['url'])

                posts_dict = {
                    'xid': sign_util.generate_random_string(10),
                    'title': item['title'],
                    'thumbnail': item['image'],
                    'description': item['description'],
                    'content': item['content'],
                    'source': 'gnews',
                    'category': categories,
                    # 反代 google api 获取站点的logo
                    'logo': f'https://api.findings.liurb.org/tool/favicon?url={domain}',
                    'url': item['url'],
                    'url_sid': sign_util.sha256_hash(item['url']),
                    'publisher': item['source']['name'],
                    'published_at': formatted_published_at
                }
                dao.create_posts(posts_dict)