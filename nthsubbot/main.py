import config
import reddit
import db

if __name__ == '__main__':
    # read config
    conf = config.Config.read()
    # automatically create config entries
    conf = config.auto_create(conf, {
        "db": {
            "name": "database",
            "type": "dict",
            "keymaps": {
                "path": {
                    "name": "database path",
                    "type": "str"
                }
            }
        },
        "reddit": {
            "name": "reddit features",
            "type": "dict",
            "keymaps": {
                "login_args": {
                    "name": "login parameters",
                    "type": "dict",
                    "keymaps": {
                        "client_id": {
                            "name": "reddit client ID",
                            "type": "str"
                        },
                        "client_secret": {
                            "name": "reddit client secret",
                            "type": "secret"
                        },
                        "user_agent": {
                            "name": "reddit user agent",
                            "type": "str"
                        },
                        "username": {
                            "name": "reddit username",
                            "type": "str"
                        },
                        "password": {
                            "name": "reddit password",
                            "type": "secret"
                        }
                    }
                }
            }
        }
    })
    # save config
    config.Config.save(conf)
    # create reddit API instance
    reddit = reddit.Reddit(conf["reddit"]["login_args"])
    # create database
    db = db.DB(conf["db"]["path"])
    # remove all posts
    reddit.remove_all()
    # post to 80th sub
    print(reddit.post_or_edit({"eightiethsub": ("Super lame", "    test")}))
    print(reddit.post_or_edit({"eightiethsub": ("Super lame", "antitest")}))
