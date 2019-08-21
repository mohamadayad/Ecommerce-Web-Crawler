from django.db import models
import os,time
from urllib.parse import urlparse
import csv
import re

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

def itemprop(key):
	return htmlContent.find(itemprop=key)

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
    return any(char.isdigit() for char in inputString)

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
	currenciesSource='/../static/currencies.csv'
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

	#get page html
	parsed_uri = urlparse(request.GET['url'])
	domain = '{uri.netloc}'.format(uri=parsed_uri)
	htmlContent = BeautifulSoup(r.content, 'html.parser')
	currencies=getAllCurrencies(currenciesSource)

	# kill all script and style elements
	for script in htmlContent(["script", "style", "function"]):
	    script.extract()    # rip it out
	

	# get text
	text = htmlContent.get_text()
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)

	
	parag=htmlContent.find_all('p')
	ayrebomak=''
	for a in parag:
		ayrebomak+=a.text
	

	#get all ids.
	arrayIDs=getArrayIDs()
	#get all classes
	arrayClasses=getArrayClasses()
	
	#static scrapping from dataset
	csvFile=os.path.abspath(os.path.dirname(__file__))+'/../static/scrapping_dataset.csv'
	with open(csvFile) as f:
		reader = csv.reader(f, delimiter=',')
		domainExists='false'
		for row in reader:
			# 0 for image 1 for name 2 is price 3 is review 4 is description 5 is domain
			#print(domain)
			if(row[5]==domain):
				domainExists = 'true';
				image=htmlContent.select(row[0]) if (row[0]!='') else ''
				name = htmlContent.select(row[1]) if (row[1]!='') else ''
				price=htmlContent.select(row[2]) if (row[2]!='') else ''
				review=htmlContent.select(row[3]) if (row[3]!='') else ''
				productDescription=htmlContent.select(row[4]) if (row[4]!='') else ''
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
		# If Domain is not mentioned on the dataset
		#dynamic scrapping using dictionaries
		if(domainExists!='true'):
			#get name and image using meta-data
			name=htmlContent.select('h1') if(htmlContent.select('h1')) else ''
			imageurl = htmlContent.find('meta', attrs={'property': 'og:image', 'content': True})
			imagenameUrl = htmlContent.find('meta', attrs={'name': 'og:image', 'content': True})
			if imageurl:
				src=imageurl['content']
				print(src)
				if src.find('http')!=-1:
					image = '<img class="maxWidth600" alt="cannot get image" src="'+src+'"/>'
					print('omak')

				else:
					if src.startswith('/'):
						image = '<img class="maxWidth600" alt="cannot get image" src="'+'https://'+domain+src+'"/>'
					else:
						image = '<img class="maxWidth600" alt="cannot get image" src="'+'https://'+domain+'/'+src+'"/>'
					
			elif imagenameUrl:
				image = '<img class="maxWidth600" src="'+imagenameUrl['content']+'"/>'
				print('e5tak')
			else:
			    #image='<img class="maxWidth600" src="/static/images/no-image.jpg"/>'
			    image=''
			#look for patterns from dictionary to get price    
			csvFileNotExist=os.path.abspath(os.path.dirname(__file__))+'/../static/priceDictionary.csv'			
			with open(csvFileNotExist) as common:
				readerCommon = csv.reader(common, delimiter=',')
				price=''
				review=''
				productDescription=''
				for itemRow in readerCommon:
					# 0 for price
					try:
					    priceTest=htmlContent.select(itemRow[0])
					    if priceTest:
					    	if(checkEqual(priceTest)):
					    		price=priceTest[0].text
					    	else:
					    		price=priceTest
					   
					except NameError:
					    Nochange = None

			#if no meta-data look for patterns from dictionary to get @Image.
			csvFileNotExist1=os.path.abspath(os.path.dirname(__file__))+ImageDictionary			
			with open(csvFileNotExist1) as common1:
				readerCommon1 = csv.reader(common1, delimiter=',')
				for itemRow in readerCommon1:
					# 0 for price
					try:
					    
					    if(image==''):
					    	imageTest=htmlContent.select(itemRow[0])
					    	if(imageTest):
					    		#imageTest[0].img['src']='omak b ayre'
					    		tagname=imageTest[0].name
					    		
					    		if tagname=='img':
					    			imagesrc=imageTest[0]['src']
					    			if imagesrc.find('http')!=-1:
					    				image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
					    				print('11111111')
					    			else:
					    				if imagesrc.startswith('/'):
					    					imageTest[0]['src']='https://'+domain+imagesrc
					    					image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0]['src']+'"/>'
					    					print('4444444')
					    				else:
					    					imageTest[0]['src']='https://'+domain+'/'+imagesrc
					    					image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0]['src']+'"/>'
					    					print('33333333')
					    		else:
					    			if(imageTest[0].find('img')!=-1):
					    				imagesrc=imageTest[0].img['src']
					    				if imagesrc.find('http')!=-1:
					    					image='<img class="maxWidth600" alt="Cannot get image" src="'+imagesrc+'"/>'
					    					print('22222222')
					    				else:
						    				if imagesrc.startswith('/'):
						    					imageTest[0].img['src']='https://'+domain+imagesrc
						    					image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0].img['src']+'"/>'
						    					print('11111111')
						    				else:
						    					imageTest[0].img['src']='https://'+domain+'/'+imagesrc
						    					image='<img class="maxWidth600" alt="Cannot get image" src="'+imageTest[0].img['src']+'"/>'
						    					print('00000000')
						 	
					except NameError:
					    Nochange = None
			
			#if no meta-data look for patterns from dictionary to get @Description.
			
			csvFileNotExist3=os.path.abspath(os.path.dirname(__file__))+descriptionDictionary		
			with open(csvFileNotExist3) as common3:
				readerCommon3 = csv.reader(common3, delimiter=',')
				for itemRow in readerCommon3:
					# 0 for price
					try:
					    
					    if(productDescription==''):
					    	descriptionTest=htmlContent.select(itemRow[0])
					    	#print(descriptionTest)
					    	if(descriptionTest):
					    		productDescription=descriptionTest
					    		#print(productDescription)
					    		#print('ayreeeeeee')
					    		
					except NameError:
					    Nochange = None
			
			#if no meta-data look for patterns from dictionary to get Recommendation.
			csvFileNotExist4=os.path.abspath(os.path.dirname(__file__))+recommendationDictionary			
			with open(csvFileNotExist4) as common4:
				readerCommon4 = csv.reader(common4, delimiter=',')
				for itemRow in readerCommon4:
					# 0 for price
					try:
					    
					    if(review==''):
					    	reviewTest=htmlContent.select(itemRow[0])
					    	if(reviewTest):
					    		review=reviewTest
					    		
					except NameError:
					    Nochange = None
	price=''
	if not price:
		#get matched ids
		matchedPriceIDs=filterArray(arrayIDs,priceIDsSource)
		#get all classes.
		matchedPriceClasses=filterArray(arrayClasses,priceIDsSource)
		
		print('matched price classsessss')
		#print(matchedPriceClasses)
		if not price:
			found=False
			if (len(matchedPriceClasses)>0):
				for i in range(len(matchedPriceClasses)):
					checkedprice=htmlContent.find(class_=matchedPriceClasses[i])
					if checkedprice is None:
						pass
					else:
						for currency in currencies:
							if hasNumbers(checkedprice.text) and checkedprice.text.find(currency)!=-1:
								
								price=checkedprice.text+"bbbb"
								found=True
								break
							if (found):
								break
		
		if not price:
			if(len(matchedPriceIDs)>0):
				myprice=[]
				for i in range(len(matchedPriceIDs)):
					checkedprice=htmlContent.find(id=matchedPriceIDs[i])
					if checkedprice is None:
						pass
					else:
						for currency in currencies:
							if hasNumbers(checkedprice.text) and checkedprice.text.find(currency)!=-1:
								prc=checkedprice.text.replace('\n','')
								myprice.append(prc)
				if  myprice:
					myprice=removeDuplicates(myprice)
					for i in myprice:
						price+=i
					price+='aaaa'
				price+=myprice[0]+'ottaa'
	productDescription=''
	if not productDescription:
		'''
		alltext = htmlContent.find_all('p')
		for i in alltext:
			print(i.text)
		'''
		desc=''
		matchedDescriptionIDs=filterArray(arrayIDs,descriptionIDsSource)
		matchedDescriptionClasses=filterArray(arrayClasses,descriptionIDsSource)
		if len(matchedDescriptionIDs)>0:
			for i in range(len(matchedDescriptionIDs)):
				desc=htmlContent.find(id=matchedDescriptionIDs[i])
				print(matchedDescriptionIDs)
				if desc is not None:
					#if desc.text.find('Description'):
					productDescription=desc
					print(matchedDescriptionIDs[i])
					print('desssssssssssssssssssssssssssssss 00000000000000000000000')
					print(productDescription)
					break
		elif len(matchedDescriptionClasses)>0:
			for i in range(len(matchedDescriptionClasses)):
				desc=htmlContent.find(class_=matchedDescriptionClasses[i])
				print(matchedDescriptionClasses)
				if desc is not None:
					if len(desc.text)>10:
						productDescription=desc
						break
		'''
		else:
			desc=htmlContent.find(itemprop='description')
			productDescription=desc
			print('desssssssssssssssssssssssssssssss 111111111111111111111')
			print(productDescription)
		'''
	#price=htmlContent.find(id=matchedIDs[5])
	#print(price)	
	#print(image)
	
	#price=htmlContent.find(itemprop='price')
	#price=price.text

	#image=htmlContent.find(itemprop='image')
	productDescription=ayrebomak
	productDescription=itemprop(description)
	#desc=htmlContent.find(itemprop='description')
	#productDescription=desc.text
	#image=htmlContent.find(itemprop='image')
	#image['src']='https://'+domain+'/'+image['src']
	#image='<img class="maxWidth600" alt="Cannot get image" src="'+image['src']+'"/>'
	price='<p>"'+price+'"</p>'
	if not name:
		name=htmlContent.title.string
	if image=='':
		image='<img class="maxWidth600" src="/static/images/no-image.jpg"/>'
	return {'request':request,'images':image,'name':name,'price':price,'description':productDescription,'review':review}


	#print(htmlContent.title.string)
	#print("bizzaaa")
	#print(htmlContent.a.parent.name)
	#htmlContent.find_all('h2')[0:5]
	#h2test=htmlContent.find('h2')
	#print(h2test.parent.parent)

	'''
			description=htmlContent.find('meta', attrs={'name': 'Description', 'content': True})
			descriptionUrl=htmlContent.find('meta', attrs={'property': 'Description', 'content': True})
			if description:
				print(description['content'])
				productDescription=description['content']
			elif descriptionUrl:
				productDescription=descriptionUrl['content']
			else:
				description=''
	'''
	#texts = htmlContent.findAll(text=True)
		#visible_texts = filter(visible, texts)
		#print(visible_texts)
		#-----not used------
		#print (tag.get('class'))
		#print(tag.get('id'))
		#print (tag.text)
		
		#lista=['aaa']
		#lista.append('bbb')
		#lista.append(1)
		#print(lista)
		
		#test=htmlContent.find_all(class_="clearfix")
		#print(test)
		#test=htmlContent.find(id='lasche-geschenk')
		#print(test.text)
		#print('aaa')
		#print(test.text)

