import praw
import psaw
import datetime as dt

start_epoch = int(dt.datetime(2014, 1, 1).timestamp())

r = praw.Reddit()
api = psaw.PushshiftAPI(r)

l_ = list(api.search_submissions(after=start_epoch,
                                subreddit='haiku',
                                filter=['title', 'subreddit'],
                                limit=None))

with open("./haikus.txt", 'ab') as MFile:
    for i, submission in enumerate(l_):
        if i % 100 == 0:
            print(submission.title)
        MFile.write(submission.title.encode('utf-8') + '\n'.encode('utf-8'))

