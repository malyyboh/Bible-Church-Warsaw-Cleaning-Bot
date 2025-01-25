from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from lexicon.lexicon import LEXICON_UA


search_button = KeyboardButton(text=LEXICON_UA['search_button'])
show_all_button = KeyboardButton(text=LEXICON_UA['show_all_button'])
web_app_button = KeyboardButton(
    text=LEXICON_UA['schedule_link_button'],
    web_app=WebAppInfo(url='https://docs.google.com/spreadsheets/d/1Q-snDE7LrDrT-ls90qJQ5G2T6UdMr8o4eZepSrC5_No/edit'
                           '?gid=0#gid=0')
)

bot_keyboard = ReplyKeyboardMarkup(
    keyboard=[[search_button],
              [show_all_button],
              [web_app_button]],
    resize_keyboard=True,
    input_field_placeholder='Натисни одну з кнопок...'
)
