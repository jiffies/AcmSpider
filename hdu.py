# -*- coding: utf-8 -*-
__metaclass__=type
from pyquery import PyQuery as pyq
from spider import AcmSpider
import urllib2
import re
class Hdu(AcmSpider):
	def getPages(self):
		doc=pyq(self.url)
		links=doc("font:contains('Volume')").eq(0).parent().find('a')
		self.pages=[self.root+'/'+pyq(l).attr('href') for l in links]


	def parsePage(self,page):
		"""
		['p(0,1000,-1,"A + B Problem",126589,399562)',
		 'p(1,1001,-1,"Sum Problem",67850,272371)',
		 ]
		"""
		#doc=pyq(page)
		text=urllib2.urlopen(page).read()
		problems=re.findall('</tr><script language="javascript">(.*)</script>',text)[0].split(';')
		print page
		#problems=doc("table.table_text script").text().split(';')
		for item in problems:
			print item
			if not item:
				continue
			problem={}
			ps=item.split(',')
			problem['ojid']=ps[1]
			print problem['ojid']
			problem['title']=','.join(ps[3:-2]).strip('"').decode('gbk')
			#print problem['title']
			problem['accepted']=ps[-2]
			problem['submitted']=ps[-1].strip(')')
			self.problems.append(problem)
if __name__=='__main__':
	hdu=Hdu("http://acm.hdu.edu.cn/listproblem.php?vol=1","HDU.csv")
	hdu.getPages()
	hdu.genData()
