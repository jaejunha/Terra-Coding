import requests
import httplib
from bs4 import BeautifulSoup

def get_index(search):
    item_url = "localhost:9000"
    con = httplib.HTTPConnection(item_url)
    con.request("GET", "/","",{})
    text = con.getresponse().read()
    text = text[text.find('tbody'):text.find('/tbody')]
    href = ''
    for t in text.split('/tr'):
	if t.find(search)>=0:
		href = t[t.find('index/')+6:t.find('" title')]
		print href
    return href
	
def get_single_item_data(index):
    item_url = "http://localhost:9000/dashboard/index/"+str(index)
    source_code = requests.get(item_url)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text, "html.parser")
    data=[]
    for i in soup.findAll('div', {'id': 'dashboard-column-1'}):
        print('-------------block1-------------\n')
        for item_name in soup.findAll('div', {'id': 'block_1'}):
            issue_message=item_name.text
            print(issue_message)
	    text = issue_message.replace(' ','').replace('\n','')
	    text = text.replace('Linesofcode','')
	    text = text.replace('JavaFiles','/')
	    text = text.replace('Directories','/')
	    text = text.replace('Lines','/')
	    text = text.replace('Functions','/')
	    text = text.replace('Classes','/')
	    text = text.replace('Statements','/')
	    text = text.replace('Accessors','/')
	    for t in text.split('/'):
		data.append(t)
        print('-------------block3-------------\n')
        for item_name in soup.findAll('div', {'id': 'block_3'}):
            issue_message=item_name.text
            print(issue_message)
	    text = issue_message.replace('Complexity','')
            text = text.replace(' /function','/')
            text = text.replace(' /class','/')
            text = text.replace(' /file','/')
            text = text.split(' ')[0].replace(' ','').replace('\n','')
	    for t in text.split('/'):
		data.append(t)
            for photo in soup.findAll('img', {'id': 'chart_img_function_complexity_distribution'}):
                photo_src=photo.get('src')
               	print(photo_src)
		data.append(photo_src)
    print('-------------block6-------------\n')
    for i in soup.findAll('div', {'id': 'dashboard-column-2'}):
        for item_name in soup.findAll('div', {'id': 'block_6'}):
            issue_message=item_name.text
            print(issue_message)
	    text = issue_message.replace(' ','').replace('\n','')
	    text = text.replace('SQALERating','')
	    text = text.replace('TechnicalDebtRatio','/')
	    for t in text.split('/'):
		data.append(t)
		
	    for d in data:
		print d
    return data
get_single_item_data(get_index('testForFeedback'))
