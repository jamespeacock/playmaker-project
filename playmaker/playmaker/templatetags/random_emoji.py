import random
from django import template

register = template.Library()

def random_emoji(_):
    emojis = [':)', ':D', ':/', ':P', ':(', ':O']
    choice = random.choice(emojis)
    return choice

register.filter('random_emoji', random_emoji)