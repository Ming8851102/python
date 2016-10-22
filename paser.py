import os
import util
import requests
import urllib2
import json

#OS_List=["Mac10.11","Win7x64-C2","GalaxyTab2-And41"]
#Browser_List=["Safari9","IE10","MblChrome38"]
Browser_List=["Chrome53","Chrome52","Chrome51","Chrome50","Chrome47","Chrome45","Chrome43","Chrome36","FF48","FF47","IE11","IE10","IE9","IE8","Safari10","Android5.0","Android4.4","Android4.2","Android4.1","MblChrome52","MblChrome51","MblChrome48","MblChrome47","MblChrome44","MblFF48","MblFF47","MblFF44","MblFF40","MblSafari9.0","MblSafari8.0","MblSafari7.0","MblSafari6.0"]
cur_Browser=""
cur_OS=""
cur_Resolutions=""
cur_Platform=""
def getExePath():
	return os.path.dirname( os.path.realpath( __file__ ) )
	
def fileExist(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	
def restgetmethod(link):
	responserequest= urllib2.Request(link)
	response = urllib2.urlopen(responserequest, timeout=120) #1610 60->120
	data = json.loads(response.read())
	return data
#filePath=os.path.join(os.path.sep, getExePath(), "BrowserList") 
#fileExist(filePath)

def get_info(json_data,index):
	print "start paser No:"+str(index)
    
	count=0

	pc_count=0
	phone_count=0
	tablet_count=0
	other_count=0

	global cur_Browser
	global cur_OS
	global cur_Resolutions
	global cur_Platform
	while(len(json_data) > count):

		if json_data[count]['device_type'] == "tablet":
			tablet_count+=1
			i=0
			while(len(json_data[count]['browsers']) > i):
				if json_data[count]['browsers'][i]['api_name'] == Browser_List[index]:
					#print "got:"+Browser_List[index]
					#print json_data[count]['browsers'][i]['default_config']
					#print json_data[count]['resolutions'][0]['name']
					#print "======================================="
					cur_Platform=json_data[count]['device']
					cur_Browser=Browser_List[index]
					cur_OS=json_data[count]['browsers'][i]['default_config']
					cur_Resolutions=json_data[count]['resolutions'][len(json_data[count]['resolutions'])-1]['name']
					return 1
				i+=1
		elif json_data[count]['device_type'] == "phone":
			phone_count+=1
			i=0
			while(len(json_data[count]['browsers']) > i):
				if json_data[count]['browsers'][i]['api_name'] == Browser_List[index]:
					#print "got:"+Browser_List[index]
					#print json_data[count]['browsers'][i]['default_config']
					#print json_data[count]['resolutions'][0]['name']
					#print "======================================="
					cur_Platform=json_data[count]['device']
					cur_Browser=Browser_List[index]
					cur_OS=json_data[count]['browsers'][i]['default_config']
					cur_Resolutions=json_data[count]['resolutions'][len(json_data[count]['resolutions'])-1]['name']
					return 1
				i+=1
		elif json_data[count]['device'] == "desktop":
			pc_count+=1

			#print len(json_data[count]['browsers'])
			i=0
			while(len(json_data[count]['browsers']) > i):
				if json_data[count]['browsers'][i]['api_name'] == Browser_List[index]:
					#print "got:"+Browser_List[index]
					#print json_data[count]['browsers'][i]['default_config']
					#print json_data[count]['resolutions'][0]['name']
					#print "======================================="
					cur_Platform=json_data[count]['device']
					cur_Browser=Browser_List[index]
					cur_OS=json_data[count]['browsers'][i]['default_config']
					cur_Resolutions=json_data[count]['resolutions'][len(json_data[count]['resolutions'])-1]['name']
					return 1
				i+=1
		else:	
			other_count+=1

		count+=1

	#print "Not found======================================="
	return 0

filePath=os.path.join(os.path.sep, getExePath(), "BrowserList") 
fileExist(filePath)
json_data=restgetmethod("https://crossbrowsertesting.com/api/v3/livetests/browsers")

i=0
while i<len(Browser_List):
	
	file = open('sample.py')

	if get_info(json_data,i) == 0:
		print "Fail got:"+Browser_List[index]
		print "======================================="
	else:	
		wFIle = open(os.path.join(os.path.sep, filePath, cur_Platform+"_"+cur_Browser+".py"), "w") 

		
		for line in file:

			if line.find("browser_api_name") != -1 :
				browserLine=line.replace("IE10",cur_Browser)
				wFIle.writelines(browserLine)
				#print cur_Browser 
				continue
				#print "find"

			if line.find("os_api_name") != -1 :
				osLine=line.replace("Win7x64-C2",cur_OS)
				wFIle.writelines(osLine)
				continue 
				#print "find"
			if line.find("screen_resolution") != -1 :
				osLine=line.replace("1024x768",cur_Resolutions)
				wFIle.writelines(osLine)
				continue 

			if line.find("aabbccdd") != -1 :
				osLine=line.replace("aabbccdd",cur_Platform+"_"+cur_Browser)
				wFIle.writelines(osLine)
				continue 
		
			wFIle.writelines(line) 
		 	
	wFIle.close()
	file.close()
	i=i+1