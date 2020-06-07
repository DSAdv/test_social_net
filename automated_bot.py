import re
import random
import argparse
import configparser
import logging
import requests

from urllib.parse import urljoin
from config import bot_config_path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf",
                    default="default",
                    help="Name of configuration section in bot_conf.ini")


def fetch_random_messages(count: int = 5):
    endpoint = "https://quotesondesign.com/wp-json/wp/v2/posts/?orderby=rand"
    messages = list()

    while len(messages) < count:
        messages.extend([
            remove_tags(msg["content"]["rendered"])
            for msg in requests.get(endpoint).json()
        ])

    return messages[:count]


def remove_tags(text):
    return re.compile(r'<[^>]+>').sub('', text)


class UserBot:
    default_password: str = "YouShallNotPass!!!"
    url_base: str = "http://127.0.0.1:5000"

    def __init__(self,
                 user_number: int,
                 max_posts_per_user: int,
                 max_likes_per_user: int):
        self.username = f"test_user_{user_number}"
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user

        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None

    def sign_up(self):
        endpoint = urljoin(self.url_base, "api/auth/register")
        payload = {
            "username": self.username,
            "password": self.default_password
        }
        response = self.session.post(endpoint, data=payload)

        if response.status_code == 200:
            json_response = response.json()
            logger.info(f"Successfully sign up for {str(self)}")
        else:
            json_response = self.session.post(urljoin(endpoint, "login"), data=payload).json()
            logger.info(f"User already exists. Login successfully instead")

        self.access_token = json_response["access_token"]
        self.refresh_token = json_response["refresh_token"]

        self.session.headers["Authorization"] = f"Bearer {self.access_token}"

    def create_random_posts(self):
        endpoint = urljoin(self.url_base, "api/posts")
        post_count = random.randint(0, self.max_posts_per_user)

        for post_body in fetch_random_messages(post_count):
            self.session.post(endpoint, data={"body": post_body})

        logger.info(f"Successfully created {post_count} by {str(self)}")

    def get_all_posts(self):
        endpoint = urljoin(self.url_base, "api/posts")
        return self.session.get(endpoint).json()["posts"]

    def like_random_posts(self):
        like_count = random.randint(0, self.max_likes_per_user)
        posts = random.choices(self.get_all_posts(), k=like_count)

        for post in posts:
            endpoint = urljoin(self.url_base, f"api/posts/{post['id']}/like")
            self.session.post(endpoint)

            logger.info(f"Liked post {post} by {str(self)}")

    def __str__(self):
        return f"UserBot<{self.username}>"

    def __repr__(self):
        return str(self)


def main():
    params = parser.parse_args()

    bot_conf = configparser.ConfigParser()
    bot_conf.read(bot_config_path)
    settings = bot_conf[params.conf]
    logger.info(f"Used config '{params.conf}' for bots")

    for i in range(int(settings["number_of_users"])):
        bot = UserBot(
            user_number=i,
            max_posts_per_user=int(settings["max_posts_per_user"]),
            max_likes_per_user=int(settings["max_likes_per_user"])
        )

        bot.sign_up()
        bot.create_random_posts()
        bot.like_random_posts()


if __name__ == '__main__':
    main()
