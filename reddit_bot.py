import praw
from prawcore import NotFound
import config
import time
import requests
import argparse
import os
from PIL import Image
import urllib2 as urllib
from cStringIO import StringIO

image_count = 1

def bot_login():
	loggedIn = False
	while not loggedIn:
		try:
			reddit = praw.Reddit(username = config.username, 
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = 'ImageSaverBot (by /u/yelhsa08)')
			loggedIn = True
		except Exception as e:
			print e

	return reddit

def get_link_type(url):
	try:
		r = requests.get(url)
		return r.headers['content-type']
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

def is_image(url):
	content_type = get_link_type(url)
	image_types = ['image/jpeg', 'image/jpg', 'image/png']
	return content_type in image_types

def convert_to_greyscale(image):
	return image.convert('L')

def rotate_image(image, degrees):
	return image.rotate(degrees)

def create_directory():
	if not os.path.exists(os.path.abspath(config.image_directory)):
		os.makedirs(os.path.abspath(config.image_directory))

def save_images(image_urls, greyscale, degrees):
	global image_count
	for url in image_urls:
		# Save image as the type indicated in the submission URL
		extension = ''
		if get_link_type(url) == 'image/jpeg' or get_link_type(url) == 'image/jpg':
			extension = 'jpg'
		elif get_link_type(url) == 'image/png':
			extension = 'png'

		# create PIL Image to save and use for transformations
		image_file = urllib.urlopen(url)
		image_content = StringIO(image_file.read())
		image = Image.open(image_content)
		if greyscale:
			image = convert_to_greyscale(image)
		if degrees != 0:
			image = image.rotate(degrees)
		file_name = '{}-{}.{}'.format('image', image_count, extension)
		image.save(config.image_directory + file_name)

		# enumerate image_count
		image_count += 1

def get_subreddit_images(reddit, subreddits, num):
	subreddit_list = ''
	for subreddit in subreddits:
		subreddit_list += subreddit + '+'
	subreddit_list = subreddit_list[:-1]

	images = []
	submissions = reddit.subreddit(subreddit_list).hot()
	
	while len(images) < num:
		submission = submissions.next()
		if is_image(submission.url):
			images.append(submission.url)
		time.sleep(1)

	return images

def subreddit_exists(reddit, subreddits):
	non_existent_subs = []
	for subreddit in subreddits:
		try:
			reddit.subreddits.search_by_name(subreddit, exact=True)
		except NotFound:
			non_existent_subs.append(subreddit)
	return non_existent_subs

def parse_args():
	parser = argparse.ArgumentParser(description='Image Saver Bot')
	parser.add_argument('-g', '--greyscale', action='store_true', help='indicates whether the images saved are converted to greyscale')
	parser.add_argument('-r', '--rotation', type=int, help='number of degrees to rotate images counterclockwise (a negative value will rotate clockwise)')
	args = parser.parse_args()
	return args

def run_bot():
	print 'Image Saver Reddit bot by /u/yelhsa08'

	# Login to reddit w/ user credentials
	reddit = bot_login()

	# Parse arguments for image transformations
	args = parse_args()
	greyscale = args.greyscale
	degrees_to_rotate = args.rotation

	# Parse subreddits from user input, filtering out empty items and finding any subreddits that do not exist
	subreddit_input = raw_input('Enter a comma-separated list of subreddits: ')
	subreddits = list(filter(None, subreddit_input.split(',')))
	subs_do_not_exist = subreddit_exists(reddit,subreddits)

	# Keep prompting the user to provide subreddits until all inputted subreddits exist; otherwise, notify which subreddits do not
	while len(subs_do_not_exist) > 0:
		print 'Woops! Couldn\'t find the following subreddits: {}'.format(subs_do_not_exist)
		subreddit_input = raw_input('Enter a comma-separated list of subreddits: ')
		subreddits = list(filter(None, subreddit_input.split(',')))
		subs_do_not_exist = subreddit_exists(reddit,subreddits)

	# Parse user input to get number of images to save, and keep trying until a valid integer is inputted
	valid_num = False
	while not valid_num:
		try:
			num_images = int(raw_input('Enter the number of images you want saved: '))
			valid_num = True
		except ValueError:
			print 'Input cannot be parsed as an integer. Please try again'
			continue

	# Create directory to save images to
	create_directory()

	# Get urls of the top image submissions from the inputted list of subreddits
	image_urls = get_subreddit_images(reddit, subreddits, num_images)

	# Save images to directory
	save_images(image_urls, greyscale, degrees_to_rotate)

	print 'Done! Check the directory for your images'

run_bot()