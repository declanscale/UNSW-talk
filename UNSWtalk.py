#!/usr/bin/python3

# written by andrewt@cse.unsw.edu.au October 2017
# as a starting point for COMP[29]041 assignment 2
# https://cgi.cse.unsw.edu.au/~cs2041/assignments/UNSWtalk
#written by Daisong Yu (z5098539)

import os, glob, operator, datetime, re, collections,sys
from flask import Flask, render_template, session, request, redirect, url_for
from time import gmtime, strftime
import fileinput

students_dir = "static/dataset-medium";
student_detail_file = "static/dataset-medium"

app = Flask(__name__)

#this is a function to get the correct time formate and use to sort the post time
def key_function(item_dictionary):
    datetime_string = item_dictionary['time']
    return datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    
#this is a function to change the specific line in a file
def replaceAll(fileName,searchExp,replaceExp):
	for line in fileinput.input(fileName, inplace=1):
		if searchExp in line:
			line = line.replace(searchExp,replaceExp)
		sys.stdout.write(line)
    
    

@app.route('/', methods=['GET','POST'])
def start():
	return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():

	zid = request.form.get('zid', '')
	password = request.form.get('password', '')
	#zid = re.sub(r'\D', '', zid)

	# store zid in session cookie
	session['zid'] = zid
	
	user_path = os.path.join(students_dir,zid)
	
	if(os.path.isdir(user_path)!=True):
		zid_error = "Please check your zid ^^"
		return render_template('login.html', zid_error = zid_error)
	
	#print("user_path is:",user_path)
	details_path = os.path.join(user_path,"student.txt")#path of student.txt
	with open(details_path) as f:
		user_details = f.readlines()
	user_details_length = len(user_details)
	i = 0
	while(i < user_details_length):
		if 'password' in user_details[i]:
			password_line = user_details[i]
			real_password = password_line.replace('password: ','')
		i+=1
	real_password = real_password.rstrip()
	#print("real password is:",real_password)
	#print("entered password is:", password)
	
	if real_password == password:
		return redirect(url_for('user_profile'))
	else:
		password_error = "Please check your password ^^"
		return render_template('login.html',password_error=password_error)	
	
#	return render_template('login.html')
	
@app.route('/profile',methods=['GET','POST'])	
def user_profile():
	#print("enter user profile")
	
	#print("in session zid:",session['zid'])
	details_path = os.path.join(students_dir,session['zid'],"student.txt")
	#print("details_path is:",details_path)
	with open(details_path) as f:
		user_details = f.readlines()
		
	user_details_length = len(user_details)
	i = 0
	show_details = []#store the details that can be displayed
	while(i < user_details_length):
		if 'email' in user_details[i]:
			i+=1
		elif 'password' in user_details[i]:
			i+=1
		elif 'courses' in user_details[i]:
			i+=1
		elif 'latitude' in user_details[i]:
		    i+=1
		elif 'longitude' in user_details[i]:
		    i+=1
		else:
		    show_details.append(user_details[i])
		    i+=1
	show_details_str = ''.join(show_details)#change the list to string
	
	user_img_path = os.path.join(students_dir, session['zid'],"img.jpg")
	
	
	return render_template('profile.html',user_details=show_details_str,user_img = user_img_path)
	
	
@app.route('/post',methods=['GET','POST'])	
def user_post():
	#user_path = os.path.join(students_dir,session['zid'])
	
	self_post_list = []
	for self_post_path in glob.glob(os.path.join(students_dir, session['zid'], '*.txt')):
		#print(self_post_path)
		
		
		
		parts = self_post_path.split("/")
		#print(parts[3])
		if("-" not in parts[3] and "s" not in parts[3]):	
	
			with open(self_post_path) as f:
			   self_post_content = f.readlines()#read the self post line by line
			   str_of_post = ''.join(self_post_content)
			   self_post_list.append(str_of_post)
		   
	new_self_post_list = []# use to store each dict above
	
	for post in self_post_list: # each post here is a bunch of content which contain form, time...
		#print(post)
	
		post_info = { # each self post has a dict like this
		'from': '',
		'time': '',
		'message': '',
		'long': '',
		'lat': '',
	
		}
	
	
		post_parts = post.split("\n") #post_parts is a list contain the content of a post
		length_of_parts = len(post_parts)
		i = 0
		while i < length_of_parts:
			if 'from:' in post_parts[i]:
				post_info['from'] = post_parts[i]
			elif 'time:' in post_parts[i]:
				line = post_parts[i]
				new_line = line.replace('+0000','')
				new_line = new_line.replace('T',' ')
				post_info['time'] = new_line[6:]
		        
			elif 'message:' in post_parts[i]:
				post_info['message'] = post_parts[i]
			elif 'longitude:' in post_parts[i]:
				post_info['long'] = post_parts[i]
			elif 'latitude:' in post_parts[i]:
				post_info['lat'] = post_parts[i]
			i+=1
		
		new_self_post_list.append(post_info)	

	new_self_post_list.sort(key=key_function)
	new_self_post_list=new_self_post_list[::-1]
	
	return render_template('user_post.html',post_list=new_self_post_list)
	
	
