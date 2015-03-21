import xml.sax,re,nltk,sys,os,shelve
from nltk.tokenize import regexp_tokenize

def parser(title,id,text):
	global stopwords,dict_posting,min_id,files_count
	dict_all={}
	dict_body={}
	dict_reference={}
	dict_links={}
	dict_infobox={}
	dict_category={}
	dict_title={}
	text=text.lower()
	title=title.lower()
	infobox,cur,body=text.partition("'''")
	if body=='' or body==None:
		body=infobox
	body,cur,category=body.partition("[[category:")
	category=cur+category
	body,cur,links=body.partition("external links")
	body,cur,references=body.partition("references")
	tokens_infobox=regexp_tokenize(infobox, pattern='[a-zA-Z]+|(\d+\.?\d+)')
	categories=re.findall(r'\[\[category:(.*?)\]\]',category)
	tokens_category=[]
	for i in categories:
		a=regexp_tokenize(i,pattern='[A-Za-z]+|(\d+\.?\d+)')
		tokens_category+=a
	#tokens_category=regexp_tokenize(tokens_category, pattern='[A-Za-z0-9]+|(\d+\.?\d+)') '[A-Za-z]+|(\d+\.?\d+)'
	tokens_links=regexp_tokenize(links, pattern='[a-zA-Z]+|(\d+\.?\d+)')
	tokens_references=regexp_tokenize(references, pattern='[a-zA-Z]+|(\d+\.?\d+)')
	tokens_body=regexp_tokenize(body, pattern='[a-zA-Z]+|(\d+\.?\d+)')
	tokens_title=regexp_tokenize(title, pattern='\d+\.?\d+|[a-zA-Z]+')
	#print tokens_infobox
	#print tokens_body
	#print tokens_references
	#print tokens_links
	#print tokens_category
	stemmer = nltk.stem.porter.PorterStemmer()
	for i in tokens_title:
		temp=stemmer.stem(i)
		try:
			if stopwords[temp]:
				continue
		except:
			try:
				dict_title[temp]+=1
			except:
				dict_title[temp]=1
	for i in tokens_infobox:
		temp=stemmer.stem(i)
		try:
			if stopwords[temp]:
				continue
		except:
			try:
				dict_infobox[temp]+=1
			except:
				dict_infobox[temp]=1
	for i in tokens_body:
		temp=stemmer.stem(i)
		try:
			if stopwords[temp]:
				continue
		except:
			try:
				dict_body[temp]+=1
			except:
				dict_body[temp]=1
	for i in tokens_references:
		temp=stemmer.stem(i)
		try:
			if stopwords[temp]:
				continue
		except:
			try:
				dict_reference[temp]+=1
			except:
				dict_reference[temp]=1
	for i in tokens_links:
		temp=stemmer.stem(i)
		try:
			if stopwords[temp]:
				continue
		except:
			try:
				dict_links[temp]+=1
			except:
				dict_links[temp]=1
	for i in tokens_category:
		temp=stemmer.stem(i)
		try:
			if stopwords[temp]:
				continue
		except:
			try:
				dict_category[temp]+=1
			except:
				dict_category[temp]=1
	for i in dict_title:
		dict_all[i]='t'+str(dict_title[i])
	for i in dict_infobox:
		try:
			dict_all[i]+='i'+str(dict_infobox[i])
		except:
			dict_all[i]='i'+str(dict_infobox[i])
	for i in dict_body:
		try:
			dict_all[i]+='y'+str(dict_body[i])
		except:
			dict_all[i]='y'+str(dict_body[i])
	for i in dict_reference:
		try:
			dict_all[i]+='r'+str(dict_reference[i])
		except:
			dict_all[i]='r'+str(dict_reference[i])
	for i in dict_links:
		try:
			dict_all[i]+='l'+str(dict_links[i])
		except:
			dict_all[i]='l'+str(dict_links[i])
	for i in dict_category:
		try:
			dict_all[i]+='z'+str(dict_category[i])
		except:
			dict_all[i]='z'+str(dict_category[i])
	for i in dict_all:
		try:
			dict_posting[i]+='|'+hex(id-min_id)[2:]+dict_all[i]
		except:
			dict_posting[i]=hex(id-min_id)[2:]+dict_all[i]
	if sys.getsizeof(dict_posting)>1000000:###1 mb = 1000000 b
		#print 'dumpd ',files_count
		dump_dict()


def dump_dict():
	global dict_posting,files_count,lines_count
	f2=open('./Index/'+str(files_count),'w')
	files_count+=1
	keys=sorted(dict_posting)
	lines_count=0
	for i in keys:
		f2.write((i+' '+dict_posting[i]+'\n').encode('utf-8'))
		lines_count+=1
	f2.close()
	dict_posting={}


