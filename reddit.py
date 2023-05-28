import config
import praw

reddit = praw.Reddit(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    user_agent=config.USER_AGENT,
    read_only=True)

subreddit = reddit.subreddit('uci')
keyword = 'ics 51'
search_results = subreddit.search(keyword, sort='relevance', limit=5)

for submission in search_results:
    print('Title:', submission.title)
    print('Comment:')
    submission.comments.replace_more(limit=5)
    for comment in submission.comments.list():
        print(comment.body)
        print('---')