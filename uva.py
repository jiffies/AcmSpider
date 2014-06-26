# -*- coding: utf-8 -*-
__metaclass__=type
from pyquery import PyQuery as pyq
from spider import AcmSpider
import httplib
import urllib2
class Uva(AcmSpider):
	def getPages(self):
		dirs=[]
		#doc=pyq(self.url)
		#while doc("div:contains('Browse Problems')+div+table img").attr('alt')=="FOLDER" and (None in dirs[p].values())：
			#dirs[p].update(dict.fromkeys([self.root+'/'+a.attr('href') for a in doc("div:contains('Browse Problems')+div+table a")]))
			#for d,c in dirs[p].items():
		dirs.append(self.url)
		while dirs:
			curdir=dirs.pop()
			try:
				doc=pyq(curdir)
			except (httplib.IncompleteRead,urllib2.URLError):
				print "Bug!!!!!!!!!!!!!1"
				httplib.HTTPConnection._http_vsn = 10
				httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
				doc=pyq(curdir)
			if doc("div:contains('Browse Problems')+div+table img").attr('alt')=="FOLDER":
				print "[folder]",curdir
				links=doc("div:contains('Browse Problems')+div+table a")
				for a in links:
					dirs.append(self.root+'/'+pyq(a).attr('href'))
			else:
				print "[file]",curdir
				self.pages.append(curdir)
	   



	def parsePage(self,page):
		doc=pyq(page)
		trs= doc("div:contains('Browse Problems')+div+table tr[class!='sectiontableheader']")
		for tr in trs:
			problem={}
			problem['ojid']=pyq(tr).find('td').eq(1).text().split(u'\xa0')[0].encode('utf8')
			print "id:",problem['ojid']
			problem['title']=pyq(tr).find('td').eq(1).text().split(u'\xa0')[2]
			#print problem['title'],type(problem['title'])
			problem['submitted']=str(pyq(tr).find('td').eq(2).text())
			ratio=pyq(tr).find('td').eq(3).find('div div').text()
			try:
				ratio=float(ratio.rstrip('%'))*0.01
				problem['accepted']=str(int(int(pyq(tr).find('td').eq(2).text())*ratio))
			except ValueError:
				problem['accepted']=str(0)
			self.problems.append(problem)

if __name__=='__main__':
	uva=Uva("http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8","UVA.csv")
	uva.getPages()
	#uva.pages.append("http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=5")
	uva.genData()

