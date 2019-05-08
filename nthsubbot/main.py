import config
import reddit
import db as db_
from typing import Dict

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
    db = db_.DB(conf["db"]["path"])
    # get all nth subs
    nthsubs = list(db.search_nth_subs(tags=["thirdsub"]))

    def get_text_for_number(number: str, offset: int, posts: Dict[str, str]):
        try:
            sub = list(db.search_nth_subs(number_eq=int(number) + offset))[0].sub
        except ValueError:
            sub = None
        except IndexError:
            sub = None
        if sub not in posts:
            sub = None
        # noinspection PyTypeChecker
        return f"⚠️ under construction ⚠️" if sub is None else f"[r/{sub}]({posts[sub]})"

    def get_text(nthsub: db_.NthSub, posts: Dict[str, str]):
        try:
           int( nthsub.number)
           number = True
        except ValueError:
            number = False
        return (
            f"# {nthsub.number} - r/{nthsub.sub}\n\n" +
           ( f"**Go up**: {get_text_for_number(nthsub.number, 1, posts)}\n\n"  +
            f"**Go down**: {get_text_for_number(nthsub.number, -1, posts)}\n\n" if number else '') +
            "^(I'm a bot. Contact [the author](https://reddit.com/user/DatNeverikGuy) for more information.)")
    texts = {
        nthsub.sub: ("Sub ladder", get_text(nthsub, {})) for nthsub in nthsubs
    }
    post_links = reddit.post_or_edit(texts, submit=False)
    texts = {
        nthsub.sub: ("Sub ladder", get_text(nthsub, post_links)) for nthsub in nthsubs
    }
    post_links = reddit.post_or_edit(texts)
    texts = {
        nthsub.sub: ("Sub ladder", get_text(nthsub, post_links)) for nthsub in nthsubs
    }
    reddit.post_or_edit(texts)
