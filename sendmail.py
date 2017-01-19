#!/usr/bin/env python
#coding: utf-8  
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
from email import encoders
from email.utils import parseaddr, formataddr
import time
import codecs,re

now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))


def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr(( \
		Header(name, 'utf-8').encode(), \
		addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendemail():
	subject = Header(u'新闻信息收集 %s' % now_time, 'utf-8').encode()
	with codecs.open('send.html', 'r', 'utf-8') as f:
		out = f.read()
	msg = MIMEText(out,'html','utf-8')
	with codecs.open('set.conf', 'r', 'utf-8') as conf:
		for conf_line in conf.readlines():
			conf_line = conf_line.strip('\r\n').split(':')
			if conf_line[0] == 'mailserver':
				print conf_line[1]
				smtpserver = conf_line[1]
			elif conf_line[0] == 'sender':
				sender_str = conf_line[1]
				print sender_str
				sender = re.findall('<.*?>',conf_line[1])[0][1:-1]
			elif conf_line[0] == 'receiver':
				receiver_str = conf_line[1]
				receiver = re.findall('<.*?>',conf_line[1])[0][1:-1]
			elif conf_line[0] == 'password':
				password = conf_line[1]
			else:
				continue

	msg['Subject'] = subject
	msg['From'] = _format_addr(sender_str)
	msg['To'] = _format_addr(receiver_str)

	print smtpserver
	smtp = smtplib.SMTP()
	smtp.connect(smtpserver)
	print smtpserver
	smtp.login(sender, password)
	print 'sending..........'
	smtp.sendmail(sender, receiver, msg.as_string())
	print('ok!!!!!!!!!!')
	smtp.quit()

