import telebot
from telebot import types
import csv
import hashlib
import os
import logging
from datetime import datetime
import re
import pytz

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = 'TOKEN_BOT'

# Секретный ключ для админов
SECRET_ADMIN_KEY = os.getenv('ADMIN_KEY', 'PASS_W')

# ID чата начальника для уведомлений
ADMIN_CHAT_ID = 'ADMIN_ID'  # Замените на реальный ID чата

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Пути для файлов
BOOKING_FILE = 'bookings.csv'
ADMINS_FILE = 'admins.txt'
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# Приветственное сообщение
WELCOME_MESSAGE = (
    "Вас приветствует официальный бот Санкт-Петербургской школы программирования для нового поколения CYBERSPACE."
)

# Тексты из ТЗ
DESCRIPTION_TEXT = """УВАЖАЕМЫЙ РОДИТЕЛЬ!

Вас приветствует команда школы программирования для нового поколения CYBERSPACE.

В CYBERSPACE ребята получают современные навыки в сфере программирования с 1 по 11 класс: от блочного программирования до подготовки к ОГЭ/ЕГЭ по профильным предметам с сентября по май.

В зимние и летние каникулы ученики разных возрастов участвуют в недельных интенсивах по образовательным модулям, которых нет в основной программе «сентябрь-май». Старшие ученики, как правило, закрепляют теоритические знания на реальных бизнес-проектах, посещают профориентационные экскурсии в IT организациях, знакомятся со специалистами разных отделов и механикой бизнес-процессов.

При выборе вуза и факультета всё это поможет вашему ребенку лучше
ориентироваться в современных специальностях и своих интересах. Во время обучения в CR он раскроет индивидуальные способности и таланты, что позволит ему сделать более осознанный выбор профессии и успешно реализовать себя в сложном, быстро меняющемся мире.

В конце обучения мы торжественно вручим каждому ученику сертификат
выпускника курса со списком пройденных модулей, а также рекомендацию с персональной характеристикой."""
ADDRESSES_TEXT = """✅️Петродворцовый район
Долгосрочная аренда в БЦ Ракета: вход под башней с часами, 3 этаж, 329 класс.
⚠️Аренду июль/август продлеваем в случае формирования групп на летние интенсивы. Либо вынуждено договор расторгаем.
\n✅️Другие районы Санкт-Петербурга
Краткросрочная аренда/коворкинги: из других районов города тоже принимаем заявки на летние интенсивы. В зависимости от спроса будем планировать открытие новых филиалов под долгосрочную аренду."""
COST_TEXT = """2200 РУБ / 1 ЧАС / 1 УРОК \nДля новых учеников действует 32% скидка на оплату летнего интенсива: 
1500 руб / 1 урок / 1 час. 
\nПо реферальной программе действует 45%: 1200 руб / 1 урок / 1 час. 
	Реферальная программа учитывается при указании информации о друге в заявке на обратный звонок и оплате обучения от обоих.
MAX 45% по реферальной программе или 100% предоплате.
Далее акционный тариф фиксируется для продолжения обучения с сентября.

Конец акции: 27.06.25\n"""
PRIVACY_TEXT = """Предоставляя данные, я даю согласие ИП Докудовский Руслан Римович (ОГРНИП 315784700159511) и его партнёрам на обработку персональных данных на условиях Политики конфиденциальности в целях оставления заявки на обратный звонок."""
KTURTLE_REPORT_TEXT = """Дата проведения: 17 мая, суббота 15:00-17:00
Модуль: Python (библиотека Turtle)
Педагог: Вадим Павлюченков

Тема урока:
Решение геометрических задач с использованием циклов. В видео показаны промежуточные результаты наших учеников. Ученики готовятся к контрольной.

Описание урока:
На занятии ученики работали с библиотекой Turtle, применяя циклы для построения геометрических фигур. Урок совмещал повторение основ геометрии с изучением принципов работы циклов в Python.

Ключевые моменты урока: Практическое применение циклов (for) для рисования фигур, Закрепление знаний по геометрии (углы, стороны, симметрия), Разбор типовых ошибок при работе с Turtle

Результаты:
Ученики улучшили понимание циклов, научились визуализировать геометрические задачи и получили базовые навыки работы с графической библиотекой Turtle. В видео-отчете показаны промежуточные результаты наших учеников, идет подготовка к контрольной В видео показаны лучшие проекты учеников."""
SCRATCH_REPORT_TEXT = """
Дата проведения: 24 мая
Модуль: Scratch
Тема урока: Контрольная работа. Создание игры с лабиринтом
Выполненные работы:
    Движение кота по лабиринту
        Реализовано управление котом с помощью стрелок клавиатуры
        Настроено корректное взаимодействие с препятствиями (кот не проходит сквозь стены)
    Дополнительные элементы игры
        Добавлены звуковые эффекты (звук победы)
        Реализована анимация движения (смена костюмов кота при перемещении)

Планы на следующее занятие:
    Добавление новых игровых элементов:
        Дверь и ключ для её открытия
        Враги (летающие огурцы)
    Расширение игрового процесса:
        Сбор звёзд как дополнительная цель

Итоги урока:
    Закреплены навыки работы с движением объектов, коллизиями и анимацией
    Подготовлена основа для дальнейшего развития проекта

Результаты:
Ученики улучшили понимание циклов, научились визуализировать геометрические задачи и получили базовые навыки работы с графической библиотекой Turtle. \nВ видео-отчете показаны промежуточные результаты наших учеников, идет подготовка к контрольной В видео показаны итоговые работы."""
REPORTS_TEXT = """Выберите группу для просмотра отчёта педагогов."""

