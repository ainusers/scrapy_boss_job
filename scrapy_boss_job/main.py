from scrapy import cmdline

# 运行scrapy crawl douban_spider
# cmdline.execute('scrapy crawl job'.split())

# 文件导出csv
cmdline.execute('scrapy crawl job -o job.csv'.split())