@app.route('/friends',methods=['GET','POST'])	
def user_friends():
	details_path = os.path.join(students_dir,session['zid'],"student.txt")
	with open(details_path) as f:
		user_details = f.readlines()
	user_details_length = len(user_details)
	i = 0
	while i < user_details_length:
		if 'friends:' in user_details[i]:
			line = user_details[i]
			line = line.replace('friends: (','')
			line = line.replace(')','')
			line = line.replace('\n','')
			user_friends = line
		i+=1
		
	user_friends_list = user_friends.split(', ')
	friends_img_path_list = []
	
	for friend in user_friends_list:
		friend_img_path = os.path.join(students_dir, friend, "img.jpg")
		friends_img_path_list.append(friend_img_path)
	#print("img path list is:")
	#print(friends_img_path_list)

	return render_template('user_friends.html',friends_img_path_list = friends_img_path_list)


@app.route('/profile/friends/<string:cur_zid>',methods=['GET','POST'])
def friend_profile(cur_zid):

	zid = cur_zid
	#print("zid is:",zid)
	friend_details_path = os.path.join(students_dir,zid,"student.txt")
	
	with open(friend_details_path) as f:
		friend_details = f.readlines()
		
	friend_details_length = len(friend_details)
	i = 0
	show_details = []#store the details that can be displayed
	while(i < friend_details_length):
		if 'email' in friend_details[i]:
			i+=1
		elif 'password' in friend_details[i]:
			i+=1
		elif 'courses' in friend_details[i]:
			i+=1
		elif 'latitude' in friend_details[i]:
		    i+=1
		elif 'longitude' in friend_details[i]:
		    i+=1
		else:
		    show_details.append(friend_details[i])
		    i+=1
	show_details_str = ''.join(show_details)#change the list to string
	
	img_path = os.path.join("../..",students_dir, zid,"img.jpg")
	#print("zid:",zid)	
	
	return render_template('friend_profile.html',friend_details = show_details_str,friend_img = img_path)


@app.route('/search',methods=['GET','POST'])
def search():
	keyword = request.form.get('keyword', '')
	
	zid_list = glob.glob(students_dir+"/*")
	#print(zid_list)
	students_list = []

	
	for path in zid_list:
	
		student_info = {
		'name':'',
		'zid':'',	
		}# a dict to store  student name and zid
		
		details_path = os.path.join(path,"student.txt")
		#print("details_path in search:",details_path)
		with open(details_path) as f:
			details_list = f.readlines()
		
		details_list_length = len(details_list)
		i = 0
		while(i < details_list_length):
			if 'full_name:' in details_list[i]:
				line = details_list[i]
				line = line.rstrip()
				line = line.replace('full_name: ','')
				student_info['name'] = line
				
			elif 'zid:' in details_list[i]:
				line = details_list[i]
				line = line.rstrip()
				line = line.replace('zid: ','')
				student_info['zid'] = line
				
			i+=1
			
		students_list.append(student_info)
			
	#print("students list:",students_list)
	
	name_list = []	
	zid_list = []
	result_list = []	
	
	for dic in students_list:
		keyword_low = keyword.lower()
		name_low = dic['name'].lower()
		if keyword_low in name_low:
			result_list.append(dic)
			
	#print(result_list)
	
	result_img_path_list = []
	
	for dic in result_list:
		img_path = os.path.join(students_dir, dic['zid'], "img.jpg")
		result_img_path_list.append(img_path)		
		
	
	return render_template('search.html',result_list=result_list,img_path_list=result_img_path_list)
	