def merge_files(file1,file2,out_file):
    global lines_count
    with open(file1) as f1, open(file2) as f2:
	sources = [f1, f2]
        with open(out_file, "w") as dest:
            l1 = f1.next()
            s1 = l1.split()
            l2 = f2.next()
            s2 = l2.split()
	    lines_count=0
            while(1):
                if(s1[0] < s2[0]):
                    dest.write(l1)
		    lines_count+=1
                    try:
                        l1 = f1.next()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.next()
                                dest.write(t2)
		    		lines_count+=1
                            except:
                                break
                        break
                elif(s1[0] > s2[0]):
                    dest.write(l2)
		    lines_count+=1
                    try:
                        l2 = f2.next()
                        s2 = l2.split()
                    except:
                        while(1):
                            try:
                                t1 = f1.next()
                                dest.write(t1)
		    		lines_count+=1
                            except:
                                break
                        break
                else:
                    line = s1[0]+' ' + s1[1] +'|'+ s2[1]
                    dest.write(line + '\n')
		    lines_count+=1
                    try:
                        l1 = f1.next()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.next()
                                dest.write(t2)
		    		lines_count+=1
                            except:
                                break
                        break
                    try:
                        l2 = f2.next()
                        s2 = l2.split()
                    except:
                        dest.write(l1)
		    	lines_count+=1
                        while(1):
                            try:
                                t1 = f1.next()
                                dest.write(t1)
		    		lines_count+=1
                            except:
                                break
                        break

class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.type=None
		self.title=''
		self.text=''


class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.type=None
		self.title=''
		self.text=''
		self.id=''
		self.first=1
		
	def startElement(self, name, attrs):
		# print("startElement '" + name + "'")
		if "title"==name.lower():
			self.title=''
			self.text=''
			self.id=''
			self.type="title"
		elif "id"==name.lower():
			if self.first:
				self.type="id"
		elif "text"==name.lower():
			self.type="text"
			
	def endElement(self, name):
		global min_id,documents,fp
		#print("endElement '" + name + "'")
		if name=="title":
			self.type=None
			#print self.title
		elif name=="id" and self.first:
			documents+=1
			self.type=None
			self.first=0
			#print self.id
		elif name=="text":
			self.type=None
			#print self.text
			if min_id==None:
				min_id=int(self.id)
			fp.write((self.id+' '+self.title+'\n').encode('utf-8'))
			parser(self.title,int(self.id),self.text)
			self.first=1

	
	def characters(self, content):
		#print("characters '" + content + "'")
		if self.type=="title":
			self.title+=content
		elif self.type=="text":
			self.text+=content
		elif self.type=="id" and self.first:
			self.id+=content
		else:
			None

def merge_drive():
	global stopwords,dict_posting,min_id,files_count
	if len(dict_posting)>0:
		dump_dict()
	start=1
	if files_count>2:
		while(1):
			if start+2==files_count:
				val='index.txt'
			else:
				val=str(files_count)
		#	print 'merging',start,start+1,
			merge_files('./Index/'+str(start),'./Index/'+str(start+1),'./Index/'+val)
			os.remove('./Index/'+str(start))
			os.remove('./Index/'+str(start+1))
			start+=2
		#	print start,files_count
			if(start==files_count):
				files_count+=1
				break
			files_count+=1
	else:
		f1=open('./Index/index.txt','w')
		f2=open('./Index/1','r')
		f1.write(f2.read())
		f1.close()
		f2.close()
		os.remove('./Index/1')

def store_shelve():
	global stopwords,dict_posting,min_id,lines_count,documents
	#d=shelve.open('./src/vars')
	f1=open('./src/min_id.txt','w')
	f1.write(str(min_id))
	f1.close()
	f1=open('./src/documents.txt','w')
	f1.write(str(documents))
	f1.close()
	f1=open('./src/lines_count.txt','w')
	f1.write(str(lines_count))
	f1.close()
	#d['stopwords']=stopwords
	#d['min_id']=min_id
	#d['documents']=documents
	#d['lines_count']=lines_count
	#d.close()

def main(sourceFileName):
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())

if __name__ == "__main__":
	global stopwords,dict_posting,min_id,files_count,lines_count,documents,fp
	documents=0
	files_count=1
	dict_posting={}
	stopwords={}
	min_id=None
	fp=open('./Tindex/Titles.txt','w')
	f1=open('./src/stoplist.txt','r')
	for i in f1:
		if i!='\n':
			stopwords[i[:-1]]=1
	f1.close()
	main(sys.argv[1])
	fp.close()
	merge_drive()
	store_shelve()


