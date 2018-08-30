import praw
import config
import time
import requests
import argparse
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


def get_top_submissions(subreddit):
	top_submissions = []
	submission_ids = subreddit.hot(limit=25)
	for id in submission_ids:
		top_submissions.append(reddit.submission(id).url)	
	return top_submissions



def get_subreddit_images(reddit, subreddits):
	images = []
	for subreddit in subreddits:
		submissions = subreddit.hot(limit=25)
		images.append(detect_images(submissions))



def save_images_from_subreddits(reddit, subreddits):
	print 'Let''s go!'

	print 'Getting subreddits...'
	subreddit_list = ''
	
	for subreddit in subreddits:
		subreddit_list += subreddit + '+'

	subreddit_list = subreddit_list[:-1]

	submission_urls = []
	submissions = reddit.subreddit(subreddit_list).hot(limit=25)

	for submission in submissions:
		submission_urls.append(submission.url)

	print 'Detecting images'
	images = detect_images(submission_urls)

	print 'Saving images'

	save_images(images)

	print 'Done'

def save_upvoted_image_submissions(reddit):
	print 'Let''s go!'

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

def parse_args():
	parser = argparse.ArgumentParser(description='Image Saver')
	parser.add_argument('-s', '--subreddits', action='store_true', help='choose a list of subreddits to save images from')
	parser.add_argument('-u', '--upvoted', action='store_true', help='save images from your latest upvoted submissions')
	args = parser.parse_args()
	return args

def main():
	print 'Image Saver Reddit bot by /u/yelhsa08'

	reddit = bot_login()

	args = parse_args()

	if args.subreddits:
		print 'Let''s get some images from subreddits'
		subreddit_input = raw_input('Enter a comma-separated list of subreddits (e.g. wallpaper,EarthPorn,multiwall): ')
		subreddits = subreddit_input.split(',')
		save_images_from_subreddits(reddit, subreddits)
	elif args.upvoted:
		print "Let's look in your upvoted submissions"
		save_upvoted_image_submissions(reddit)

main()