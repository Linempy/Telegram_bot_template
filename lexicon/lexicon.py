from random import choice


welcome_words: list[str] = ['Приветствую!', 'Здравствуй!', 'Привет!']

LEXICON: dict[str, str] = {
    'start': f'<b>{choice(welcome_words)}</b>\n\nЭто бот, который '
              'поможет в подготовке к Единому Государственному Экзамену '
              'по информатике\n\nЧтобы узнать подробную информацию о боте '
              'выполни команду /info\nВыполни команду /help, если хочешь '
              'посмотреть список доступных команд\n\nУдачи в подготовке!',
    'help': '<b>Это бот для подготовке к ЕГЭ по информатике</b>\n\n'
            'Дотупные команды:\n\n/file_to_prepare - клавиатура '
            'с файлами для подготовки\n/qiuck_test - быстрый тест\n'
            '/useful_links - полезные ссылки\n/info - подробная информация '
            'об использовании бота\n/help - справка о боте\n\n<b>Удачи '
            'в подготовке! 🍀</b>',
    'info': 'Это бот для подготовки к ЕГЭ по информатике. Ниже представлен алгоритм '
            'взаимодейсвия с ботом:\n1. Выполнить команду /file_to_prepare, чтобы '
            'получить список  заданий с материалами для подготовки\n2. Выбрать интересующее '
            'задание\n3. Выбрать один из файлов: <em>Теория</em>, <em>Теория Python</em>, \n'
            '<em>Практика</em>\n\n Также вы можете проверить свои знания благодаря '
            'мини-тесту, выполнив команду /quick_test\n\nПо команде /useful_links представлены '
            'бесплатные ресурсы для подготовке к экзамену. \nДля отслеживания своей '
            'подготовки в написании пробников предлагаю Excel табличку, выполнив /get_excel_table'
            '\n\n<em><b>Примечание : большинство материала из файлов составлено по '
            'открытому курсу Алексея Кабанова: <a href="https://kompege.ru/course"> открытый '
            'курс</a>, <a href="https://vk.com/ege_info_open">сообщество в ВК</a></b></em>.'
            '\n\n<em><b>Примечание 2</b>: в файле <ins>Теория</ins> находятся аналитический '
            'метод решения или решение через Excel в зависимости от номера задания. В '
            '<ins>Теория Python</ins> описаны функции, синтаксис, которые используются '
            'для решения данного задания. В файлике <ins>Практика</ins> включен разбор '
            'заданий ЕГЭ: каталог заданий Школоково по информатике, сайт Полякова, сайт '
            'KOMPEGE. Авторство каждой задачи и ссылка на источник указаны в шапке задач.'
            '</em>',
    'useful_links': 'Открытый курс по подготовки к ЕГЭ по информатике Алексея Кабанова - <a href='
                     '"https://kompege.ru/course">KOMPEGE</a>\n'
                     'Курсы по Python:\n<a href="https://stepik.org/course/58852/promo">'
                     '"Поколение Python": курс для начинающих"</a>\n<a href='
                     '"https://stepik.org/course/68343/syllabus">"Поколение Python": '
                     'курс для продвинутых</a>\n\nСайт визуализации рекусии - <a href="https://'
                     'recursion.vercel.app/">Recursion Tree Visualizer</a>\nВизуализатор Python '
                     'кода - <a href="https://pythontutor.com/visualize.html#mode=edit">Python Tutor</a>\n\n'
                     'Каталог задач: <a href="https://3.shkolkovo.online/catalog?SubjectId=30">каталог '
                     'Школково</a>\n<a href="https://kpolyakov.spb.ru/school/ege.htm">сайт Константина '
                     'Юрьевича Полякова</a>\n<a href="https://kompege.ru/task">KOMPEGE</a>\n\nЮтуб каналы:'
                    #  'Для продвинутых:\n'
                     'Курс по основам командной строки: <a href="https://ru.hexlet.io/courses/cli-basics">'
                     'Хекслет</a>\nКурсы по основам Git: <a href="https://practicum.yandex.ru/trainer/git-basics'
                     '/lesson/874ec244-bc3a-4bba-8a92-259e5cd5a2a3/">Яндекс Практикум</a>, <a href="https://ru.'
                     'hexlet.io/courses/intro_to_git">Хекслет</a>, <a href="https://youtu.be/VJm_AjiTEEc?si='
                     'i-8fFSjmhpEKkut3">Что такое Git для начинающих</a>\n\nКурсы и тренажеры по SQL:\n'
                     '<a href="https://sql-academy.org/ru">SQL Academy</a>, <a href="https://sql-ex.ru/?Lang=0;">'
                     'Тренажер по SQL</a>\n\nРазработка Telegram-ботов:\n<a href="https://stepik.org/course/'
                     '120924/syllabus">Телеграм-боты на Python и AIOgram</a>',

    'echo': 'Я тебя не понимаю :(',
    'file_to_prepare': 'Для получения материалов нажми на интересующий номер задания:',
    'error': 'Кажется, что-то пошло не так',
    'type_file': '<b>Выбери один из файлов</b>\nЧтобы узнать, чем они отличаются '
                 'выполни команду /info',
    'send_file': 'Вот, держи свой файлик. Нажми на кнопку, чтобы вернуться к файлам',
    'adding_file': '<b>Выберите тему файла</b>.\nДля отмены выполните команду /cancel',
    'send_task_number': '<b>Напишите номер задания</b>. \nДля отмены выполните команду /cancel',
    'loading_file': '<b>Отправьте документ с материалом</b>. \nДля отмены выполните команду '
                    '/cancel',
    'cancel': 'Ваша форма успешно удалена',
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