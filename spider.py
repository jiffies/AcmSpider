# -*- coding: utf-8 -*-  
__metaclass__=type
import UserString
import urllib2
import urllib
from urlparse import urlparse
from pyquery import PyQuery as pyq

class AcmSpider:
	TARGET={
			'id':'No',
			'ojid':'题目编号',
			'title':'题目标题',
			'accepted':'做对次数',
			'submitted':'提交次数'
			}
	def __init__(self,url,name):
		self.url=url
		parsed=urlparse(url)
		self.root=parsed.scheme+"://"+parsed.hostname
		self.problems=[]
		self.name=name

	def getPages(self):
		self.pages=[]
		pass

	def parsePage(self):
		pass

	def genData(self):
		for page in self.pages:
			self.parsePage(page)
		self.problems.sort(lambda p1,p2:int(p1['ojid'])-int(p2['ojid']))
		s = UserString.MutableString('')
		f=file(self.name,'w')
		s+=self.TARGET['id']+'\t'+self.TARGET['ojid']+'\t'+self.TARGET['title']+'\t'+self.TARGET['accepted']+'\t'+self.TARGET['submitted']+'\n'
		for i in range(len(self.problems)):
			#print str(i)+'\t'+'\t'.join(self.problems[i].values())+'\n'
			p=self.problems[i]
			#print p['ojid'],p['title'],p['accepted'],p['submitted']
			#print type(p['ojid']),type(p['title'])
			s+=str(i)+'\t'+p['ojid']+'\t'+p['title'].encode('utf8')+'\t'+p['accepted']+'\t'+p['submitted']+'\n'
		f.write(str(s))
		f.close()	


		


class Zoj(AcmSpider):
	def getPages(self):
		doc=pyq(self.url)
		links=doc("form[name=\"ProblemListForm\"] > a")
		self.pages=[self.root+pyq(l).attr('href') for l in links]

	def parsePage(self,page):
		doc=pyq(page)
		trs=doc('table.list tr[class!="rowHeader"]')
		for tr in trs:
			problem={}
			problem['ojid']=str(pyq(tr).find('td.problemId a').text())
			print "id:",problem['ojid']
			try:
				problem['title']=pyq(tr).find('td.problemTitle a').text().decode('utf8')
			except:
				problem['title']=''
			#print pyq(tr).find('td.problemStatus a').text()
			if len(pyq(tr).find('td.problemStatus a'))==2:
				problem['accepted']=str(pyq(tr).find('td.problemStatus a').text().split(' ')[0])
				problem['submitted']=str(pyq(tr).find('td.problemStatus a').text().split(' ')[1])
			else:
				print "ggggggggggggggggot!"
				problem['accepted']='0'
				problem['submitted']=str(pyq(tr).find('td.problemStatus a').text().split(' ')[0])

			self.problems.append(problem)
			

if __name__=='__main__':
	zoj=Zoj("http://acm.zju.edu.cn/onlinejudge/showProblemsets.do",'ZOJ')
	zoj.getPages()
	zoj.genData()
	















