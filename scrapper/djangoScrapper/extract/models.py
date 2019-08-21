from django.db import models
import os,time
from urllib.parse import urlparse
from urllib.request import urlopen
import urllib.request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
#from pandas import DataFrame
import csv
import re
import requests

#filter and get matched elements with specific keywords
def filterArray(list,source):
	srcIDs=[]
	matched=[]
	excelReader=os.path.abspath(os.path.dirname(__file__))+source			
	with open(excelReader) as common:
		reader = csv.reader(common, delimiter=',')
		for row in reader:
			srcIDs.append(str(row[0]))
	
	for item in list:
		match=False
		for itemRow in srcIDs:
			if(str(item).lower().find(str(itemRow).lower())!=-1):
				matched.append(str(item))
	return matched	
		

#get all possible currencies		
def getAllCurrencies(source):
	currencies=[]
	excelReader=os.path.abspath(os.path.dirname(__file__))+source			
	with open(excelReader) as common:
		reader = csv.reader(common, delimiter=',')
		for row in reader:
			currencies.append(str(row[0]))
	return currencies

#check if string contains numbers		
def hasNumbers(inputString):
	for char in inputString:
		if char=='0':
			continue
		elif char.isdigit():
			return True
	return False

def checkEqual(lst):
   return lst[1:] == lst[:-1]

def visible(element):
    if element.parent.name in ['style', 'script', 'document', 'head', 'title']: 
    	return False
    elif re.match('<!--.*-->', str(element)): 
    	return False
    elif re.match('\n', str(element)): 
    	return False
    else:
        return True

def validateURL(domain):
	try:
		request = requests.get(domain)
		if request.status_code == 200:
			return True
		else:
			return False
	except:
		pass

#remove duplicates from a list
def removeDuplicates(lst):
 	newlist=[]
 	for i in lst:
 		if i not in newlist:
 			newlist.append(i)
 	return newlist

