#!/usr/bin/python
import shelve,nltk,os,sys,re,math,operator
from nltk.tokenize import regexp_tokenize

def search_doc(file1,word,field):
	global doc_rank,documents
	f=open('./Index/'+file1)
	st=''
	for line in f:
		a=line.split()
		if a[0]==word:
			st=a[1]
			break
		elif a[0]>word:
			return ''
	s=st.split('|')
	n=0
	for st in s:
		if field=='-':
			n=st.count('|')+1
		else:
			if st.find(field)>=0:
				n+=1
	for st in s:
		val=0
		doc=st.split('z')
		if len(doc)==1:
			cat=0
		else:
			cat=int(doc[1])
			if field=='z':
				val+=cat*30
			elif field=='-':
				val+=cat*10
		doc=doc[0]
		doc=doc.split('l')
		if len(doc)==1:
			link=0
		else:
			link=int(doc[1])
			if field=='l':
				val+=link*30
			elif field=='-':
				val+=link*10
		doc=doc[0]
		doc=doc.split('r')
		if len(doc)==1:
			ref=0
		else:
			ref=int(doc[1])
			if field=='r':
				val+=ref*30
			elif field=='-':
				val+=ref*10
		doc=doc[0]
		doc=doc.split('y')
		if len(doc)==1:
			body=0
		else:
			body=int(doc[1])
			if field=='y':
				val+=body*20
			elif field=='-':
				val+=body*5
		doc=doc[0]
		doc=doc.split('i')
		if len(doc)==1:
			info=0
		else:
			info=int(doc[1])
			if field=='i':
				val+=info*30
			elif field=='-':
				val+=info*10
		doc=doc[0]
		doc=doc.split('t')
		if len(doc)==1:
			title=0
		else:
			title=int(doc[1])
			if field=='t':
				val+=title*150
			elif field=='-':
				val+=title*40
		doc=int(doc[0],16)
		if n!=0:
			val=val*math.log(documents*1.0/n)
		try:
			doc_rank[doc]+=val
		except:
			doc_rank[doc]=val
		#print doc,title,info,body,link,ref,cat
		

def search_index(word,field):
	global stopwords,index,min_id,files_count,lines_count
	#word=stemmer.stem(word)
	arr=[]
	l=len(index)
	for i in range(l):
		if (i==l-1) or (i!=l-1 and index[i][0][0]<=word and index[i+1][0][0]>=word):
			#print 'came',i
			flag=0
			for j in range(1,len(index[i])):
				if index[i][j][0]==word:
					return search_doc(index[i][j][1],word,field)
					#print index[i][j][1],'$$'
					flag=1
					break
				elif index[i][j][0]>word:
					j=j-1
					return search_doc(index[i][j][1],word,field)
					#print index[i][j][1],'##'
					flag=1
					break
			if flag==0:
				return search_doc(index[i][j][1],word,field)
				#print index[i][j][1],'****'
			break


def search_Tindex(word):
	global stopwords,Tindex,min_id,files_count,lines_count
	#word=stemmer.stem(word)
	arr=[]
	l=len(Tindex)
	for i in range(l):
		if (i==l-1) or (i!=l-1 and int(Tindex[i][0][0])<=word and int(Tindex[i+1][0][0])>=word):
			#print 'came',i
			flag=0
			for j in range(1,len(Tindex[i])):
				if int(Tindex[i][j][0])==word:
					return search_Tdoc(Tindex[i][j][1],word)
					#print Tindex[i][j][1],'$$'
					flag=1
					break
				elif int(Tindex[i][j][0])>word:
					j=j-1
					return search_Tdoc(Tindex[i][j][1],word)
					#print Tindex[i][j][1],'##'
					flag=1
					break
			if flag==0:
				return search_Tdoc(Tindex[i][j][1],word)
				#print index[i][j][1],'****'
			break

def search_Tdoc(file1,word):
	global doc_rank,documents
	f=open('./Tindex/T'+file1)
	st=''
	for line in f:
		a=line.split()
		if int(a[0])==word:
			st=' '.join(a[1:])
			return st
		elif int(a[0])>word:
			return ''

def shelve_retrive():
	#d=shelve.open('./src/vars')
	global stopwords,index,min_id,files_count,lines_count,documents,Tindex
	stopwords={}
	#stopwords=d['stopwords']
	#index=d['index_level']
	#min_id=d['min_id']
	#lines_count=d['lines_count']
	#documents=d['documents']
	f1=open('./src/stoplist.txt','r')
	for i in f1:
		if i!='\n':
			stopwords[i[:-1]]=1
	f1.close()
	f1=open('./src/min_id.txt','r')
	min_id=int(f1.read())
	f1.close()
	f1=open('./src/documents.txt','r')
	documents=int(f1.read())
	f1.close()
	f1=open('./src/lines_count.txt','r')
	lines_count=int(f1.read())
	f1.close()
	f1=open('./Index/S_index.txt','r')
	index=[]
	for line in f1:
		arr=[]
		line=line[:-1]
		line=line.split('|')
		for i in line:
			arr.append(i.split(','))
		index.append(arr)
	#print index
	f1.close()
	
	f1=open('./Tindex/S_Tindex.txt','r')
	Tindex=[]
	for line in f1:
		arr=[]
		line=line[:-1]
		line=line.split('|')
		for i in line:
			arr.append(i.split(','))
		Tindex.append(arr)
	#print index
	f1.close()
	

if __name__ == "__main__":
	shelve_retrive()
	global stopwords,doc_rank,min_id
	#search_index('backbon')
	n=input()
	stemmer = nltk.stem.porter.PorterStemmer()
	for i in range(n):
		doc_title={}
		doc_rank={}
		text=raw_input()
		text=text.lower()
		text=text.split()
		tokens=[]
		for i in text:
			if len(i)>2 and i[1]==':':
				a=i.split(':')
				try:
					if stopwords[a[1]]:
						continue
				except:
					tokens.append([stemmer.stem(a[1]),a[0]])
			else:
				try:
					if stopwords[i]:
						continue
				except:
					tokens.append([stemmer.stem(i),'-'])
			search_index(tokens[-1][0],tokens[-1][1])
		s_doc = sorted(doc_rank.items(), key=operator.itemgetter(1))
		l=min(10,len(doc_rank))
		length=len(doc_rank)
		#print s_doc
		for i in range(l):
			val=s_doc[length-i-1][0]
			print search_Tindex(val+min_id)

		#for i in range(l):
		#	print s_doc[length-i-1][0]+min_id

