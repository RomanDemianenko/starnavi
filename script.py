import json
import random
import os
import secrets

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starnavi_project.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from post.models import Post, PostLike

User = get_user_model()
# Read the configuration file
with open('config.json') as f:
    config = json.load(f)

# Get configuration values
number_of_users = config['number_of_users']
max_posts_per_user = config['max_posts_per_user']
max_likes_per_user = config['max_likes_per_user']

# Create a list of user IDs
user_ids = []


def signup_user(username, password):
    password = make_password(password)
    user, _ = User.objects.get_or_create(username=username, password=password)
    user_ids.append(user.id)
    print(f"Signing up user {username}...")


# Loop through and sign up the specified number of users
for i in range(number_of_users):
    username = secrets.token_hex(8)
    password = f"password{i}"
    signup_user(username, password)

for user_id in user_ids:
    # Create a random number of posts for the user
    num_posts = random.randint(1, max_posts_per_user)
    for i in range(num_posts):
        # Generate a random post content
        post_text = f"Post {i + 1} by User {user_id}"
        # Store the post in the dictionary
        post = Post.objects.create(author_id=user_id, text=post_text)
        print(f"Post {post.id} by User {user_id}: {post_text}")
        # Choose Users who like it
        num_likes = random.randint(0, max_likes_per_user)
        if len(user_ids) >= num_likes:
            liked_by = random.sample(user_ids, num_likes)
        else:
            number_of_multiple_likes = num_likes - len(user_ids)
            user_ids_like_several_times = random.sample(user_ids, number_of_multiple_likes)
            liked_by = user_ids + user_ids_like_several_times
        # Like the post randomly
        for liked_user_id in liked_by:
            PostLike.objects.create(user_id=liked_user_id, post=post)
            print(f"User {liked_user_id} liked Post {post.id}")
