from __future__ import print_function
import praw
import json
import sys

if len(sys.argv) < 3:
  print ("Please use arguments: (1) subreddit name (2) output file name")
  exit()

subred = sys.argv[1]
output = sys.argv[2]

user_agent = ("Corpus creator by Leah https://github.com/leahrnh")
r = praw.Reddit(user_agent=user_agent)

f = open (output, 'w')

comment_pairs = 0

def readcomments(q, comments):
      for comment in comments:
        global comment_pairs
        comment_pairs += 1
        print("Found comment pair: " + comment.body[:20] + "...")
        f.write(json.dumps({"question":q, "answer":comment.body}, sort_keys=False, indent=4))
        readcomments(comment.body, comment.replies)

subreddit = r.get_subreddit(subred)
for submission in subreddit.get_hot(limit=10):
    #submission = r.get_submission(submission_id='2u0wiq')
    q = submission.title
    submission.replace_more_comments(limit=None, threshold=0)
    forest_comments = submission.comments
    readcomments(q, forest_comments)

print("Created file with %d comment pairs" % comment_pairs)
f.close()
