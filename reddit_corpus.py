from __future__ import print_function
from collections import OrderedDict
from datetime import date
import praw
import re
import json
import sys

#subredditList = ['movies', 'books', 'Sports', 'News', 'television', 'gaming', 'gadgets', 'worldnews', 'programming', 'compsci', 'machinelearning', 'history']
subredditList = ['worldnews', 'programming', 'compsci', 'machinelearning', 'history']

user_agent = ("Corpus creator by Leah https://github.com/leahrnh/reddit_corpus")
r = praw.Reddit(user_agent=user_agent)

comment_pairs = 0
line_id = 0

d = date.today() 

#Filter out comments that include things that are hard to pronounce, awkward to include in conversation, or otherwise inappropriate
def acceptable(comment):
    if comment == "[deleted]":
        return False
    p = re.compile('[a-z]+\.[a-z]+\.[a-z][a-z]')
    if p.search(comment):
        return False
    p = re.compile('http')
    if p.match(comment):
        return False
    return True

def processSubmission(submission, n):
    try:
        q = submission.title
        print("Looking at new submission: " + q[:30] + "...")
        submission.replace_more_comments(limit=None, threshold=0)
        forest_comments = submission.comments
        print("Reading comments")
        readcomments(q, forest_comments, f)
    except Exception as err:
        print("Exception is: " + str(err))
        print("Failed at try #" + str(n))
        if n < 11:
            time.sleep(60)
            processSubmission(submission, n+1)
        else:
            print("Giving up and moving on")
        
def readcomments(q, comments, f):
      global line_id
      line_id += 1
      q_id = line_id
      num_answers = 0
      for comment in comments:
        #add any processing to check for deleted comments or url's, etc here
        if acceptable(q) and acceptable(comment.body):
          global comment_pairs
          num_answers += 1
          if num_answers <= 3:
            line_id += 1
            a_id = line_id
            #print("Found comment pair: " + q[:10] + "...  " + comment.body[:20] + "...")
            #d = OrderedDict([("question", q), ("answer", comment.body), ("corpus", "reddit"), ("docID", submission.subreddit_id), ("qSentId", q_id), ("aSentId", a_id)])
            f.write(json.dumps({"question":q, "answer":comment.body, "corpus":"reddit", "docID":submission.subreddit_id, "qSentId":q_id, "aSentId":a_id}, indent=4))
            f.flush()
            #json.dumps(d, output, indent=4)
            comment_pairs += 1
          readcomments(comment.body, comment.replies, f)


for subred in subredditList:
    print("Examining subreddit " + subred)
    fileName = "reddit_corpus/" + subred + "_" + str(d) + ".txt"
    f = open (fileName, 'w')
    print("Created file " + fileName)
    subreddit = r.get_subreddit(subred)
    for submission in subreddit.get_hot(limit=25):
        processSubmission(submission, 0)
    f.close()
    print("Created file %s with %d comment pairs" % (fileName, comment_pairs))