@app.route('/friend_post/<string:cur_zid>',methods=['GET','POST'])
def friend_post(cur_zid):

	self_post_list = []
	for self_post_path in glob.glob(os.path.join(students_dir, cur_zid, '*.txt')):
		#print(self_post_path)
		
		
		
		parts = self_post_path.split("/")
		#print(parts[3])
		if("-" not in parts[3] and "s" not in parts[3]):	
	
			with open(self_post_path) as f:
			   self_post_content = f.readlines()#read the self post line by line
			   str_of_post = ''.join(self_post_content)
			   self_post_list.append(str_of_post)
		   
	new_self_post_list = []# use to store each dict above
	
	for post in self_post_list: # each post here is a bunch of content which contain form, time...
		#print(post)
	
		post_info = { # each self post has a dict like this
		'from': '',
		'time': '',
		'message': '',
		'long': '',
		'lat': '',
	
		}
	
	
		post_parts = post.split("\n") #post_parts is a list contain the content of a post
		length_of_parts = len(post_parts)
		i = 0
		while i < length_of_parts:
			if 'from:' in post_parts[i]:
				post_info['from'] = post_parts[i]
			elif 'time:' in post_parts[i]:
				line = post_parts[i]
				new_line = line.replace('+0000','')
				new_line = new_line.replace('T',' ')
				post_info['time'] = new_line[6:]
		        
			elif 'message:' in post_parts[i]:
				post_info['message'] = post_parts[i]
			elif 'longitude:' in post_parts[i]:
				post_info['long'] = post_parts[i]
			elif 'latitude:' in post_parts[i]:
				post_info['lat'] = post_parts[i]
			i+=1
		
		new_self_post_list.append(post_info)	

	new_self_post_list.sort(key=key_function)
	new_self_post_list=new_self_post_list[::-1]
	
	return render_template('friend_post.html',post_list=new_self_post_list)
	

@app.route('/make_post',methods=['GET','POST'])
def make_post():
	post = request.form.get("post","")#get post from profile
	self_post_list = []
	for self_post_path in glob.glob(os.path.join(students_dir, session['zid'], '*.txt')):
		#print(self_post_path)	
		
		parts = self_post_path.split("/")
		#print(parts[3])
		if("-" not in parts[3] and "s" not in parts[3]):	
	
			with open(self_post_path) as f:
			   self_post_content = f.readlines()#read the self post line by line
			   str_of_post = ''.join(self_post_content)
			   self_post_list.append(str_of_post)	
	
	old_post_num = len(self_post_list)
	post_path = os.path.join(students_dir,session['zid'],"%s.txt"%old_post_num)
	#print(post_path)
	#print(post)
	f = open(post_path,'w')
	
	post_list = []
	post_list.append("from: "+session['zid'])
	post_list.append("message: "+post)
	cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	post_list.append("time: "+cur_time)
	
	f.write(post_list[0])
	f.write("\n")
	f.write(post_list[1])
	f.write("\n")
	f.write(post_list[2])
	
	f.close()
	
	hint = "Click MyPost to see your recent post~"
	return render_template('user_post.html', hint = hint)
	
@app.route('/delate_friend/<string:cur_zid>',methods=['GET','POST'])
def delate_friend(cur_zid):
	#print(cur_zid)
	details_path = os.path.join(students_dir, session['zid'], "student.txt")
	#print(details_path)
	
	details_list = []
	new_list = []
	with open(details_path) as f:
		details_list = f.readlines()
		
	#print(details_list)
	
	for line in details_list:
		
		if cur_zid in line:
			#print("enter if\n\n\n\n\n")
			new_line = line.replace(cur_zid+", ","")
			new_list.append(new_line)
		else:
			new_list.append(line)
			
	f = open(details_path,'w')
	f.close()
			
			
	f = open(details_path,'a')
	for line in new_list:
		f.write(line)
		
	f.close()
	
	hint = "Click Friends to see your new frineds list~"
	
	return render_template('user_friends.html', hint=hint)
			
	
@app.route('/add_friend/<string:cur_zid>',methods=['GET','POST'])
def add_friend(cur_zid):

	#print(cur_zid)

	details_path = os.path.join(students_dir, session['zid'], "student.txt")
	#print(details_path)
	
	details_list = []
	new_list = []
	with open(details_path) as f:
		details_list = f.readlines()
		
	#print(details_list)
	
	for line in details_list:
		
		if "friends:" in line:
			
			if cur_zid in line:
				new_list.append(line)
			else:
				new_line = line.replace("friends: (","friends: ("+cur_zid+", ")
				new_list.append(new_line)
		else:
			new_list.append(line)
			
	#print(new_list)
			
			
			
	f = open(details_path,'w')
	f.close()
			
			
	f = open(details_path,'a')
	for line in new_list:
		f.write(line)
		
	f.close()
	
	hint = "Click Friends to see your new frineds list~"
	
	return render_template('user_friends.html', hint=hint)
				


