from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardRemove
)

class KeyboardBuilder:
    def __init__(self):
        self.buttons = []
        self.row_width = 1
        self.keyboard_type = 'reply'
        self.resize_keyboard = True
        self.one_time_keyboard = False
        self.selective = None

    def set_type(self, keyboard_type: str):
        """Установить тип клавиатуры: 'reply' или 'inline'"""
        self.keyboard_type = keyboard_type
        return self

    def add_button(self, text: str, callback_data: str = None, url: str = None, request_contact: bool = False, request_location: bool = False):
        """Добавить кнопку с различными параметрами"""
        self.buttons.append({
            'text': text,
            'callback_data': callback_data,
            'url': url,
            'request_contact': request_contact,
            'request_location': request_location
        })
        return self

    def add_row(self, *buttons):
        """Добавить готовый ряд кнопок"""
        self.buttons.append(list(buttons))
        return self

    def set_row_width(self, width: int):
        """Установить количество кнопок в ряду"""
        self.row_width = width
        return self

    def set_resize(self, resize: bool):
        self.resize_keyboard = resize
        return self

    def set_one_time(self, one_time: bool):
        self.one_time_keyboard = one_time
        return self

    def set_selective(self, selective: bool):
        self.selective = selective
        return self

    def build(self):
        """Построить клавиатуру"""
        if not self.buttons:
            return ReplyKeyboardRemove()

        if self.keyboard_type == 'inline':
            return self._build_inline_keyboard()
        else:
            return self._build_reply_keyboard()

    def _build_inline_keyboard(self):
        keyboard = []
        current_row = []

        for btn in self.buttons:
            if isinstance(btn, list):
                if current_row:
                    keyboard.append(current_row)
                    current_row = []
                keyboard.append([self._create_inline_button(b) for b in btn])
            else:
                current_row.append(self._create_inline_button(btn))
                if len(current_row) >= self.row_width:
                    keyboard.append(current_row)
                    current_row = []

        if current_row:
            keyboard.append(current_row)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def _build_reply_keyboard(self):
        keyboard = []
        current_row = []

        for btn in self.buttons:
            if isinstance(btn, list):
                if current_row:
                    keyboard.append(current_row)
                    current_row = []
                keyboard.append([self._create_reply_button(b) for b in btn])
            else:
                current_row.append(self._create_reply_button(btn))
                if len(current_row) >= self.row_width:
                    keyboard.append(current_row)
                    current_row = []

        if current_row:
            keyboard.append(current_row)

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=self.resize_keyboard,
            one_time_keyboard=self.one_time_keyboard,
            selective=self.selective
        )

    def _create_inline_button(self, btn_data):
        if btn_data.get('url'):
            return InlineKeyboardButton(
                text=btn_data['text'], 
                url=btn_data['url']
            )
        else:
            return InlineKeyboardButton(
                text=btn_data['text'], 
                callback_data=btn_data['callback_data']
            )

    def _create_reply_button(self, btn_data):
        return KeyboardButton(
            text=btn_data['text'],
            request_contact=btn_data.get('request_contact', False),
            request_location=btn_data.get('request_location', False)
        )

    def clear(self):
        """Очистить конфигурацию"""
        self.__init__()
        return self
