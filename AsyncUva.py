# -*- coding: utf-8 -*-
__metaclass__=type
import UserString
import functools
from pyquery import PyQuery as pyq
from spider import AcmSpider
import httplib
import urllib2
from tornado import ioloop
from tornado import httpclient
request_count=0
count=0

class AsyncUva(AcmSpider):
	def __init__(self,url,name):
		super(AsyncUva,self).__init__(url,name)
		self.ojids=[]

	def getPages(self):
		dirs=[]
		http_client=httpclient.AsyncHTTPClient()
		dirs.append(self.url)
		def _isFinshied():
			print len(dirs),request_count
			if not dirs and request_count==0:
				print "stop"
				io_loop.stop()
				return
			else:
				_asyncGet()
				io_loop.add_callback(_isFinshied)

		def _parse(response):
			global request_count
			if response.error:
				print	"Error",response.error
				http_client.fetch(response.request,_parse)
				request_count+=1
				print "add",request_count
				print "try again"
			else:
				curdir=response.effective_url
				doc=pyq(response.body)
				if doc("div:contains('Browse Problems')+div+table img").attr('alt')=="FOLDER":
					print "[folder]",curdir
					links=doc("div:contains('Browse Problems')+div+table a")
					for a in links:
						dirs.append(self.root+'/'+pyq(a).attr('href'))
				else:
					print "[file]",curdir
					self.pages.append(curdir)
					self.cache[curdir]=doc
				print "-",request_count
			request_count-=1

		def _asyncGet():
			while dirs:
				cur=dirs.pop()
				http_client.fetch(cur,_parse)
				global request_count
				print "add",request_count
				request_count+=1

		io_loop=ioloop.IOLoop.instance()
		io_loop.add_callback(_isFinshied)
		io_loop.start()


	def parsePage(self,io_loop,http_client,response,*args):
		global count
		if count>len(self.pages):
			print "stop"
			io_loop.stop()
			return
		try:
			if response.error:
				print	"Error,try again",response.error
				http_client.fetch(response.request,functools.partial(self.parsePage,io_loop,http_client))
				return
		except:
			pass
		print count
		count+=1
		if args:
			doc=args[0]
		else:
			doc=pyq(response.body)
		trs= doc("div:contains('Browse Problems')+div+table tr[class!='sectiontableheader']")
		for tr in trs:
			problem={}
			problem['ojid']=pyq(tr).find('td').eq(1).text().split(u'\xa0')[0].encode('utf8')
			if problem['ojid'] in self.ojids:
				continue
			else:
				self.ojids.append(problem['ojid'])
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
	def period(self,io_loop):
		print "period",count,len(self.pages)
		if count==len(self.pages):
			io_loop.stop()
		io_loop.add_callback(functools.partial(self.period,io_loop))

	def genData(self):
		http_client=httpclient.AsyncHTTPClient()
		print "have %d pages" % len(self.pages)
		io_loop=ioloop.IOLoop.instance()
		for page in self.pages:
			if self.cache[page]:
				print "cache",page
				self.parsePage([],[],[],self.cache[page])
			else:
				print "fetch",page
				http_client.fetch(page,functools.partial(self.parsePage,io_loop,http_client))
		io_loop.add_callback(functools.partial(self.period,io_loop))
		io_loop.start()

		self.problems.sort(lambda p1,p2:int(p1['ojid'])-int(p2['ojid']))
		s = UserString.MutableString('')
		f=file(self.name,'w')
		s+=self.TARGET['id']+','+self.TARGET['ojid']+','+self.TARGET['title']+','+self.TARGET['accepted']+','+self.TARGET['submitted']+'\n'
		for i in range(len(self.problems)):
			#print str(i)+'\t'+'\t'.join(self.problems[i].values())+'\n'
			p=self.problems[i]
			#print p['ojid'],p['title'],p['accepted'],p['submitted']
			#print type(p['ojid']),type(p['title']),type(p['accepted']),type(p['submitted'])
			s+=str(i+1)+','+p['ojid']+','+"'"+p['title'].encode('gbk')+"'"+','+p['accepted']+','+p['submitted']+'\n'
		f.write(str(s))
		f.close()	



if __name__=="__main__":
	uva=AsyncUva("http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8","a.csv")
	uva.getPages()
	print uva.pages
	#uva.pages.append("http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=5")
	uva.genData()


