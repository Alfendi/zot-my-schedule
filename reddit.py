import config
import praw

reddit = praw.Reddit(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    user_agent=config.USER_AGENT,
    read_only=True)

subreddit = reddit.subreddit('uci')
keyword = 'ics 51'
search_results = subreddit.search(keyword, sort='relevance', limit=3)

for submission in search_results:
    print("Link to the thread:", submission.url)
    print('Title:', submission.title)

    submission.comments.replace_more(limit=None, threshold=0)
    sorted_comments = sorted(submission.comments, key=lambda comment: comment.score, reverse=True)
    if sorted_comments:
        top_comment = sorted_comments[0]
        print("Top-rated comment:", top_comment.body)
    else:
        print("No comments found in the thread.")