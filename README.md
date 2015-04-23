Reddit Corpus Creator
===============

A python script to read a selection of Reddit threads, and save
statement-response pairs. It saves up to 3 responses for each
statement, chosen from the top submissions of the day.

Primarily uses Praw https://praw.readthedocs.org/

Input
-----
Currently reads the top 25 submissions from the following subreddits:
 * movies
 * books
 * Sports
 * News
 * television
 * gaming
 * gadgets
 * worldnews
 * programming
 * compsci
 * machinelearning
 * history
 * weather
 * AskReddit

It is also possible to modify the commented section at the bottom of
the code to read specific submission threads.

Output
-------
Writes JSON files named with the subreddit name and date. Each entry
has the following fields:
 * docID = subreddit ID
 * qSentID = semi-sequential number
 * question = a submission title, or a comment in a submission
 * aSentID = semi-sequential number
 * answer = a comment posted in response to the question
 * corpus = "reddit"

Corpus
-------
The current corpus contains 268 files collected between February 2 and
April 21, 2015. Most files contain between 200 and 3,000 turn pairs,
depending on the subreddit, although AskReddit tends to run closer to 15,000/day.
