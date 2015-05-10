import os
import datetime
import urllib2

#Script polling IP cameras for current still frame and storing them on filesystem.
#Polling is done every minute. Timeout for every transaction is fixed(10 seconds).
#If transaction timeout/error occurs, corresponding message is printed to console
#and next URL from configuration is processed

#Script processing sequence:
#1. reads configuration from file "config" 
#    each line has format: URL_of_file_for_periodic_recording \t DIRECTORY_to_store_recorded_files
#2. creates directories(if not already existing) listed in configuration
#3. periodically polls files from configration and stores them in their respective directories
#    filename format is: img_YYYY-MM-DD_HH-MM-SS.jpg

print "Reading configuration file:"
configuration = []
config_file = open('config', 'r')
for line in config_file:
	config_list = line.rstrip('\r\n').split("	")
	configuration.append({"URL":config_list[0], "directory":config_list[1]})

for webcam in configuration:
	print webcam['URL'], webcam['directory']
	if not os.path.exists(webcam['directory']):
		os.makedirs(webcam['directory'])

print "RECORDING STARTED: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
while 1:
	minute=datetime.datetime.now().minute
	for webcam in configuration:
		try: response = urllib2.urlopen(webcam['URL'],timeout=10)
		except urllib2.HTTPError, e:
			print datetime.datetime.now().strftime("%m-%d %H:%M:%S   ")+webcam['URL']+" "+str(e.code)
		except urllib2.URLError, e:
			print datetime.datetime.now().strftime("%m-%d %H:%M:%S   ")+webcam['URL']+" "+str(e.reason)
		except:
			print datetime.datetime.now().strftime("%m-%d %H:%M:%S   ")+webcam['URL']+" SOME OTHER ERROR"
		else:
			try: downloaded_file = response.read()
			except:
				print datetime.datetime.now().strftime("%m-%d %H:%M:%S   ")+webcam['URL']+" SOCKET READ ERROR"
			else:
				image_out = open(os.path.join(webcam['directory'], "img_"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".jpg"), 'wb')
				image_out.write(downloaded_file)
				image_out.close()
	while datetime.datetime.now().minute==minute:
		pass
