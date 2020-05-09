# /usr/bin/python 3.7
# -*-coding:utf-8*-

from scrapy import cmdline


name = 'house_gz'
cmd = 'scrapy crawl {}'.format(name)
cmdline.execute(cmd.split())
