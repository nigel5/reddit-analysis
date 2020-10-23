"""
Dumps top submissions off a Reddit subreddit to a csv file

Input the Reddit API credentials in the 'opt' file at the root of this project.
"""
import praw
import pandas as pd
import demoji
import re

demoji.download_codes()

def download_submissions(subreddit, limit=1000):
  settings = {}
  with open('opts') as opts:
      for line in opts:
          name, setting = line.partition('=')[::2]
          settings[name.strip()] = setting.strip()
      
  reddit = praw.Reddit(
      client_id=settings['id'],
      client_secret=settings['secret'],
      user_agent=settings['user_agent']
  )

  d = {
      'author': [],
      'clicked': [],
      #'comments': [],
      'created_utc': [],
      'distinguished': [],
      'edited': [],
      'id': [],
      'is_original_content': [],
      'is_self': [],
      'link_flair_template_id': [],
      'link_flair_text': [],
      'locked': [],
      'name': [],
      'num_comments': [],
      'over_18': [],
      'permalink': [],
      #'poll_data': [],
      'score': [],
      'selftext': [],
      'spoiler': [],
      'stickied': [],
      #'subreddit': [],
      'title': [],
      'upvote_ratio': [],
      'url': []
  }
  for submission in reddit.subreddit(subreddit).top('all', limit=limit):
      for key in d:
          val = getattr(submission, key, 'None')
          if isinstance(val, str):
            val = demoji.replace(val)
            val = re.sub('[^A-Za-z0-9]+', '', val)
          d[key].append(val)

  df = pd.DataFrame(data=d)

  df.to_csv('{}_dump.csv'.format(subreddit.strip()))

if __name__ == '__main__':
  download_submissions('toronto', limit=999)