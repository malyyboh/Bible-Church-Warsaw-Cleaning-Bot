from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from keyboards.keyboards import bot_keyboard
from lexicon.lexicon import LEXICON_UA
from services.file_handling import prepare_data_person, prepare_saturday_data_persons
from filters.filters import IsAlphaAndIsSpace


router = Router()
storage = MemoryStorage()

schedule_url = ('https://docs.google.com/spreadsheets/d/1Q-snDE7LrDrT-ls90qJQ5G2T6UdMr8o4eZepSrC5_No/edit?gid'
                '=0#gid=0')
class FSMFillForm(StatesGroup):
    fill_name = State()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_UA['/start'],
                         reply_markup=bot_keyboard)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_UA['/help'],
                         reply_markup=bot_keyboard)


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_UA['/cancel'])


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_UA['cancel_search'],
                         reply_markup=bot_keyboard)
    await state.clear()


@router.message(Command(commands='search'), StateFilter(default_state))
@router.message(F.text == LEXICON_UA['search_button'], StateFilter(default_state))
async def process_search_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_UA['/search'],
                         reply_markup=bot_keyboard)
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), IsAlphaAndIsSpace())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    name_dict = await state.get_data()
    sent_name = prepare_data_person(name_dict['name'])
    if sent_name:
        await message.answer(text=f'{sent_name} \n\n{LEXICON_UA['successful_search']}',
                             reply_markup=bot_keyboard)
        await state.clear()
    else:
        await message.answer(text=LEXICON_UA['no_data'])


@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_UA['bad_input'])


@router.message(F.text == LEXICON_UA['show_all_button'])
@router.message(Command(commands='show'))
async def proces_show_command(message: Message):
    show_all = prepare_saturday_data_persons()
    if show_all:
        await message.answer(text=show_all,
                             reply_markup=bot_keyboard)
    else:
        await message.answer(text='Щось пішло не так...')


@router.message(F.text == LEXICON_UA['schedule_link_button'])
@router.message(Command(commands='schedule'))
async def proces_show_command(message: Message):
    if message == LEXICON_UA['schedule_link_button']:
        await message.answer(text=LEXICON_UA['/schedule'],
                             reply_markup=bot_keyboard)
    else:
        await message.answer(text=schedule_url,
                             reply_markup=bot_keyboard)