# Состояния для сбора данных
user_data = {}


# Главное меню
def main_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Программа «Сентябрь-Май»", callback_data='program'))
    keyboard.add(types.InlineKeyboardButton("Подробнее о школе", callback_data='about'))
    keyboard.add(types.InlineKeyboardButton("Бронь до 27.06 MAX 45% скидку", callback_data='booking'))
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'main'
    return keyboard


# Меню "Программа"
def program_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("1-3", callback_data='program_1-3'))
    keyboard.add(types.InlineKeyboardButton("4-5", callback_data='program_4-5'))
    keyboard.add(types.InlineKeyboardButton("5-6", callback_data='program_5-6'))
    keyboard.add(types.InlineKeyboardButton("7-8", callback_data='program_7-8'))
    keyboard.add(types.InlineKeyboardButton("9-10", callback_data='program_9-10'))
    keyboard.add(types.InlineKeyboardButton("НАЗАД", callback_data='back'))
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'program'
    return keyboard


# Меню "Подробнее о школе"
def about_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(
        types.InlineKeyboardButton("Описание школы", callback_data='about_description'),
        types.InlineKeyboardButton("Видео-конкурс", callback_data='about_video'),
    )
    keyboard.add(
        types.InlineKeyboardButton("Благодарности", callback_data='about_thanks'),
        types.InlineKeyboardButton("Отчёты педагогов", callback_data='about_teachers_reports')
    )
    keyboard.add(
        types.InlineKeyboardButton("Назад", callback_data='back'),
    )
    keyboard.add(
        types.InlineKeyboardButton("Адреса филиалов", callback_data='about_addresses'),
        types.InlineKeyboardButton("Разработчики Бота", callback_data='about_devs'),
    )
    keyboard.add(
        types.InlineKeyboardButton("Стоимость", callback_data='about_cost'),
        types.InlineKeyboardButton("Задать вопрос", callback_data='ask_question')
    )
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'about'
    return keyboard


# Меню "Отчёты педагогов"
def reports_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Младшая группа (Scratch)", callback_data='report_scratch'))
    keyboard.add(types.InlineKeyboardButton("Средняя группа (K-Turtle)", callback_data='report_kturtle'))
    keyboard.add(types.InlineKeyboardButton("НАЗАД", callback_data='back'))
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'reports'
    return keyboard


# Меню "Стоимость"
def cost_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("ПОДРОБНЕЕ", callback_data='cost_summer'))
    keyboard.add(types.InlineKeyboardButton("НАЗАД", callback_data='back'))
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'cost'
    return keyboard


# Меню "Бронирование"
def booking_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("1-2", callback_data='booking_1-2'))
    keyboard.add(types.InlineKeyboardButton("3-5", callback_data='booking_3-5'))
    keyboard.add(types.InlineKeyboardButton("6-8", callback_data='booking_6-8'))
    keyboard.add(types.InlineKeyboardButton("9-11", callback_data='booking_9-11'))
    keyboard.add(types.InlineKeyboardButton("НАЗАД", callback_data='back'))
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'booking'
    return keyboard


