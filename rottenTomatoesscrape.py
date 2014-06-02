import re
from bs4 import BeautifulSoup as bs
import requests

#Query variable can be set to raw_input, string, arg, etc.
query = raw_input("Enter search query: ")

class MovieSearchResult(object):
	def __init__(self, soupTag):
		self.name = soupTag.div.h3.a.getText()
		self.url = self.getURL(soupTag)
		self.year = soupTag.find('span',{'class':"movie_year"}).getText()
		self.score = self.getScore(soupTag)
		self.cast = self.getCastLinks(soupTag)
		
	def getURL(self, soupTag):
		baseURL = "http://www.rottentomatoes.com"
		shortURL = str(soupTag.div.h3.a['href'])
		completeURL = baseURL + shortURL
		return completeURL
	
	def getCastLinks(self, soupTag):
		reLinks = soupTag.findAll('a',{'class':""})
		cast = {}
		for reLink in reLinks:
			if "/celebrity/" in reLink['href']:
				cast[reLink.getText()] = reLink['href']
		return cast
	
	def getScore(self, soupTag):
		if soupTag.find('span',{'class':"tMeterScore"}):
			rating = soupTag.find('span',{'class':"tMeterScore"}).getText()
		else:
			rating = "Unavailable"
		return rating
	
	def Preview(self):
		print "Title: " + self.name + self.year
		print "Rotten Tomatoes Score: " + self.score
		print "Cast: " + str(self.cast.keys())
		
class MoviePage(object):
	
	def __init__(self, soup):
		self.name = soup.find('span',{'itemprop':"name"}).getText()
		#self.url = 
		self.score = self.getScore(soup)
		self.cast = self.getCast(soup)
		self.synopsis = soup.find('p',{'id':"movieSynopsis"}).getText()
	
	def getScore(self, soup):
		score = {}
		scoreTag = soup.find('div',{'id':"scorePanel"})
		score["all critics"] = scoreTag['data-score']
		score['BreakDown'] = scoreTag.find('p',{'class':"critic_stats"}).getText().replace('\t', '').replace('\n', '').replace(' ','')
		score['audience'] = scoreTag.find('a',{'class':"fan_side"}).getText().replace('\t', '').replace('\n', '').replace(' ','')
		return score
		
	def getCast(self, soup):
		cast = {}
		castTag = soup.find('div',{'id':"cast-info"})
		names = castTag.findAll('span',{'itemprop':"name"})
		characters = castTag.findAll('span', {'class':"characters"})
		pages = castTag.findAll('a',{'itemprop':"url"})
		for i in names:
			num = names.index(i)
			cast[str(characters[num].getText())] = (str(names[num].getText()), "http://www.rottentomatoes.com" + pages[num]['href'])
		return cast
	
	def Preview(self):
		print self.name
		print "Rotten Tomatoes Score:  " + str(self.score['all critics'])
		print self.cast.values()
		
	
def main(query):
	url = "http://www.rottentomatoes.com/search/?search="
	raw_string = re.compile(r' ')
	fullQuery = raw_string.sub('+', query)
	r = requests.post(url + fullQuery)
	soup = bs(r.content)
	if soup.find('ul',{'class':"results_ul"}):
		tags = soup.findAll('li',{'class':"media_block bottom_divider clearfix"})
		results = {}
		for tag in tags:
			info = MovieSearchResult(tag)
			resultNum = str(tags.index(tag) + 1)
			results[resultNum] = info.url
			print "__________________________"
			print "Result Number "  + resultNum
			info.Preview()
		selectResult = raw_input("Please enter the result number you would like to see: ")
		r = requests.post(results[selectResult])
		mSoup = bs(r.content) #targetURL
		page = MoviePage(mSoup)
	elif soup.find('h1',{'class':"center noresults"}):
		page = {}
		print "Sorry, no results. Please check your search query and try again!"
		restart = raw_input("Try again?  y/n:")
		if restart.lower() == 'y':
			main(raw_input("Enter search query: "))
		else:
			exit()
	else:
		mSoup = soup
		page = MoviePage(mSoup)
	return page
		

if __name__ =="__main__":
	main(query)
