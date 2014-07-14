# -*- coding: utf-8 -*-
__metaclass__=type
import UserString
from pyquery import PyQuery as pyq
from spider import AcmSpider
import httplib
import urllib2
class Uva(AcmSpider):
	TARGET={
			'id':'No',
			'ojid':'OJ-id',
			'title':'Title',
			'accepted':'Accepted',
			'submitted':'Submitted',
			'users':'Users',
			'solving':'Solving',
			}
	def __init__(self,url,name):
		super(Uva,self).__init__(url,name)
		self.ojids=[]

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
				#httplib.HTTPConnection._http_vsn = 11
				#httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
			if doc("div:contains('Browse Problems')+div+table img").attr('alt')=="FOLDER":
				print "[folder]",curdir
				links=doc("div:contains('Browse Problems')+div+table a")
				for a in links:
					dirs.append(self.root+'/'+pyq(a).attr('href'))
			else:
				print "[file]",curdir
				self.pages.append(curdir)
	   



	def parsePage(self,page):
		try:
			doc=pyq(page)
		except (httplib.IncompleteRead,urllib2.URLError):
			print "Bug!!!!!!!!!!!!!1"
			httplib.HTTPConnection._http_vsn = 10
			httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
			doc=pyq(page)
		trs= doc("div:contains('Browse Problems')+div+table tr[class!='sectiontableheader']")
		for tr in trs:
			problem={}
			try:
				problem['ojid']=pyq(tr).find('td').eq(1).text().split(u'\xa0')[0].encode('utf8')
				if problem['ojid'] in self.ojids:
					continue
				else:
					self.ojids.append(problem['ojid'])
				print "id:",problem['ojid']
				problem['title']=pyq(tr).find('td').eq(1).text().split(u'\xa0')[2]
			except IndexError:
				print "wTTTTTTTTTTTTFFFFFFFFFFFFF!"
			#print problem['title'],type(problem['title'])
			problem['submitted']=str(pyq(tr).find('td').eq(2).text())
			ratio=pyq(tr).find('td').eq(3).find('div div').text()
			try:
				ratio=float(ratio.rstrip('%'))*0.01
				problem['accepted']=str(int(int(pyq(tr).find('td').eq(2).text())*ratio))
			except ValueError:
				problem['accepted']=str(0)
			problem['users']=str(pyq(tr).find('td').eq(4).text())
			ratio=pyq(tr).find('td').eq(5).find('div div').text()
			try:
				ratio=float(ratio.rstrip('%'))*0.01
				problem['solving']=str(int(int(pyq(tr).find('td').eq(4).text())*ratio))
			except ValueError:
				problem['solving']=str(0)
			self.problems.append(problem)

	def genData(self):
		for page in self.pages:
			self.parsePage(page)
		self.problems.sort(lambda p1,p2:int(p1['ojid'])-int(p2['ojid']))
		s = UserString.MutableString('')
		f=file(self.name,'w')
		s+=self.TARGET['id']+','+self.TARGET['ojid']+','+self.TARGET['title']+','+self.TARGET['accepted']+','+self.TARGET['submitted']+','+self.TARGET['users']+','+self.TARGET['solving']+'\n'
		for i in range(len(self.problems)):
			#print str(i)+'\t'+'\t'.join(self.problems[i].values())+'\n'
			p=self.problems[i]
			#print p['ojid'],p['title'],p['accepted'],p['submitted']
			#print type(p['ojid']),type(p['title']),type(p['accepted']),type(p['submitted'])
			s+=str(i+1)+','+p['ojid']+','+p['title'].encode('utf8')+','+p['accepted']+','+p['submitted']+','+p['users']+','+p['solving']+'\n'
		f.write(str(s))
		f.close()	

if __name__=='__main__':
	uva=Uva("http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8","UVA.csv")
	uva.getPages()
	#uva.pages.append("http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=5")
	uva.genData()