# Меню "Летний интенсив"
def summer_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("1-2", callback_data='summer_1-2'))
    keyboard.add(types.InlineKeyboardButton("3-5", callback_data='summer_3-5'))
    keyboard.add(types.InlineKeyboardButton("6-8", callback_data='summer_6-8'))
    keyboard.add(types.InlineKeyboardButton("9-11", callback_data='summer_9-11'))
    keyboard.add(types.InlineKeyboardButton("НАЗАД", callback_data='back'))
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'summer'
    return keyboard


# Клавиатура для отмены
def cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("Отмена"))
    return keyboard


# Клавиатура для подтверждения политики
def confirm_privacy_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("✅Подтверждаю"))
    keyboard.add(types.KeyboardButton("Отмена"))
    return keyboard


# Клавиатура для возврата в главное меню
def back_to_main_menu():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Перейти в главное меню", callback_data='back_to_main'))
    return keyboard


# Клавиатура для возврата назад
def back_button():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("НАЗАД", callback_data='back'))
    return keyboard


# Валидация номера телефона
def validate_phone(phone):
    pattern = r'^(\+7|8|7)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return bool(re.match(pattern, phone))


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id]['menu_state'] = 'main'
    bot.send_message(chat_id, WELCOME_MESSAGE, reply_markup=main_menu(chat_id))
    logger.info(f"Команда /start выполнена для chat_id={chat_id}")


# Обработчик команды /addadmin
@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    try:
        command_parts = message.text.split()
        if len(command_parts) != 2:
            bot.reply_to(message, "Использование: /addadmin <ключ>")
            return

        provided_key = command_parts[1]
        if provided_key != SECRET_ADMIN_KEY:
            bot.reply_to(message, "Неверный ключ!")
            return

        chat_id = str(message.chat.id)
        if os.path.exists(ADMINS_FILE):
            with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
                admins = f.read().splitlines()
                if chat_id in admins:
                    bot.reply_to(message, "Вы уже администратор!")
                    return

        with open(ADMINS_FILE, 'a', encoding='utf-8') as f:
            f.write(chat_id + '\n')
        bot.reply_to(message, "Вы успешно добавлены как администратор!")
        logger.info(f"Добавлен администратор: chat_id={chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при добавлении администратора: {e}")
        bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")


# Обработчик команды /getbookings
@bot.message_handler(commands=['getbookings'])
def get_bookings(message):
    try:
        chat_id = str(message.chat.id)
        if os.path.exists(ADMINS_FILE):
            with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
                admins = f.read().splitlines()
                if chat_id not in admins:
                    bot.reply_to(message, "У вас нет прав администратора!")
                    return
        else:
            bot.reply_to(message, "Список администраторов пуст!")
            return

        if os.path.exists(BOOKING_FILE):
            with open(BOOKING_FILE, 'rb') as f:
                bot.send_document(chat_id, f, caption="Список заявок для обзвона")
        else:
            bot.reply_to(message, "Заявок пока нет.")
        logger.info(f"Команда /getbookings выполнена для chat_id={chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке заявок: {e}")
        bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")


