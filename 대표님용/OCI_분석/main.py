import os
import time
import lib
from textwrap import dedent
from googletrans import Translator

bot = lib.Chat_engine(lib.session_token)

output = []
for inpur in df:
    output = bot.send_msg(input)





