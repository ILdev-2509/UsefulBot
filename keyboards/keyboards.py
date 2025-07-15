from keyboards.keyboard_generator import KeyboardBuilder

main_menu = (
    KeyboardBuilder()
    .set_type("reply")
    .set_resize(True)
    .add_row(
        {"text": "Конвертер"},
        {"text": "Переводчик"}
    )
    .add_button(text="Менеджер паролей")
    .build()
)

choosing_converter = (
    KeyboardBuilder()
    .set_type("reply")
    .add_row(
        {"text": "Римские цифры"},
        {"text": "Системы счисления"}
    )
    .add_button(text="Отмена")
    .set_row_width(1)
    .set_resize(True)
    .build()
)

choosing_translator = (
    KeyboardBuilder()
    .set_type("reply")
    .add_row(
        {"text": "Переводчик клавиатуры"},
        {"text": "Переводчик морзе"}
    )
    .add_button(text="Отмена")
    .set_row_width(1)
    .set_resize(True)
    .build()
)

choosing_password_manager = (
    KeyboardBuilder()
    .set_type("reply")
    .add_row(
        {"text": "Сгенерировать пароль"},
        {"text": "Проверка надежности пароля"}
    )
    .add_button(text="Отмена")
    .set_row_width(1)
    .set_resize(True)
    .build()
)

def choosing_direction(directions: list[str]):
    return (
        KeyboardBuilder()
        .set_type("reply")
        .add_row(*[{"text": i} for i in directions])
        .add_button(text="Отмена")
        .set_resize(True)
        .build()
    )

def back_button():
    return (
        KeyboardBuilder()
        .set_type("reply")
        .add_button(text="Отмена")
        .set_resize(True)
        .build()
    )
