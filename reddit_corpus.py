import praw
from pprint import pprint
import json

user_agent = ("Corpus creator by Leah https://github.com/leahrnh")
r = praw.Reddit(user_agent=user_agent)

f = open ('tmp.txt', 'w')

subreddit = r.get_subreddit('movies')
#for submission in subreddit.get_hot(limit=1):
submission = r.get_submission(submission_id='2u0wiq')
t = submission.title
submission.replace_more_comments(limit=None, threshold=0)
forest_comments = submission.comments
#flat_comments = praw.helpers.flatten_tree(submission.comments)
for comment in forest_comments:
        #print(comment.body)
        f.write(comment.body)
        f.write('\n')

f.close()


q = "question"
a = "answer"

f2 = open ('tmp2.txt', 'w')
f2.write(json.dumps({'question':q, 'answer':a}, file))
f2.write(json.dumps({'question':a, 'answer':q}, file))

f2.close()