@app.route('/search_post',methods=['GET','POST'])
def search_post():
	keyword = request.form.get('keyword', '')
	#print(keyword)
	
	
	self_post_list = []
	for self_post_path in glob.glob(os.path.join(students_dir, session['zid'], '*.txt')):
		#print(self_post_path)
		
		
		
		parts = self_post_path.split("/")
		#print(parts[3])
		if("-" not in parts[3] and "s" not in parts[3]):	
	
			with open(self_post_path) as f:
			   self_post_content = f.readlines()#read the self post line by line
			   str_of_post = ''.join(self_post_content)
			   self_post_list.append(str_of_post)
		   
	new_self_post_list = []# use to store each dict above
	
	for post in self_post_list: # each post here is a bunch of content which contain form, time...
		#print(post)
	
		post_info = { # each self post has a dict like this
		'from': '',
		'time': '',
		'message': '',
		'long': '',
		'lat': '',
	
		}
	
	
		post_parts = post.split("\n") #post_parts is a list contain the content of a post
		length_of_parts = len(post_parts)
		i = 0
		while i < length_of_parts:
			if 'from:' in post_parts[i]:
				post_info['from'] = post_parts[i]
			elif 'time:' in post_parts[i]:
				line = post_parts[i]
				new_line = line.replace('+0000','')
				new_line = new_line.replace('T',' ')
				post_info['time'] = new_line[6:]
		        
			elif 'message:' in post_parts[i]:
				post_info['message'] = post_parts[i]
			elif 'longitude:' in post_parts[i]:
				post_info['long'] = post_parts[i]
			elif 'latitude:' in post_parts[i]:
				post_info['lat'] = post_parts[i]
			i+=1
		
		new_self_post_list.append(post_info)	

#	new_self_post_list.sort(key=key_function)
#	new_self_post_list=new_self_post_list[::-1]

	result_list = []
	for post in new_self_post_list:
		if keyword in post['message']:
			result_list.append(post)
			
	return render_template('search_post.html',result_list = result_list)


@app.route('/reply',methods=['GET','POST'])
def reply():

	post = request.form.get("post","")#get post from profile
	self_post_list = []
	for self_post_path in glob.glob(os.path.join(students_dir, session['zid'], '*.txt')):
		#print(self_post_path)	
		
		parts = self_post_path.split("/")
		#print(parts[3])
		if("-" not in parts[3] and "s" not in parts[3]):	
	
			with open(self_post_path) as f:
			   self_post_content = f.readlines()#read the self post line by line
			   str_of_post = ''.join(self_post_content)
			   self_post_list.append(str_of_post)	
	
	old_post_num = len(self_post_list)
	
	post_num_list = []
	
	i = 0
	reply_list = []
	while(i<old_post_num):
		num_dic = {} # this dict contain three key: num, self_post and reply_to_post; reply_to_post store a list which contian the replys to this post 
		#reply_list = []
		num_dic['num'] = i
		num_dic['self_post']=self_post_list[i]
		
		######################
		#create a list to store the reply to current(this) post
		
		for post_path in glob.glob(os.path.join(students_dir,session['zid'],'*.txt')):
		
			
			#print("enter this for loop")
		
			parts = post_path.split("/")
			if(re.match('%s-[0-9].txt'%i,parts[3]) and "s" not in parts[3]):
				#print("enter this if statement in for loop")
				#print(post_path)
				#print("=====================================================")
				with open(post_path) as f:
					post_content = f.readlines()
					post_str = ''.join(post_content)
					reply_list.append(post_str)
		

		######################
		
					num_dic['reply_to_post'] = reply_list
		
		post_num_list.append(num_dic)
		
		
		
		
		i+=1
		
	#print(post_num_list)
	#print(reply_list)
	
	return render_template('reply.html', post_num_list = post_num_list)


@app.route('/logout',methods=['GET','POST'])	
def logout():
	session.clear()
	#return redirect(url_for('login'))
	return render_template('login.html')	


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