# Обработчик команды /clearbookings
@bot.message_handler(commands=['clearbookings'])
def clear_bookings(message):
    try:
        chat_id = str(message.chat.id)
        if os.path.exists(ADMINS_FILE):
            with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
                admins = f.read().splitlines()
                if chat_id not in admins:
                    bot.reply_to(message, "У вас нет прав администратора!")
                    return
        else:
            bot.reply_to(message, "Список администраторов пуст!")
            return

        confirm_keyboard = types.InlineKeyboardMarkup()
        confirm_keyboard.add(types.InlineKeyboardButton("Подтвердить", callback_data='clear_bookings_confirm'))
        confirm_keyboard.add(types.InlineKeyboardButton("Отмена", callback_data='clear_bookings_cancel'))
        bot.reply_to(message, "Вы уверены, что хотите удалить все заявки? Это действие нельзя отменить.",
                     reply_markup=confirm_keyboard)
        logger.info(f"Команда /clearbookings выполнена для chat_id={chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при запросе очистки заявок: {e}")
        bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        logger.info(f"Callback received: chat_id={chat_id}, data={call.data}")

        user_data[chat_id] = user_data.get(chat_id, {})
        if call.data == 'program':
            bot.edit_message_text("Уважаемый родитель, выберите, пожалуйста, класс, в котором учится Ваш ребенок",
                                  chat_id=chat_id, message_id=message_id, reply_markup=program_menu(chat_id))
        elif call.data.startswith('program_'):
            class_range = call.data.split('_')[1]
            user_data[chat_id]['menu_state'] = f'program_{class_range}'
            bot.edit_message_text(f"Скачивание файла для {class_range} классов",
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
            file_path = f'{DATA_DIR}/program_{class_range}.pdf'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    bot.send_document(chat_id, f)
            else:
                bot.send_message(chat_id, "Файл не найден. Свяжитесь с нами через @rr_mir.")
            logger.info(f"Отправлен файл программы для class_range={class_range}, chat_id={chat_id}")
        elif call.data == 'about':
            bot.edit_message_text("Подробнее о школе:\n",
                                  chat_id=chat_id, message_id=message_id, reply_markup=about_menu(chat_id))
        elif call.data == 'about_description':
            user_data[chat_id]['menu_state'] = 'about_description'
            bot.edit_message_text(DESCRIPTION_TEXT,
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
        elif call.data == 'about_video':
            user_data[chat_id]['menu_state'] = 'about_video'
            bot.edit_message_text("Видео-конкурс → Видео, в котором будут разыграны подарки, опубликуем 29.06",
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
        elif call.data == 'about_thanks':
            user_data[chat_id]['menu_state'] = 'about_thanks'
            bot.edit_message_text("Благодарности от Лицея",
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
            for i in range(1, 3):
                file_path = f'{DATA_DIR}/thanks_{i}.jpg'
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        bot.send_photo(chat_id, f)
                else:
                    bot.send_message(chat_id, f"Изображение thanks_{i}.png не найдено. Свяжитесь с нами через @rr_mir.")
            logger.info(f"Отправлены благодарности для chat_id={chat_id}")
        elif call.data == 'about_teachers_reports':
            bot.edit_message_text(REPORTS_TEXT,
                                  chat_id=chat_id, message_id=message_id, reply_markup=reports_menu(chat_id))
        elif call.data == 'report_scratch':
            user_data[chat_id]['menu_state'] = 'report_scratch'
            bot.edit_message_text(SCRATCH_REPORT_TEXT,
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
            video_path = f'{DATA_DIR}/scratch_report_video.mp4'
            if os.path.exists(video_path):
                with open(video_path, 'rb') as f:
                    bot.send_video(chat_id, f)
            else:
                bot.send_message(chat_id, "Видео отчёта Scratch не найдено. Свяжитесь с нами через @rr_mir.")
            logger.info(f"Отправлен отчёт Scratch для chat_id={chat_id}")
        elif call.data == 'report_kturtle':
            user_data[chat_id]['menu_state'] = 'report_kturtle'
            bot.edit_message_text(KTURTLE_REPORT_TEXT,
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
            video_path = f'{DATA_DIR}/kturtle_report_video.mp4'
            if os.path.exists(video_path):
                with open(video_path, 'rb') as f:
                    bot.send_video(chat_id, f)
            else:
                bot.send_message(chat_id, "Видео отчёта K-Turtle не найдено. Свяжитесь с нами через @rr_mir.")
            logger.info(f"Отправлен отчёт K-Turtle для chat_id={chat_id}")
        elif call.data == 'about_addresses':
            user_data[chat_id]['menu_state'] = 'about_addresses'
            bot.edit_message_text(ADDRESSES_TEXT,
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
        elif call.data == 'about_devs':
            user_data[chat_id]['menu_state'] = 'about_devs'
            bot.edit_message_text("Бота создали:\n"
                                  "Чувин М.Д., ГБОУ лицей № 419, 10-А\n"
                                  "Санякова Е.Л., ГБОУ лицей № 419, 8-Э\n"
                                  "Альгин Н.С., ГБОУ гимназия № 415, 9-В\n"
                                  "Мальков В.Д., ГБОУ школа № 319, 10-А",
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
        elif call.data == 'about_cost':
            bot.edit_message_text(COST_TEXT,
                                  chat_id=chat_id, message_id=message_id, reply_markup=cost_menu(chat_id))
        elif call.data == 'cost_summer':
            user_data[chat_id]['menu_state'] = 'cost_summer'
            bot.edit_message_text("Выберите класс для получения информации о летнем интенсиве",
                                  chat_id=chat_id, message_id=message_id, reply_markup=summer_menu(chat_id))
        elif call.data.startswith('summer_'):
            class_range = call.data.split('_')[1]
            user_data[chat_id]['menu_state'] = f'summer_{class_range}'
            bot.edit_message_text(f"Информация о летнем интенсиве для {class_range} классов",
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
            for bg in ['white', 'black']:
                file_path = f'{DATA_DIR}/intensive_{class_range}_{bg}.pdf'
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        bot.send_document(chat_id, f)
                else:
                    bot.send_message(chat_id, f"Файл intensive_{class_range}_{bg}.pdf не найден.")
            bot.send_message(chat_id, "Для удобства отправляю 2 файла: PDF с белым и чёрным фоном")
            logger.info(f"Отправлена информация о летнем интенсиве для class_range={class_range}, chat_id={chat_id}")
        elif call.data == 'booking':
            user_data[chat_id]['menu_state'] = 'booking'
            bot.edit_message_text(
                "Уважаемый родитель! Выберите, пожалуйста, класс, в котором учится Ваш ребенок, чтобы после оставления заявки Бот смог корректно отправить презентацию 17-ти часового летнего интенсива.",
                chat_id=chat_id, message_id=message_id, reply_markup=booking_menu(chat_id))
            logger.info(f"Начало бронирования для chat_id={chat_id}")
        elif call.data.startswith('booking_'):
            class_range = call.data.split('_')[1]
            user_data[chat_id]['class_range'] = class_range
            user_data[chat_id]['state'] = 'confirm_privacy'
            bot.edit_message_text(PRIVACY_TEXT, chat_id=chat_id, message_id=message_id)
            file_path = f'{DATA_DIR}/ПОЛИТИКА_КОНФИДЕНЦИАЛЬНОСТИ_и_обработки_ПДн.docx'
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        bot.send_document(chat_id, f)
                    logger.info(f"Отправлен файл политики конфиденциальности для chat_id={chat_id}")
                else:
                    bot.send_message(chat_id,
                                     "Файл политики конфиденциальности не найден. Свяжитесь с нами через @rr_mir.")
                    logger.error(f"Файл политики конфиденциальности не найден для chat_id={chat_id}")
            except Exception as e:
                logger.error(f"Ошибка при отправке файла политики для chat_id={chat_id}: {e}")
            bot.send_message(chat_id, "Пожалуйста, подтвердите согласие, отправив '✅Подтверждаю'",
                             reply_markup=confirm_privacy_keyboard())
            logger.info(f"Ожидается подтверждение политики для chat_id={chat_id}, class_range={class_range}")
        elif call.data == 'clear_bookings_confirm':
            try:
                with open(BOOKING_FILE, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Name', 'Phone', 'Hashed_Phone', 'Class_Range', 'Referral', 'Timestamp'])
                bot.edit_message_text("Список заявок успешно очищен.",
                                      chat_id=chat_id, message_id=message_id)
                logger.info(f"Список заявок очищен администратором: chat_id={chat_id}")
            except Exception as e:
                logger.error(f"Ошибка при очистке заявок: {e}")
                bot.edit_message_text("Ошибка при очистке заявок. Попробуйте позже.",
                                      chat_id=chat_id, message_id=message_id)
        elif call.data == 'clear_bookings_cancel':
            bot.send_message(chat_id, "Очистка заявок отменена.")
            logger.info(f"Очистка заявок отменена для chat_id={chat_id}")
        elif call.data == 'back':
            current_state = user_data[chat_id].get('menu_state', 'main')
            if current_state.startswith('program_'):
                bot.edit_message_text("Уважаемый родитель, выберите, пожалуйста, класс, в котором учится Ваш ребенок",
                                      chat_id=chat_id, message_id=message_id, reply_markup=program_menu(chat_id))
            elif current_state in ['about_description', 'about_video', 'about_thanks', 'about_addresses', 'about_devs',
                                   'ask_question']:
                bot.edit_message_text("Подробнее о школе:\n",
                                      chat_id=chat_id, message_id=message_id, reply_markup=about_menu(chat_id))
            elif current_state == 'reports':
                bot.edit_message_text("Подробнее о школе:\n",
                                      chat_id=chat_id, message_id=message_id, reply_markup=about_menu(chat_id))
            elif current_state in ['report_scratch', 'report_kturtle']:
                bot.edit_message_text(REPORTS_TEXT,
                                      chat_id=chat_id, message_id=message_id, reply_markup=reports_menu(chat_id))
            elif current_state.startswith('summer_'):
                bot.edit_message_text(COST_TEXT,
                                      chat_id=chat_id, message_id=message_id, reply_markup=cost_menu(chat_id))
            elif current_state.startswith('booking'):
                bot.edit_message_text(WELCOME_MESSAGE,
                                      chat_id=chat_id, message_id=message_id, reply_markup=main_menu(chat_id))
            else:
                bot.edit_message_text(WELCOME_MESSAGE,
                                      chat_id=chat_id, message_id=message_id, reply_markup=main_menu(chat_id))
            logger.info(f"Назад к menu_state={user_data[chat_id]['menu_state']} для chat_id={chat_id}")
        elif call.data == 'back_to_main':
            user_data[chat_id] = user_data.get(chat_id, {})
            user_data[chat_id]['menu_state'] = 'main'
            bot.edit_message_text(WELCOME_MESSAGE,
                                  chat_id=chat_id, message_id=message_id, reply_markup=main_menu(chat_id))
            logger.info(f"Возврат в главное меню для chat_id={chat_id}")
        elif call.data == 'ask_question':
            user_data[chat_id] = user_data.get(chat_id, {})
            user_data[chat_id]['menu_state'] = 'ask_question'
            bot.edit_message_text("Переадресация на @rr_mir. Свяжитесь с нами для вопросов!",
                                  chat_id=chat_id, message_id=message_id, reply_markup=back_button())
    except Exception as e:
        logger.error(f"Ошибка в callback_query: chat_id={chat_id}, data={call.data}, error={e}")
        bot.send_message(chat_id, "Произошла ошибка. Пожалуйста, попробуйте связаться с нами через @rr_mir.")


# Обработчик текстовых сообщений для сбора данных
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        chat_id = message.chat.id
        user_data[chat_id] = user_data.get(chat_id, {})
        if user_data[chat_id].get('state'):
            state = user_data[chat_id]['state']
            if message.text == "Отмена":
                user_data[chat_id] = {'menu_state': user_data[chat_id].get('menu_state', 'main')}
                bot.send_message(chat_id, "Процесс бронирования отменен.", reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(chat_id, WELCOME_MESSAGE, reply_markup=main_menu(chat_id))
                logger.info(f"Бронирование отменено для chat_id={chat_id}")
                return
            if state == 'confirm_privacy':
                if message.text == "✅Подтверждаю":
                    user_data[chat_id]['state'] = 'name'
                    bot.send_message(chat_id, "КАК ВАС ЗОВУТ?", reply_markup=cancel_keyboard())
                    logger.info(f"Политика конфиденциальности подтверждена для chat_id={chat_id}")
                else:
                    bot.send_message(chat_id, "Пожалуйста, отправьте '✅Подтверждаю' для продолжения.",
                                     reply_markup=confirm_privacy_keyboard())
                    logger.info(f"Неверное подтверждение политики для chat_id={chat_id}: {message.text}")
                return
            if state == 'name':
                user_data[chat_id]['name'] = message.text.strip()
                user_data[chat_id]['state'] = 'phone'
                bot.send_message(chat_id, "ВАШ МОБИЛЬНЫЙ НОМЕР?\nПример: +79991234567 или 8-999-45-67",
                                 reply_markup=cancel_keyboard())
                logger.info(f"Получено имя для chat_id={chat_id}: {message.text}")
            elif state == 'phone':
                phone = message.text.strip()
                if not validate_phone(phone):
                    bot.send_message(chat_id,
                                     "Неверный формат номера. Пожалуйста, введите номер в формате: +79991234567, 8-999-123-45-67 или 79991234567",
                                     reply_markup=cancel_keyboard())
                    logger.info(f"Неверный формат номера: {phone}")
                    return
                user_data[chat_id]['phone'] = phone
                user_data[chat_id]['state'] = 'referral'
                bot.send_message(chat_id, "ОТ КОГО УЗНАЛИ О НАС *для реферальной программы?",
                                 reply_markup=cancel_keyboard())
                logger.info(f"Получен телефон для chat_id={chat_id}: {phone}")
            elif state == 'referral':
                user_data[chat_id]['referral'] = message.text.strip()
                user_data_for_saving = user_data[chat_id].copy()  # Явно берем данные для конкретного chat_id
                save_booking(user_data_for_saving, chat_id)
                bot.send_message(chat_id,
                                 "Благодарим за информацию, в ближайшее время с Вами свяжется наш администратор, Руслан, или свяжитесь самостоятельно: +79995153318",
                                 reply_markup=types.ReplyKeyboardRemove())
                class_range = user_data[chat_id]['class_range']
                for bg in ['white', 'black']:
                    for ext in ['pdf']:
                        file_path = f'{DATA_DIR}/intensive_{class_range}_{bg}.{ext}'
                        if os.path.exists(file_path):
                            with open(file_path, 'rb') as f:
                                bot.send_document(chat_id, f)
                        else:
                            bot.send_message(chat_id, f"Файл intensive_{class_range}_{bg}.{ext} не найден.")
                bot.send_message(chat_id,
                                 "Уважаемый родитель, пока ознакомьтесь, пожалуйста, с описанием летнего интенсива для возраста Вашего ребёнка."
                                 "Для удобства отправляю 2 одинаковых файла, но с 2 разными фонами: белый/чёрный")
                bot.send_message(chat_id, "Вы можете вернуться в главное меню для продолжения работы с ботом.",
                                 reply_markup=back_to_main_menu())
                logger.info(f"Заявка завершена для chat_id={chat_id}, class_range={class_range}")
                user_data[chat_id] = {'menu_state': 'main'}
        else:
            bot.send_message(chat_id, "Пожалуйста, используйте команду /start для начала работы.")
            logger.info(f"Неожиданное текстовое сообщение для chat_id={chat_id}: {message.text}")
    except Exception as e:
        logger.error(
            f"Ошибка в handle_text: chat_id={chat_id}, state={user_data.get(chat_id, {}).get('state', 'none')}, error={e}")
        bot.send_message(chat_id, "Ошибка отправки данных. Пожалуйста, начните с /start.",
                         reply_markup=types.ReplyKeyboardRemove())
        if chat_id in user_data:
            del user_data[chat_id]


# Сохранение данных в CSV и отправка уведомления начальнику
def save_booking(user_data, chat_id):
    # Установка часового пояса CEST
    cest = pytz.timezone('Europe/Paris')  # CEST соответствует Paris
    timestamp = datetime.now(cest).strftime('%Y-%m-%d %H:%M:%S %Z')

    logger.info(f"Тип user_data: {type(user_data)}, Содержимое user_data перед проверкой: {user_data}")
    if 'phone' not in user_data:
        logger.error(f"Отсутствует ключ 'phone' в user_data для chat_id={chat_id}")
        bot.send_message(chat_id, "Ошибка: Не указан номер телефона. Пожалуйста, начните процесс заново с /start.")
        return

    hashed_phone = hashlib.sha256(user_data['phone'].encode()).hexdigest()
    try:
        with open(BOOKING_FILE, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if os.path.getsize(BOOKING_FILE) == 0:
                writer.writerow(['Name', 'Phone', 'Hashed_Phone', 'Class_Range', 'Referral', 'Timestamp'])
            writer.writerow(
                [user_data['name'], user_data['phone'], hashed_phone, user_data['class_range'], user_data['referral'],
                 timestamp])
        logger.info(f"Заявка сохранена: {user_data['name']}, {user_data['class_range']}")

        # Отправка уведомления начальнику с отладкой
        logger.info(f"Попытка отправки уведомления начальнику в чат {ADMIN_CHAT_ID}")
        notification_text = (
            f"Новая регистрация:\n"
            f"Имя: {user_data['name']}\n"
            f"Телефон: {user_data['phone']}\n"
            f"Класс: {user_data['class_range']}\n"
            f"Реферал: {user_data['referral']}\n"
            f"Время: {timestamp}"
        )
        try:
            bot.send_message(ADMIN_CHAT_ID, notification_text)
            logger.info(f"Уведомление успешно отправлено в чат {ADMIN_CHAT_ID}")
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления в чат {ADMIN_CHAT_ID}: {e}")
            bot.send_message(chat_id, f"Ошибка отправки уведомления администратору: {e}")
    except IOError as e:
        logger.error(f"Ошибка при записи в файл {BOOKING_FILE}: {e}")
        bot.send_message(chat_id, "Ошибка при сохранении данных. Пожалуйста, попробуйте позже.")


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")