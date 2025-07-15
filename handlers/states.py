from aiogram.fsm.state import State, StatesGroup

class MainStates(StatesGroup):
    choosing_converter = State()
    choosing_translator = State()
    choosing_password_manager = State()

class PasswordGeneratorStates(StatesGroup):
    waiting_for_input = State()

class PasswordCheckerStates(StatesGroup):
    waiting_for_input = State()

class KeyboardTranslatorStates(StatesGroup):
    waiting_for_direction = State()
    waiting_for_input = State()

class MorseTranslatorStates(StatesGroup):
    waiting_for_direction = State()
    waiting_for_input = State()

class BaseConverterStates(StatesGroup):
    waiting_for_input = State()

class RomanConverterStates(StatesGroup):
    waiting_for_direction = State()
    waiting_for_input = State()
