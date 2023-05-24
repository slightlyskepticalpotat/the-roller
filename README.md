# the-roller
Reddit bot that rolls dice. I may put up a hosted instance in the future.

## Installation
```
$ git clone https://github.com/slightlyskepticalpotat/the-roller.git
$ cd the-roller
$ pip3 install -r requirements.txt
$ nano praw.ini # enter your settings
$ python3 the_roller.py &
```
## Usage

You can invoke this bot by mentioning it in a comment or replying to it in a thread with a valid dice roll. Valid dice rolls can be surrounded by other text, and follow the format:

`[Number of dice rolled]d[Maximum number rolled][operator][operand]`

The operator and operand are optional, and the operator can be any one of +, -, \*, /, or %. The number of dice rolled, maximum number rolled, and operand must all be positive. Some valid examples are:

- `1d20` (1 20-sided die)
- `2d20` (2 20-sided dice)
- `1d20*5` (1 20-sided die, multiplies result by 5)
- `2d20-5` (2 20-sided dice, sums results, subtracts 5)
