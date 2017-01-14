#/bin/python
#-*- coding: utf-8 -*-

import requests,sys,codecs,re
from lxml import etree

url = 'http://www.freebuf.com'

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}


def write2File(FileName,WriteName):
	file = codecs.open(FileName,'w','utf-8')
	try:
		for every in WriteName:
                	file.write("%s,%s,%s\n" % (every[0],every[1],every[2]))
		file.flush()
	except Exception, e:
		raise e
		return -1
	finally:
		file.close()
		return 0

def xpath2List(XpathList):
	newXpathList = []
	for Xpath in XpathList:
        	newXpathList.append(Xpath.text)
	return newXpathList


def initRespons(url,headers):
	try:
		result = requests.get(url,headers=headers)
		result.raise_for_status()
	except requests.RequestException as e:
		print(e)
	return result


def dealRespons(result):
	tree = etree.HTML(result.text)
	titles = tree.xpath('//div[@id="timeline"]/*/div[@class="news-info"]/dl/dt/a/@title')
	links = tree.xpath('//div[@id="timeline"]/*/div[@class="news-info"]/dl/dt/a/@href')
	tags = tree.xpath('//div[@id="timeline"]/*/div[@class="news-info"]/div[@class="news_bot"]/span[@class="tags"]/a[1]')
	tags = xpath2List(tags)
	texts = tree.xpath('//div[@id="timeline"]/*/div[@class="news-info"]/dl/dd[@class="text"]')
	texts = xpath2List(texts)
	maps = zip(titles,texts,links,tags)
	for title in maps:
		print 'abc:',title
	return maps


def main():
	result = initRespons(url,headers)
	maps = dealRespons(result)
	write2File('./tet.txt',maps)


if __name__ == '__main__':
	main()