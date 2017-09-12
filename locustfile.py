from locust import HttpLocust, TaskSet, task
import string,random
from bs4 import BeautifulSoup
import requests,lxml,random,string
from datetime import datetime
import base64


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class WebsiteTasks(TaskSet):
	
	def on_start(self):
		self.mark()

	@task
	def hi(self):
		pass

	def mark(self):
		url = 'http://coe1.annauniv.edu/home/'
		post_url = 'http://coe1.annauniv.edu/home/students_corner.php'
		reg_no = '312415205014'
		dob =  '09-04-1997'

		s=requests.Session()

		r = s.get(url)

		ti = datetime.now()

		soup = BeautifulSoup(r.content,'lxml')
		a = soup.find_all('input',type = 'hidden')
		# print a
		hidden = a[2]['value']
		a = soup.find_all('img')
		image_data = a[8]['src']

		image_name = id_generator()	

		convert = base64.b64decode(image_data[22:])

		t = open(image_name+".png", "wb+")
		t.write(convert)
		t.close()

		print ti

		capcha = raw_input('enter capcha '+ image_name + ' : ')

		data = {
			 hidden : hidden,
			'register_no': reg_no,
			'dob': dob,
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
		
		out = open("a.txt","w")
		out.write(r.content)
		out.close()

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 2*1000
    max_wait = 4000