# Create your models here.
def scrape_data(r,request):	
	import csv
	from bs4 import BeautifulSoup
	priceIDsSource='/../static/priceIDs.csv'
	priceDictionary='/../static/priceDictionary.csv'
	imageIDsSource='/../static/imageIDs.csv'
	ImageDictionary='/../static/ImageDictionary.csv'
	descriptionIDsSource='/../static/descriptionIDs.csv'
	descriptionDictionary='/../static/descriptionDictionary.csv'
	recommendationIDsSource='/../static/recommendationIDs.csv'
	recommendationDictionary='/../static/recommendationDictionary.csv'
	titleDictionary='/../static/NameDictionary.csv'
	currenciesSource='/../static/currencies.csv'
	price=''
	review=''
	name=''
	image=''
	productDescription=''
	#get all ids from html
	def getArrayIDs():
		arrayi=[]
		for tag in htmlContent.find_all():
			#print(tag.text)
			if(tag.name!='script'):
				tag_id=tag.get('id')
				if tag_id is None:
					pass
				else :
					currentID=str(tag_id)
					arrayi.append(currentID)
		return arrayi
		
	#get all classes from html
	def getArrayClasses():
		arrayc=[]
		for tag in htmlContent.find_all():
		#print(tag.text)
			if(tag.name!='script'):
				tag_class=tag.get('class')
				if tag_class is None:
					pass
				else:
					for clas in tag_class:
						if clas in arrayc:
							pass
						else:
							arrayc.append(clas)
		return arrayc
	
	def getArrayClasses1():
		arrayc=[]
		for tag in htmlContent.find_all():
			tag_class=tag.get('class')
			if tag_class is None:
				pass
			else:
				for clas in tag_class:
					if clas in arrayc:
						pass
					else:
						arrayc.append(clas)
		return arrayc


	#get data using itemprop key word	
	def itemprop(key):
		return htmlContent.find(itemprop=key)
		
	#get product description
	def getDescription():
		productDescription=''
		csvFileNotExist3=os.path.abspath(os.path.dirname(__file__))+descriptionDictionary		
		with open(csvFileNotExist3) as common3:
			readerCommon3 = csv.reader(common3, delimiter=',')
			for itemRow in readerCommon3:
				# 0 for price
				break
				try:
				    
				   	descriptionTest=htmlContent.select(itemRow[0])
				   	#print(descriptionTest)
				   	if descriptionTest:
				   		#print(descriptionTest)
				   		productDescription=descriptionTest
				   		print('description from css selectors')
				   		return productDescription
				    		#print(productDescription)
				    		#print('ayreeeeeee')
					    		
				except NameError:
				    Nochange = None
		
		
		productDescription=itemprop('description') 
		if productDescription:
			if 'content' in productDescription.attrs and productDescription['content']!='':
				productDescription=productDescription['content']
			else:
				productDescription=productDescription.text
				
			print('description from itemprop')
			return productDescription
		
		parag=htmlContent.find_all('p')
		productDescription=''
		try:
			for a in parag:
				productDescription+=a.text+'\n'
			print('description from p')
			return productDescription

		except:
			pass

		#get matched ids and classes for description using dictionaries key words	
		matchedDescriptionIDs=filterArray(arrayIDs,descriptionIDsSource)
		matchedDescriptionClasses=filterArray(arrayClasses,descriptionIDsSource)
			
		if len(matchedDescriptionIDs)>0:
			for i in range(len(matchedDescriptionIDs)):
				desc=htmlContent.find(id=matchedDescriptionIDs[i])
				#print(matchedDescriptionIDs)
				if desc is not None:
					#if desc.text.find('Description'):
					productDescription=desc
					print('description from id')
					return productDescription
						
		elif len(matchedDescriptionClasses)>0:
			for i in range(len(matchedDescriptionClasses)):
				desc=htmlContent.find(class_=matchedDescriptionClasses[i])
				#print(matchedDescriptionClasses)
				if desc is not None:
					if len(desc.text)>30:
						productDescription=desc
						print('description from class')
						return productDescription
		
		
		productDescription=getDescription1()
		#if type(productDescription) is not str:
		#	productDescription=productDescription.text
		print('description from all text')
		return productDescription

	#get all visible text
	def getDescription1():
		# get text
		text = htmlContent.get_text()
		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)
		return text
	
	

	#get product title
	def getTitle():
		name=''
		
		csvFileNotExist4=os.path.abspath(os.path.dirname(__file__))+titleDictionary			
		with open(csvFileNotExist4) as common4:
			readerCommon4 = csv.reader(common4, delimiter=',')
			for itemRow in readerCommon4:
				# 0 for price
				try:
				   	nameTest=htmlContent.select(itemRow[0])
				   	#print(nameTest)
				   	if nameTest:
				   		name=nameTest
				   		return name
				    		
				except NameError:
				    Nochange = None
		
		name=htmlContent.title.string	
		print('title from title.string')
		return name			

	#get product price
	def getPrice():
		
		if(domain=='www.timberland.de'):
			prc = htmlContent.find('meta', attrs={'property': 'og:price:amount', 'content': True})
			price='EUR '+(prc['content'])
			return price
		
		for script in htmlContent(["script", "style", "function"]):
			script.extract()

		price=''
		csvFileNotExist=os.path.abspath(os.path.dirname(__file__))+'/../static/priceDictionary.csv'			
		with open(csvFileNotExist) as common:
			readerCommon = csv.reader(common, delimiter=',')
			for itemRow in readerCommon:
				#break
				try:
				    priceTest=htmlContent.select(itemRow[0])
				    if priceTest:
				    	
				    	if(checkEqual(priceTest)):
				    		if priceTest:
				    			price=priceTest[0].text
				    		if(price==''):
				    			pass
				    		else:
				    			print('price from dictionary ')

				    			if hasNumbers(price):
				    				print(price)
				    				return price
				    	else:
				    		if price:
					    		price=priceTest
					    		if(price==''):
					    			pass
					    		else:
					    			print('price from dictionary')
					    			
					    			if hasNumbers(price):
					    				print(price)
					    				return price
				    		
				except NameError:
				    Nochange = None
		
		cur=''
		price=itemprop('price')
		if price:
			if 'content' in price.attrs:
				price=price['content']
			else:
				price=price.text
			#for currency in currencies:
			if hasNumbers(price):#fix it for 0 price
				for currency in currencies:
					if  price.find(currency)!=-1:#price.find(currency)!=-1
						print('price from itemprop')
						return price
				else:
					#getCurrency if available
					priceCur=itemprop('priceCurrency')
					if not priceCur:
						priceCur=itemprop('currency')
					if priceCur:
						if 'content' in priceCur.attrs and priceCur['content']!='':
							cur=priceCur['content']
							price=price+cur
						else:
							cur=priceCur.text
							price=price+cur
					print('price from itemprop')
					return price
		

		#get matched ids
		matchedPriceIDs=filterArray(arrayIDs,priceIDsSource)
		#get all classes.
		matchedPriceClasses=filterArray(arrayClasses,priceIDsSource)
		
		found=False
		if (len(matchedPriceClasses)>0):
			for i in range(len(matchedPriceClasses)):
				checkedprice=htmlContent.find(class_=matchedPriceClasses[i])
				if checkedprice is None:
					pass
				else:
					b=checkedprice.text
					c=b.strip()

					for currency in currencies:
						if hasNumbers(c) and (c.find(currency) or c.find('USD')!=-1 or c.find('EUR')!=-1 or c.find('€')!=-1 or c.find('$')!=-1):#and c!='0.0' and c!='0,00' and c!='0.00' and c!='0,0' and len(c)<70 and c!='CHF0.00' and c.find('0,00')==-1:
							price=c
							return price
		if(len(matchedPriceIDs)>0):

			myprice=[]
			for i in range(len(matchedPriceIDs)):
				checkedprice=htmlContent.find(id=matchedPriceIDs[i])
				if checkedprice is None:
					pass
				else:
					b=checkedprice.text
					c=b.strip()
					for currency in currencies:
						if hasNumbers(c) and (c.find(currency) or c.find('USD')!=-1 or c.find('EUR')!=-1 or c.find('€')!=-1 or c.find('$')!=-1) and c!='0.0' and c!='0,00' :#and c!='0.00' and c!='0,0' and len(c)<0 and c!='CHF0.00' and c.find('0.00')==-1:
							prc=checkedprice.text.replace('\n','')
							myprice.append(prc)
							
			if  myprice:
				price=''
				myprice=removeDuplicates(myprice)
				for i in myprice:
					price+=i
			#price+=myprice[0]+'ottaa'
		#if type(price) is not str and price is not None:
		#		price=price.text
		return price			

	#get product reviews
	def getReviews():
		review=''
		csvFileNotExist4=os.path.abspath(os.path.dirname(__file__))+recommendationDictionary			
		with open(csvFileNotExist4) as common4:
			readerCommon4 = csv.reader(common4, delimiter=',')
			for itemRow in readerCommon4:
				# 0 for price
				try:
				   	reviewTest=htmlContent.select(itemRow[0])
				   	if(reviewTest):
				   		review=reviewTest
				   		#print(review)
				    		
				except NameError:
				    Nochange = None
		if review is None:
			review=''
		return review

	#get product image
	def getImage():
		image=''
		#get image from meta-data
		imageurl = htmlContent.find('meta', attrs={'property': 'og:image', 'content': True})
		imagenameUrl = htmlContent.find('meta', attrs={'name': 'og:image', 'content': True})
		if imageurl:
			src=imageurl['content']
			#print('imageurl')
			if src.find('http')!=-1:
				image = '<img class="maxWidth600" alt="cannot get image" src="'+src+'"/>'
				print('image from meta')
			else:
				if src.startswith('/'):
					image = '<img class="maxWidth600" alt="cannot get image" src="'+'https://'+domain+src+'"/>'
				else:
					image = '<img class="maxWidth600" alt="cannot get image" src="'+'https://'+domain+'/'+src+'"/>'
			return image	

		elif imagenameUrl:
			print('imageurl name')
			image = '<img class="maxWidth600" src="'+imagenameUrl['content']+'"/>'
			return image
			
		#if no meta-data look for patterns from dictionary to get @Image.
		csvFileNotExist1=os.path.abspath(os.path.dirname(__file__))+ImageDictionary			
		with open(csvFileNotExist1) as common1:
			readerCommon1 = csv.reader(common1, delimiter=',')
			for itemRow in readerCommon1:
				try:
				    if(image==''):
				    	imageTest=htmlContent.select(itemRow[0])
				    	if imageTest:

				    		tagname=imageTest[0].name
				    		print('image from dictionary')
				    		if tagname=='img':
				    			try:
					    			imagesrc=imageTest[0]['src']
					    			if validateURL(imagesrc):
					    				image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
					    				print('11111111')
					    				return image
					    			else:
					    				if imagesrc.startswith('/'):
					    					imageTest[0]['src']='https://'+domain+imagesrc
					    					if validateURL(imageTest[0]['src']):
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0]['src']+'"/>'
					    						

					    					else:
					    						imageTest[0]['src']='http://'+domain+imagesrc
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0]['src']+'"/>'

					    					return image
					    				else:
					    					imageTest[0]['src']='https://'+domain+'/'+imagesrc
					    					if validateURL(imageTest[0]['src']):
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0]['src']+'"/>'
					    						
					    					else:
					    						imageTest[0]['src']='http://'+domain+'/'+imagesrc
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0]['src']+'"/>'

					    					return image
					    		except:
					    			pass
				    		else:
				    			try:
					    			if(imageTest[0].find('img')!=-1):
					    				imagesrc=imageTest[0].img['src']
					    				if validateURL(imagesrc):
					    					image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
					    					return image
					    			else:
					    				if imagesrc.startswith('/'):
					    					imageTest[0].img['src']='https://'+domain+imagesrc
					    					if validateURL(imageTest[0].img['src']):
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0].img['src']+'"/>'
					    						
					    					else:
					    						imageTest[0].img['src']='http://'+domain+imagesrc
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0].img['src']+'"/>'

					    					return image

					    				else:
					    					imageTest[0].img['src']='https://'+domain+'/'+imagesrc
					    					if validateURL(imageTest[0].img['src']):
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0].img['src']+'"/>'
					    						
					    					else:
					    						imageTest[0].img['src']='http://'+domain+'/'+imagesrc
					    						image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0].img['src']+'"/>'

					    					return image

					    		except:
					    			pass
					 	
				except NameError:
				    Nochange = None	
		try:
			image=htmlContent.find(itemprop='image')
			if image:
				try:
					print('image from itemprop')
					imagesrc=image['src']
					print(imagesrc)
					if imagesrc.find(domain)!=-1:
						return image
					elif validateURL(imagesrc):
						return image
					
					elif imagesrc.startswith('//'):
						imagesrc=imagesrc.replace('//','',1)
						if validateURL(imagesrc):
							image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
							return image

					else:
						if imagesrc.startswith('/'):
							imagesrc='https://'+domain+imagesrc
							if validateURL(imagesrc):
								image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
								return image
							else:
								imagesrc='http://'+domain+imagesrc
								if validateURL(imagesrc):
									image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
						elif imagesrc.startswith('../'):
							imagesrc=imagesrc.replace('.','',2)
							imagesrc='https://'+domain+imagesrc
							print(imagesrc)
							if validateURL(imagesrc):
								image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
								return image
							else:
								imagesrc=image['src']
								imagesrc=imagesrc.replace('.','',2)
								imagesrc='http://'+domain+imagesrc
								print(imagesrc)
								if validateURL(imagesrc):
									image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'

						else:
							imagesrc='https://'+domain+'/'+imagesrc
							if validateURL(imagesrc):
								image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
								return image
							else:
								imagesrc='http://'+domain+'/'+imagesrc
								if validateURL(imagesrc):
									image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
									return image
				except:
					pass
		except:
			pass
		if not image:
			image='<img class="maxWidth600" src="/static/images/no-image.jpg"/>'	
		return image	


	#get page html
	
	parsed_uri = urlparse(request.GET['url'])
	domain = '{uri.netloc}'.format(uri=parsed_uri)
	htmlContent = BeautifulSoup(r.content, 'html.parser')
	
	currencies=getAllCurrencies(currenciesSource)
	# kill all script and style elements
	#for script in htmlContent(["script", "style", "function"]):
	 #   script.extract()    # rip it out
	
	'''
	#script for automatic testing of a list of websites
	#results will be saved in test.xlsx file in the project folder
	prices=[]
	images=[]
	urls=[]
	xy=0
	arrayIDs=getArrayIDs()		
	arrayClasses=getArrayClasses()
	htmlContent=None
	csvFileNotExist4=os.path.abspath(os.path.dirname(__file__))+'/../static/testList.csv'			
	with open(csvFileNotExist4) as common4:
		readerCommon4 = csv.reader(common4, delimiter=',')
		for itemRow in readerCommon4:

			url=itemRow[0]
			try:
				data = urlopen(url)
				soup = BeautifulSoup(data, 'html.parser')
				htmlContent=soup
				result = htmlContent.find('title')
				name=getTitle()
				image=getImage()
				productDescription=getDescription()
				review=getReviews()
				price=getPrice()
				url=itemRow[0]
				prices.append(price)
				images.append(image)
				urls.append(url)
				xy+=1
			except:
				pass
			
			
		print('total scrapped')
		print(xy)	
		df=DataFrame({'URL': urls, 'Prices':prices, 'Images': images})
		df.to_excel('test.xlsx',sheet_name='sheet1',index=False)
				
	'''
	#static scrapping from dataset
	csvFile=os.path.abspath(os.path.dirname(__file__))+'/../static/scrapping_dataset.csv'
	with open(csvFile) as f:
		reader = csv.reader(f, delimiter=',')
		domainExists='false'
		for row in reader:
			
			# 0 for image 1 for name 2 is price 3 is review 4 is description 5 is domain
			if(row[5]==domain):
				domainExists = 'true';
				for script in htmlContent(["script", "style", "function"]):
					script.extract()    # rip it out
				image=htmlContent.select(row[0])
				#print(image)
				name = htmlContent.select(row[1]) if (row[1]!='') else ''
				price=htmlContent.select(row[2]) if (row[2]!='') else ''
				review=htmlContent.select(row[3]) if (row[3]!='') else ''
				productDescription=htmlContent.select(row[4]) if (row[4]!='') else ''
				print('from static-scrapping')

#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
		# If Domain is not in the dataset
		#dynamic scrapping
		if(domainExists!='true'):
			
			#get all ids.
			arrayIDs=getArrayIDs()
			
			#get all classes
			arrayClasses=getArrayClasses()
			name=getTitle()
			image=getImage()
			productDescription=getDescription()
			review=getReviews()
			price=getPrice()

			
	return {'request':request,'images':image,'name':name,'price':price,'description':productDescription,'review':review}



