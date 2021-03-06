# -*- coding: utf-8 -*-

# Scrapy settings for mm_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'moko_spider'

SPIDER_MODULES = ['moko_spider.spiders']
NEWSPIDER_MODULE = 'moko_spider.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'middlewares.RotateUserAgent': 110,
}

ITEM_PIPELINES = {
    'moko_spider.pipelines.MyImagesPipeline': 200,
    'moko_spider.pipelines.MmSpiderPipeline': 300,
}
IMAGES_STORE = './image/'
DOWNLOAD_DELAY = 3
IMAGES_EXPIRES = 90  # 过期天数
MYIMAGESPIPELINE_IMAGES_MIN_WIDTH = 600
MYIMAGESPIPELINE_IMAGES_MIN_HEIGHT = 600

# 图片的最小宽度
IMAGES_THUMBS = {  # 缩略图的尺寸，设置这个值就会产生缩略图
    'small': (50, 50),
    'big': (270, 270),
}

MONGODB_SERVER = "10.200.10.224"
MONGODB_PORT = 27017
MONGODB_DB = 'qb_db'
PROXY_DB = 'proxy_db'
MONGODB_COLLECTION = 'qb_image'
PROXY_COLLECTION = 'proxy_ip'
HUABAN_DB = 'huaban_image'
HUABAN_COLLECTION = 'moko_models'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'mm_spider (+http://www.yourdomain.com)'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True
COOKIES_ENABLED = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'mm_spider.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'mm_spider.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'mm_spider.pipelines.SomePipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
