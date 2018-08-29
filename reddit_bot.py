import praw
import config
import time
import requests
import os

image_directory = os.path.expanduser('~') + '/Documents/images/'

def bot_login():
	loggedIn = False
	while not loggedIn:
		try:
			reddit = praw.Reddit(username = config.username, 
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "ImageSaverBot (by /u/yelhsa08)")
			loggedIn = True
		except Exception as e:
			print e

	return reddit

def save_images(images):
	count = 1
	for image in images:
		file_name = '{}-{}{}'.format('images', count, '.jpg')
		with open(image_directory + file_name, "wb") as handler:
			handler.write(image)
		count += 1


def detect_images(urls):
	print 'Let''s see if these links contain images...'
	imgTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
	images = []
	count = 1
	for url in urls:
		print 'Looking at URL ' + str(count)
		try:
			r = requests.get(url)
			link_type = r.headers['content-type']
			if link_type in imgTypes:
				print 'Found an image'
				images.append(r.content)
		except requests.exceptions.RequestException as e:
			print 'Oops! Something fuckey''s going on...:', e
			pass
		except requests.exceptions.HTTPError as e:
			print 'Http Error: ', e
			pass
		except requests.exceptions.Timeout as e:
			print 'Timeout Error: ', e
			pass
		except requests.exceptions.ConnectionError as e:
			print 'Error Connecting: ', e 
			pass
		count = count + 1

	print 'Found the images'

	return images


def run_bot(reddit):
	print 'Let''s go!'
	# for comment in reddit.subreddit('EarthPorn','title','me_irl','spaceporn','wallpaper').comments(limit=25):
	# 	if "cat" in comment.body:
	# 		print "String found!!"
	# 		comment.reply("I found cat")

	print 'Finding upvoted submissions...'
	redditor = reddit.redditor(config.username)
	upvoted_submissions_ids = redditor.upvoted(limit=10)

	submissions = []
	for id in upvoted_submissions_ids:
		print 'Submission url: ' + reddit.submission(id).url
		submissions.append(reddit.submission(id).url)

	print 'Done'
	images = detect_images(submissions)

	print 'Saving images'

	save_images(images)

	print 'Done'

reddit = bot_login()

run_bot(reddit)