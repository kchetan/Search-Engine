import xml.sax,re,nltk,sys,os,shelve
import commands
from nltk.tokenize import regexp_tokenize

def create_index():
	global lines_count,index_level
	index_level=[]
	v1=int((lines_count)**(1/3.0))+1
	v2=v1**2
	f1=open(sys.argv[1],'r')
	count=0
	fname=0
	word=''
	arr1=[]
	for line in f1:
		if count%v2==0:
			if len(arr1)>0:
				index_level.append(arr1)
			arr1=[]
		if count%v1==0:
			fname+=1
			f2=open('./Index/'+str(fname),'w')
			word=line.split()[0]
			arr1.append([word,str(fname)])
			f2.write(line)
		else:
			f2.write(line)
		count+=1
	if len(arr1)>0:
		index_level.append(arr1)

def store_shelve():
	global stopwords,dict_posting,min_id,lines_count,index_level
	#d=shelve.open('./src/vars')
	#d['index_level']=index_level
	#d.close()
	f1=open('./Index/S_index.txt','w')
	final=''
	for i in index_level:
		st=''
		for j in i:
			st+=j[0]+','+j[1]+'|'
		f1.write(st[:-1]+'\n')
	f1.close()

def shelve_retrieve():
	#d=shelve.open('./src/vars')
	global stopwords,index,lines_count
	#stopwords=d['stopwords']
	#lines_count=d['lines_count']
	f1=open('./src/lines_count.txt','r')
	lines_count=int(f1.read())
	f1.close()
	#min_id=d['min_id']
	#a=commands.getstatusoutput('wc -l '+sys.argv[1])[1]
	#lines_count=a.split()[0]
	#d.close()	


if __name__ == "__main__":
	shelve_retrieve()
	create_index()	
	store_shelve()
