from random import choice


welcome_words: list[str] = ["Приветствую!", "Здравствуй!", "Привет!"]
sad_words: list[str] = ["Хорошо.", "Эх!", ""]

LEXICON: dict[str, str] = {
    "start": f"<b>{choice(welcome_words)}</b>\n\nЭто бот, который "
    "поможет в подготовке к ЕГЭ по информатике 👨🏼‍💻. Здесь Вы можете изучить теоретический "
    "материал необходимый для решения задач. Для проверки своих знаний можно выполнять "
    "тестовые задания"
    "\n\nЧтобы узнать подробную информацию о боте выполни команду /info"
    "\n\nУдачи в подготовке!",
    "help": "<b>Это бот для подготовки к ЕГЭ по информатике</b>\n\n"
    "<b>Доступные команды:</b>\n\n/file_to_prepare -  файлы для подготовки"
    "\n/test - тестовые задания\n/get_table - таблица для расчета баллов"
    "\n/useful_links - полезные ссылки"
    "\n/info - подробная информация об использовании бота\n/help - "
    "справка о боте\n\n<b>Удачи в подготовке! 🍀</b>",
    "info": "Это бот для подготовки к ЕГЭ по информатике. Ниже представлен алгоритм "
    "взаимодейсвия с ботом:\n1. Выполнить команду /file_to_prepare\n2. Выбрать интересующее "
    "задание\n3. Выбрать один из файлов:\n•<em>Теория</em>\n•<em>Теория Python</em>\n"
    "•<em>Практика</em>\n\nДля проверки своих знаний выполните команду /test"
    "\n\nПо команде /useful_links представлены "
    "бесплатные ресурсы для подготовки к экзамену. \nДля отслеживания своих "
    "результатов в написании пробников, предлагаю Excel табличку, выполнив /get_table"
    "\n\n<em><b>Примечание : большинство материала из файлов составлено по "
    'открытому курсу Алексея Кабанова: <a href="https://kompege.ru/course"> открытый '
    'курс</a>, <a href="https://vk.com/ege_info_open">сообщество в ВК</a></b></em>.'
    "\n\n<em><b>Примечание 2</b>: в файле <ins>Теория</ins> находятся аналитический "
    "метод решения или решение в Excel в зависимости от номера задания. В "
    "<ins>Теория Python</ins> описаны функции, синтаксис, которые используются "
    "для решения данного задания. В файле <ins>Практика</ins> включен разбор "
    "заданий ЕГЭ: каталог заданий Школоково по информатике, сайт Полякова, сайт "
    "KOMPEGE. Авторство каждой задачи и ссылка на источник указаны в шапке задач."
    "</em>",
    "useful_links": "Открытый курс по подготовке к ЕГЭ по информатике Алексея Кабанова - <a href="
    '"https://kompege.ru/course">KOMPEGE</a>\n'
    'Курсы по Python: <a href="https://stepik.org/course/58852/promo">'
    '"Поколение Python": курс для начинающих"</a>, <a href='
    '"https://stepik.org/course/68343/syllabus">"Поколение Python": '
    'курс для продвинутых</a>\n\nСайт для визуализации рекусии - <a href="https://'
    'recursion.vercel.app/">Recursion Tree Visualizer</a>\nВизуализатор Python '
    'кода - <a href="https://pythontutor.com/visualize.html#mode=edit">Python Tutor</a>\n\n'
    'Каталог задач: <a href="https://3.shkolkovo.online/catalog?SubjectId=30">каталог '
    'Школково</a>, <a href="https://kpolyakov.spb.ru/school/ege.htm">сайт Константина '
    'Юрьевича Полякова</a>, <a href="https://kompege.ru/task">KOMPEGE</a>\n\nЮтуб каналы:'
    ' <a href="https://www.youtube.com/@kompege">Алексей Кабанов</a>, <a href="https:'
    '//www.youtube.com/@pro100ege68">PRO100 ЕГЭ</a>, <a href="https://www.youtube.'
    'com/@inf_shkolkovo/streams">Информатика Школково</a>, <a href="https://www.youtube.'
    'com/@rodya_inf">Информатик Родя</a>\n\nДля продвинутых:\n'
    'Курс по основам командной строки: <a href="https://ru.hexlet.io/courses/cli-basics">'
    'Хекслет</a>\nКурсы по основам Git: <a href="https://practicum.yandex.ru/trainer/git-basics'
    '/lesson/874ec244-bc3a-4bba-8a92-259e5cd5a2a3/">Яндекс Практикум</a>, <a href="https://ru.'
    'hexlet.io/courses/intro_to_git">Хекслет</a>, <a href="https://youtu.be/VJm_AjiTEEc?si='
    'i-8fFSjmhpEKkut3">Что такое Git для начинающих</a>\n\nКурсы и тренажеры по SQL: '
    '<a href="https://sql-academy.org/ru">SQL Academy</a>, <a href="https://sql-ex.ru/?Lang=0;">'
    'Тренажер по SQL</a>\n\nРазработка Telegram-ботов: <a href="https://stepik.org/course/'
    '120924/syllabus">Телеграм-боты на Python и AIOgram</a>\n\nЮтуб каналы: <a href="https://'
    'www.youtube.com/@fakng-engineer">Влад Мишустин</a>, <a href="https://www.youtube.com/'
    '@SurenKhorenyan">Сурен Хоренян</a>, <a href="https://www.youtube.com/@PythonGuru_">'
    'PythonGuru</a>, <a href="https://www.youtube.com/@sudoteach">$ sudo tech IT</a>, '
    '<a href="https://www.youtube.com/@AndyPronin">Андрей += Пронин</a>\n\nГде решать '
    'алгоритмические задачки?\n<a href="https://neetcode.io/roadmap">Neetcode</a>, <a '
    'href="https://www.codewars.com">CodeWars</a>, <a href="https://leetcode.com">Leetcode</a>, '
    '<a href="https://codeforces.com">CodeForces</a>, <a href="https://acm.timus.ru/">Timus '
    'Online Judge</a>, <a href="https://acmp.ru">ACMP</a>\n\nАлгоритмы: <a href="https://'
    'brestprog.by/topics/">brestprog</a>, <a href="https://ru.algorithmica.org/cs/">Алгоритмика'
    '</a>\n\nСлепая печать: <a href="https://klava.org/delta/#rus_adv">Klava.org</a>, <a href='
    '"https://klavogonki.ru/u/#/752711/">Клавогонки</a>, <a href="https://www.keybr.com/typing-'
    'test">keybr</a>',
    "echo": "Я тебя не понимаю :(",
    "file_to_prepare": "Для получения материалов нажми на интересующий номер задания:",
    "error": "Кажется, что-то пошло не так",
    "type_file": "<b>Выбери один из файлов</b>",
    "send_file": "Нажми на кнопку <em>Назад</em>, чтобы вернуться к файлам",
    "adding_file": "<b>Выберите тему файла</b>.\nДля отмены выполните команду /cancel",
    "send_task_number": "<b>Напишите номер задания</b>. \nДля отмены выполните команду /cancel",
    "loading_file": "<b>Отправьте документ с материалом</b>. \nДля отмены выполните команду "
    "/cancel",
    "cancel": "Ваша форма успешно удалена",
    "cancel_default_state": "Мне пока что нечего отменять",
    "cancel_test": "Тест завершен",
    "agree_clear": "Ваши ответы удалены",
    "finish_test": "Количество набранных баллов: ",
    "get_task_title": "<b>Напишите название задачи.</b>\nДля отмены выполните команду "
    "/cancel",
    "send_quiz": "<b>Отлично!\nТеперь нужно создать викторину</b>",
    "small_len_title": "<b>Название должно быть больше 5 символов</b>",
    "small_first_char": "<b>Название должно начинаться с заглавной буквы</b>",
    "only_numbers": "<b>Название не может состоять только из цифр</b>",
    "send_picture": "<b>Отправьте изображение, если это необходимо, иначе "
    "нажмите на кнопку <em>Нет</em></b>",
    "result_poll": "<b>Так это задание будут видеть пользователи:</b>",
    "done_quiz": "Для сохранения задания нажмите <b>Готово</b>",
    "success_add_task": "Задание успешно сохранено, для его просмотра выполните "
    "команду /show_tasks",
    "test_result": "<b>Тест закончен</b>\n\nКоличество набранных баллов:",
    "not_finish_test": "<b>Пожалуйста завершите тест до конца</b>",
    "task_over": "<b>Поздравляю!🎉</b> Вы решили все задания",
    "test": "<b>Вводная информация</b>\nТест состоит из 5 заданий "
    "(викторин). Задания могут быть как на тему программирования, так и на обычные вычисления. "
    "После нажатия на один из вариантов ответа, Вы сразу же узнаете правильный ответ, также "
    "появляется значек лампочки 💡 около вопроса , при нажатии на который можно узнать краткое "
    "решение к данной задаче. По окончании теста будет подсчитано ваше количество набранных "
    "баллов за данный тест.\nЕсли готовы - нажмите кнопку <em>Начать тест</em> ",
    "get_table": "Таблица для расчета баллов",
    "write_title": "<b>Введите название задания</b>",
    "edit_tasks_button": "Редактировать",
    "cancel_button": "Отменить",
    "del_button": "✖️",
    "show_tasks": "<b>Список заданий:</b>",
    "backward": "<<",
    "forward": ">>",
    "edit_button": "<b>Нажмите на кнопку, чтобы удалить задание</b>",
    "cancel_start_test_words": f"{choice(sad_words)} Давай в следующий раз",
    "success": "Файл успешно добавлен!",
}

LEXICON_COMMANDS: dict[str, str] = {
    "/file_to_prepare": "Файлы для подготовки",
    "/test": "Мини-тест",
    "/get_table": "Таблица для пробников",
    "/useful_links": "Полезные ссылки",
    "/info": "Подробная информация",
    "/help": "Справка по работе бота",
}

LEXICON_COMMANDS_ADMIN: dict[str, str] = {
    "/adding_file": "Добавить файл",
    "/adding_task": "Добавить задание",
    "/show_tasks": "Список заданий",
    "/cancel": "Отмена",
}
