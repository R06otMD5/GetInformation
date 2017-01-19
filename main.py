#/bin/python
#-*- coding: utf-8 -*-

import requests,sys,codecs,re
from lxml import etree
import time
import sendmail



url = 'http://www.freebuf.com'

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}


def write2File(WriteName):
	now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	TempleteFile = 'send_templete.html'
	SendOutFile = 'send.html'
	with codecs.open(TempleteFile, 'r', 'utf-8') as file_temp:
		content_temp = file_temp.read()
		pos = content_temp.find('<!-->update<!-->')

	head_str = "<html>\n<div height=\"20\"><p>" + now_time + "</p></div>\n"
	str_update = ''
	i = 0
	with codecs.open(SendOutFile,'w','utf-8') as file:
		for every in WriteName:
			if i > 4:
				break
			if every[2] == u'招聘' or every[2] == u"人物志":
				continue

			str_update = str_update + "<tr>\n<td>" + every[0] + "</td>\n<td>" + every[1] + "</td>\n<td>" + every[2] + "</td>\n<td>" + every[3] + "</td>\n</tr>"
			i = i + 1
		file.write(head_str + content_temp[:pos] + str_update + content_temp[pos:])
		file.flush()

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
	maps = zip(titles,texts,tags,links)
	return maps


def main():
	result = initRespons(url,headers)
	maps = dealRespons(result)
	write2File(maps)
	sendmail.sendemail()



if __name__ == '__main__':
	main()