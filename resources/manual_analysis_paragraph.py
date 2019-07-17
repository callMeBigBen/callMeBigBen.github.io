import os

path ="/home/shawn/Desktop/ConfAnalysis/manuals/result/afterMerge/manual"
files = os.listdir(path)
apps = ["cinder","glance","nova","placement","neutron","keystone"]
'''
1. get conf list from Teng's work
2. define intra-component conf denpendency analysis
3. define inter-component conf dependency analysis. quite similar with 2.Just chagne the scope of pair conf
'''

def get_paras(lines):
	i = 0
	j = 0
	para = ""
	paras = []
	while j < len(lines):
		if lines[j]=="\n" or lines[j]=="" :
			if para <> "":
				paras.append(para)
				para = ""
				i = j+1
				j = j+1
			else:
				j= j+1
		else:
			para = para+lines[j][:-1]
			j = j+1
	# print(paras)
	if para <> "":
		paras.append(para)
	# for n in range(i,len(lines)):
	# 	para = para+lines[n][:-1]
	# 	paras.append(para)
	return paras
def get_app_list(app):
	f = open("ConfList/"+app,"r")
	content = f.read()
	params = content.split("##")
	return params
# currently just name. No section name
def intra_component_extraction(app):
	res = open("intra_component/paragraph/"+app+"_with_paragraph","w")
	result = []
	params = get_app_list(app)
	counter = 0
	situation2 = [0,0,0,0]
	for file in files:
		counter = counter+1
		f = open(path+"/"+file,"r")
		content = f.readlines()
		paras = get_paras(content)
		print(situation2,counter)
		for para in paras:
			para = para.replace("\n"," ")
			para_split = set(para.split())
			if para =="\n" or para=="" or len(para_split)<10:
				continue
			for index1 in range(1,len(params)):
				for index2 in range(index1+1,len(params)):
					# if index1==0 or index2 ==0:# do not know whether this will work
					# 	continue
					# if index1>=index2:
					# 	continue
					value1 = params[index1].split("**")
					value2 = params[index2].split("**")
					single1 = int(value1[-1][0])
					single2 = int(value2[-1][0])
					if single1 ==1 and single2 ==1:
						if value1[0] in para_split and value2[0] in para_split:
							situation2[0] = situation2[0]+1
							result.append(file +" " +value1[-2] +" " + value1[0] + " " + value2[-2] +" " + value2[0] +"\n") 
					elif single1 ==1 and single2 ==0:
						if value1[0] in para_split and value2[0] in para_split and value2[3] in para_split:
							situation2[1] = situation2[1]+1
							result.append(file +" " +value1[0] + " " + value2[-2] +" " + value2[0] +"\n") 
					elif single1 ==0 and single2 ==1:
						if value1[0] in para_split and value2[0] in para_split and value1[3] in para_split:
							situation2[2] = situation2[2]+1
							result.append(file +" " +value1[-2] +" " + value1[0] + " " + value2[0] +"\n")
					elif single1 ==0 and single2 ==0:
						if value1[0] in para_split and value2[0] in para_split and value2[3] in para_split and value1[3] in para_split:
							situation2[3] = situation2[3]+1
							result.append(file +" " +value1[0] + " " + value2[0] +"\n") 
						# print(situation)
						# print(para)
	result = list(set(result))
	for line in result:
		res.write(line)
	res.close()

def inter_component_extraction(app1,app2):
	res = open("inter_component/paragraph/"+app1+"_"+app2+"_with_paragraph","w")
	result = []
	params1 = get_app_list(app1)
	params2 = get_app_list(app1)
	counter = 0
	situation2 = [0,0,0,0]
	for file in files:
		counter = counter+1
		f = open(path+"/"+file,"r")
		content = f.readlines()
		paras = get_paras(content)
		print(situation2,counter)
		for para in paras:
			para = para.replace("\n"," ")
			para_split = set(para.split())
			if para =="\n" or para=="" or len(para_split)<10:
				continue
			for index1 in range(len(params1)):
				for index2 in range(len(params2)):
					if index1==0 or index2 ==0:
						continue
					value1 = params1[index1].split("**")
					value2 = params2[index2].split("**")
					single1 = int(value1[-1][0])
					single2 = int(value2[-1][0])
					if single1 ==1 and single2 ==1:
						if value1[0] in para_split and value2[0] in para_split:
							situation2[0] = situation2[0]+1
							result.append(file +" " +app1 +" "+app2 +" "+value1[-2] +" " + value1[0] + " " + value2[-2] +" " + value2[0] +"\n") 
					elif single1 ==1 and single2 ==0:
						if value1[0] in para_split and value2[0] in para_split and value2[3] in para_split:
							situation2[1] = situation2[1]+1
							result.append(file +" " +app1 +" "+app2 +" "+value1[0] + " " + value2[-2] +" " + value2[0] +"\n") 
					elif single1 ==0 and single2 ==1:
						if value1[0] in para_split and value2[0] in para_split and value1[3] in para_split:
							situation2[2] = situation2[2]+1
							result.append(file +" " +app1 +" "+app2 +" "+value1[-2] +" " + value1[0] + " " + value2[0] +"\n")
					elif single1 ==0 and single2 ==0:
						if value1[0] in para_split and value2[0] in para_split and value2[3] in para_split and value1[3] in para_split:
							situation2[3] = situation2[3]+1
							result.append(file +" " +app1 +" "+app2 +" "+value1[0] + " " + value2[0] +"\n") 
						# print(situation)
						# print(para)
	result = list(set(result))
	for line in result:
		res.write(line)
	res.close()
# intra_component_extraction("keystone")
# intra_component_extraction("placement")
# intra_component_extraction("neutron")
# intra_component_extraction("cinder")
# intra_component_extraction("nova")
# intra_component_extraction("glance")
# below is test code for para splitor
# f = open(path+"/cinder-latest-admin-blockstorage-backup-disks","r")
# f = open("test","r")
# content = f.readlines()
# paras = get_paras(content)
# for para in paras:
# 	print(para)