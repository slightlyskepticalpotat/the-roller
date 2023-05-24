import logging
import praw
import re
import secrets
import time

def roll_die(roll, modifier=""):
    try:
        count, maximum = map(int, roll.split("d"))
        if count > 4096:
            raise Exception("Too many rolls")
        rolls = [secrets.randbelow(maximum) + 1 for _ in range(count)]
        total = sum(rolls)

        if modifier:
            if modifier[0] == "+":
                total += int(modifier[1:])
            elif modifier[0] == "-":
                total -= int(modifier[1:])
            elif modifier[0] == "*":
                total *= int(modifier[1:])
            elif modifier[0] == "/":
                total /= int(modifier[1:])
            elif modifier[0] == "%":
                total %= int(modifier[1:])
            else:
                raise Exception("Invalid operation")
        return roll + modifier + ": " + "**" + str(total) + "**" + "\n\n" + str(rolls) + "\n\n"
    except Exception as oops:
        logger.error(str(oops) + roll + modifier)
        return roll + modifier + ": " + "Error: Unable to parse roll." + "\n\n"

for logger_name in ("praw", "prawcore"): # setup logging
   logging.getLogger(logger_name).addHandler(logging.StreamHandler())
logging.basicConfig(filename='application.log', format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.DEBUG)

reddit = praw.Reddit("the_roller") # settings loaded from praw.ini
for comment in reddit.inbox.stream():
    if isinstance(comment, praw.models.Comment):
        dice, response = re.findall(r'(\d+d\d+)([+\-*/%]\d+)?', comment.body), "" # roll and optional modifier
        for die in dice:
            response += roll_die(die[0], die[1])
        if len(response) > 9905:
            response = "Error: Too many rolls at once.\n\n"
        if response:
            response += "---\n\nI can roll dice if you mention me! Check out my GitHub repository if you need any help."
            try:
                comment.reply(response)
            except praw.exceptions.RedditAPIException as error:
                time.sleep(min(int(re.search(r'\b(\d+)\b', str(error))[0]) * 60, 600)) # maximum of 10 minutes
                comment.reply(response)
    comment.mark_read()
