from random import choice


welcome_words: list[str] = ['Приветствую!', 'Здравствуй!', 'Привет!']

LEXICON: dict[str, str] = {
    'start': f'<b>{choice(welcome_words)}</b>\n\nЭто бот, который '
              'поможет в подготовке к Единому Государственному Экзамену '
              'по информатике\n\nЧтобы узнать подробную информацию о боте '
              'выполни команду /info\nВыполни команду /help, если хочешь '
              'посмотреть список доступных комнад\n\nУдачи в подготовке!',
    'help': '<b>Это бот для подготовке к ЕГЭ по информатике</b>\n\n'
            'Дотупные команды:\n\n/file_to_prepare - клавиатура '
            'с файлами для подготовки\n/qiuck_test - быстрый тест\n'
            '/useful_links - полезные ссылки\n/info - подробная информация '
            'об использовании бота\n/about - информация про создании бота\n'
            '/help - справка о боте\n\n<b>Удачи в подготовке! 🍀</b>',
    'echo': 'Я тебя не понимаю :(',
    'file_to_prepare': 'Для получения материалов нажми на интересующий номер задания:',
    'error': 'Кажется, что-то пошло не так',
    'type_file': '<b>Выбери один из файлов</b>\nЧтобы узнать, чем они отличаются '
                 'выполни команду /info',
    'send_file': 'Вот, держи свой файлик',
    'adding_file': '<b>Выберите тему файла</b>.\nДля отмены выполните команду /cancel',
    'send_task_number': '<b>Напишите номер задания</b>',
    'loading_file': '<b>Отправьте документ с материалом</b>',
    'cancel': 'Ваши действия успешно удалены',
    'cancel_default_state': 'Мне пока что нечего отменять',
}

LEXICON_COMMANDS: dict[str, str] = {
    '/file_to_prepare': 'Файлы для подготовки',
    '/qiuck_test': 'Мини-тест',
    '/useful_links': 'Полезные ссылки',
    '/info': 'Подробная информация',
    '/help': 'Справка по работе бота'
}

LEXICON_COMMANDS_ADMIN: dict[str, str] = {
    '/adding_file': 'Добавить файл',
    '/cancel': 'Отмена'
}