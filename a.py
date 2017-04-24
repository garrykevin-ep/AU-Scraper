from bs4 import BeautifulSoup
import requests,lxml
import base64

url = 'http://coe1.annauniv.edu/home/'
post_url = 'http://coe1.annauniv.edu/home/students_corner.php'
s=requests.Session()

r = s.get(url)


soup = BeautifulSoup(r.content,'lxml')
a = soup.find_all('input',type = 'hidden')
hidden = a[2]['value']
a = soup.find_all('img')
image_data = a[8]['src']


convert = base64.b64decode(image_data[22:])

t = open("capcha.png", "wb+")
t.write(convert)
t.close()

capcha = raw_input('enter capcha : ')

data = {
	 hidden : hidden,
	'register_no': '',
	'dob': '',
	 'security_code_student' : capcha,
	 'gos' : 'Login',
}


r = s.post(post_url,data=data)

# print(r.content)

soup = BeautifulSoup(r.content,'lxml')
a = soup.find_all('input',type='hidden')

hidden = a[0]['value']

data = {
	hidden : hidden,
	'ExamResults' : '',
	'univ_reg_no' : '',
}

r = s.post(post_url,data = data)
print r.content