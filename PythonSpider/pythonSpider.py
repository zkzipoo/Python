# ---------------------------------------------
#	name: 		python spider
#	version:	0.1
#	author:		Kai
#	date:		11/03/2015
#	
# ---------------------------------------------

import string, urllib.request
import re, os
from fileinput import filename

# find all photos(jpg/gif) in specific website and page
def JandanPhoto(website_url,cur_page):

	photos = [];
	allPhotos = [];

	myJPGs = [];
	myMultiJPGs = [];
	myGIFs = [];

	myURL = website_url + str(cur_page) + "#comments";
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)';
	headers = { 'User-Agent' : user_agent };
	myRequest = urllib.request.Request(myURL, headers = headers);
	myResponse = urllib.request.urlopen(myRequest);
	myPage = myResponse.read();
	# decode to unicode
	unicodePage = myPage.decode("utf-8");

	# using regular expression to find photos
	# jpg regular expression
	jpgRegularExp = r'<a href=".*?">(.*?)</a></span><p><img src="(.*?)" />';
	jpgRE = re.compile(jpgRegularExp);
	myJPGs = re.findall(jpgRE, unicodePage);
	# print(myJPGs);

	# for several photos with same index
	multiJpgRE = r'<img src="(.*?)" />';
	multiRE = re.compile(multiJpgRE);
	myMultiJPGs = re.findall(multiRE, unicodePage);
	# print(myMultiJPGs);
	# jfiaeow();

	# gif regular expression
	gifRegularExp = r'<a href=".*?">(.*?)</a></span><p><img src=".*?" org_src="(.*?)" ';
	gifRE = re.compile(gifRegularExp);
	myGIFs = re.findall(gifRE, unicodePage);
	# print(myGIFs);


	photos.extend(myJPGs);
	photos.extend(myGIFs);
	allPhotos.extend(myMultiJPGs);

	# print(photos);
	# print(allPhotos);
	# print(len(photos))
	# print(len(allPhotos))
	return (photos, allPhotos)

# parse the content into filename
def parseFileName(os_dir,photos, allPhotos):
	if not os.path.exists(os_dir):
		os.makedirs(os_dir);

	for i in range(len(photos)):
		curNum = photos[i][0];
		curURL = photos[i][1];

		if i+1 < len(photos):
			nextURL = photos[i+1][1]; # next url in photos
			# find .jpg first
			if curURL.find('.jpg') > -1:
				curIndx = allPhotos.index(curURL); # first index of a series of photos 
				if nextURL.find('.gif') > -1: # last jpg in photos
					for j in range(len(allPhotos) - curIndx):
						filename = os_dir + curNum + "_" + str(j+1) + ".jpg";
						SavePhotos(allPhotos[curIndx+j],filename);
				else: # not lat jpg in photos
					nextIdx = allPhotos.index(nextURL); # several jpgs with same name 
					if nextIdx > curIndx+1:
						for j in range(nextIdx-curIndx):
							filename = os_dir + curNum + "_" + str(j+1) + ".jpg";
							SavePhotos(allPhotos[curIndx+j],filename);
					else: # there is only one photo of the same tag
						filename = os_dir + curNum + ".jpg";
						SavePhotos(curURL,filename);
			# find gif
			elif curURL.find('.gif') > -1:
				filename = os_dir + curNum + ".gif";
				SavePhotos(curURL,filename);
			else:
				print(photos[i]);
				wrong();

# save the photos to local folder			
def SavePhotos(itemURL,filename):
	if os.path.isfile(filename):
		print('Already downloaded !');
		pass
	else:
		try:
			print('Downloading: ' + itemURL );
			urllib.request.urlretrieve(itemURL, filename);
		except Exception as e:
			print('\tError in retrieving the URL:' + itemURL);
			raise e
			pass


#---------------------------------------#
os_dir = "E:\\不错小软件\\美图\\";
website_url = "http://jandan.net/ooxx/page-";
begin_page = 1332;
end_page = 1348;
for curPage in range(begin_page, end_page+1):
	(Photos, allPhotos) = JandanPhoto(website_url,curPage);
	parseFileName(os_dir,Photos, allPhotos);