import pytest
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from keyboards.keyboard_generator import KeyboardBuilder

class TestKeyboardBuilder:
    def test_empty_keyboard_returns_remove():
        builder = KeyboardBuilder()
        keyboard = builder.build()
        assert isinstance(keyboard, ReplyKeyboardRemove)

    def test_reply_keyboard_structure():
        builder = KeyboardBuilder()
        builder.add_button("Button 1").add_button("Button 2").set_row_width(2)
        keyboard = builder.build()
        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert keyboard.resize_keyboard is True
        assert keyboard.one_time_keyboard is False
        assert len(keyboard.keyboard) == 1
        assert keyboard.keyboard[0][0].text == "Button 1"
        assert keyboard.keyboard[0][1].text == "Button 2"

    def test_inline_keyboard_structure():
        builder = KeyboardBuilder()
        builder.set_type('inline').add_button("Inline 1", callback_data="cb1").add_button("Inline 2", callback_data="cb2").set_row_width(2)
        keyboard = builder.build()
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 1
        assert keyboard.inline_keyboard[0][0].text == "Inline 1"
        assert keyboard.inline_keyboard[0][0].callback_data == "cb1"
        assert keyboard.inline_keyboard[0][1].text == "Inline 2"
        assert keyboard.inline_keyboard[0][1].callback_data == "cb2"

    def test_reply_keyboard_custom_options():
        builder = KeyboardBuilder()
        builder.add_button("Contact", request_contact=True).set_one_time(True).set_resize(False)
        keyboard = builder.build()
        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert keyboard.one_time_keyboard is True
        assert keyboard.resize_keyboard is False
        assert keyboard.keyboard[0][0].request_contact is True

    def test_clear_resets_builder():
        builder = KeyboardBuilder()
        builder.add_button("Temp").clear()
        keyboard = builder.build()
        assert isinstance(keyboard, ReplyKeyboardRemove)
