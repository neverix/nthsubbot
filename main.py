import bot  # communication with the bot
import db  # database access


if __name__ == '__main__':
    # create a bot
    robot = bot.Bot("nthsubbot")
    # read the database
    db = db.DB("db.csv")
    # get 80th subreddit
    print(db.get_nth_subs(80))