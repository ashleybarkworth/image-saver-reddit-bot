# image-saver-bot

A Reddit bot to save the top image submissions from an inputted list of subreddits, and optionally perform a series of image transformations on them. 

## Getting Started

### Prerequisites

* **PRAW** - Install with `pip install praw`
* **Pillow** - Install with `pip install Pillow`

## How to Run the Bot

### Clone repository

`https://github.com/ashleybarkworth/image-saver-reddit-bot.git`

### Obtain Reddit API access credentials
1. Create a [Reddit](https://www.reddit.com/) account, and while logged in, navigate to preferences > apps
2. Click on the **are you a developer? create an app...** button
3. Fill in the details-
    * name: Name of your bot/script
    * Select the option 'script'
    * decription: Put in a description of your bot/script
    * redirect uri: `http://localhost:8080`
4. Click **create app**
5. You will be given a `client_id` and a `client_secret`. Keep them confidential.

### Setup config.py

Fill in the contents of config.py:

  ```
  username: reddit username
  password: reddit password
  client_id: client id you got
  client_secret: client_secret you got
  image_directory: directory to save images to
  ```

### Run the script

`python reddit_bot.py` 

#### Optional Arguments:
  ```
  -g, --greyscale: converts images to greyscale if included
  -r, --rotation: rotates images counterclockwise (a negative value rotates images clockwise)
  ```


