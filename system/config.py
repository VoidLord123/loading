import datetime

from system.tg_keyboards import markup_start, markup_sub, markup_to_user, markup_to_bot

vk_api_token = "vk1.a.sVCWSGP4blxD8qQ1OhzNZNR7mj_JLKrItbuWfjhoYMtX8rzi0S7-AzkCOIXL_naTMOHYcqVlNur77u5LPP7z0U0aCJuRmbGdogC8j2vAID6I5IcfiAnLfBfwW9mJQihddM7Vin99XkTakPbLQ-8aKv6PYfgq17eSQDRz_WicK1KGswS-OA1McV55lqIYxcXEpW9j-4_hmSmk3WazygbO4A"
tg_api_token = "6514053896:AAEULNGpxEjjrx2xxB5HcPUdN2SaLkNRjsY"
database_filename = "system/db/database.sqlite"


dialogs_tg = {
    "start": {
        "text": """Привет! Я Инна Дан, профориентолог для взрослых и подростков. Рада приветствовать тебя! 🌟 
 
Хочешь понять, в какой точке ты находишься сегодня и каким образом развиваться дальше?   
 
""",
        "kb": markup_start
    },
    "not_subscribed": {
        "text": "Вы не подписаны на канал. Подпишитесь на канал чтобы использовать бота",
        "kb": markup_sub
    },
    "finish_test": {
        "text": "Для более подробных результатов вам необходимо пройти профориентацию. Переходите по кнопке!",
        "kb": markup_to_user
    },
    "start_test": {
        "text": """Впереди тебя ждет 10 вопросов, на которые нужно ответить цифрой от 0 до 10. 
Т.е. 10 – когда есть четкое понимание и удовлетворенность. 
0 - это ...
Отвечай быстро, первое что придёт на ум. Так ответы будут более правдивыми.

Нажми на кнопку ниже, чтобы начать тестирование.🚀
 
После получения результата ты можешь записаться на бесплатную консультацию.""",
        "kb": None
    },
    "to_bot": {
        "text": "Хотите пройти быстрый тест по профориентации?",
        "kb": markup_to_bot
    }
}

dialogs_vk = {
    "not_subscribed": "Вы не подписаны на группу. Подпишитесь чтобы продолжить",
    "start_test": """Впереди тебя ждет 10 вопросов, на которые нужно ответить цифрой от 0 до 10. 
Т.е. 10 – когда есть четкое понимание и удовлетворенность. 
0 - это ...
Отвечай быстро, первое что придёт на ум. Так ответы будут более правдивыми.

Нажми на кнопку ниже, чтобы начать тестирование.🚀
 
После получения результата кнопки 
Записаться на бесплатную консультацию.""",
    "finish_test": "Для более подробных результатов вам необходимо пройти профориентацию. Переходите по кнопке!",
    "start_bot": """Привет! Я Инна Дан, профориентолог для взрослых и подростков. Рада приветствовать тебя! 🌟 
 
Хочешь понять, в какой точке ты находишься сегодня и каким образом развиваться дальше?   
После получения результата ты можешь записаться на бесплатную консультацию.
""",
    "statistic": "Статистика по пользователям прошедшим тест.\nЗа последний месяц:"
                 "\n    Телеграмм: {tg_m}\n    Вк: {vk_m}\n    Общее: {all_m}\n\nЗа все время:"
                 "\n    Телеграмм: {tg_a}\n    Вк: {vk_a}\n    Общее: {all_a}"
}

time_constants = {
    "month": datetime.timedelta(days=30),
    "week": datetime.timedelta(days=7),
    "day": datetime.timedelta(days=1)
}

vk_commands = {
    "start": "Запустить тест",
    "first": "/start",
    "statistic": "/statistic",
    "sending": "/sending"
}

test = [
    "#1: Мне понятно, куда и ради чего я иду в жизни:",
    "#2: Я чувствую себя самореализованной(ым):",
    "#3: Я ощущаю себя счастливой(ым):",
    "#4: Я чувствую себя уверенной(ым):",
    "#5: Я знаю свои сильные/слабые стороны и активно этим пользуюсь:",
    "#6: Я осознаю, какая деятельность приносит мне радость, удовольствие, в чем мое призвание:",
    "#7: Я знаю, что смогу реализовать свои желания и цели:",
    "#8: Я умею ценить, радовать, баловать себя:",
    "#9: Моя личная жизнь и работа (профессиональная жизнь) сбалансированы:",
    "#10: Я умею «думать» сердцем, слышать свою интуицию, желания:"
]

results = [
    (30, "Такие результаты близки к состоянию высокой неудовлетворенности жизнью, собой, сложившейся ситуацией,"
         " результатом чего бывает депрессия, апатия, грусть и нежелание что-то делать. Вы сейчас переживаете трудный"
         " период. Скорее всего, вы не понимаете, что делать, куда идти дальше, ощущаете бессилие. Высока вероятность, "
         "что вы чувствуете отчужденность и непонимание со стороны окружения. В таком состоянии человек не знает, "
         "чего хочет, зачастую и веры в изменения тоже нет. Неудовлетворенность жизнью часто переносится на "
         "недовольство собой и высокую самокритику. Возможно, это временная ситуация, но если неудовлетворенность "
         "длится уже долго, нужно гораздо внимательнее отнестись к этой ситуации. Помните, что каждый хоть раз в жизни"
         " оказывался в трудной ситуации. Главное - не закрываться, а продолжать искать решение и действовать. "
         "Только действия дают шанс на изменение и решение ваших проблем. Шаг за шагом вы обязательно найдете выход,"
         " главное - ДЕЙСТВУЙТЕ. "),
    (55, "Видимо, сейчас вы находитесь в состоянии «на плаву», однако есть сферы, которые вам совершенно точно "
         "хотелось бы улучшить. Возможно, вы устали. Высока вероятность ощущения нереализованности в жизни, "
         "неуверенности в себе или в будущем. Однако такие баллы говорят о том, что есть вера в лучшее, надежда, "
         "что вы знаете, как решить вопросы, которые вас сейчас так волнуют. Однако не исключено, что вы часто "
         "задаете себе много вопросов, на которые пока не знаете ответа, и находитесь сейчас в поиске. Это переходный "
         "период. Возможно, вас нужно немного поддержать делом или советом в вопросах, которые так волнуют. Высока "
         "вероятность ощущения нехватки «прочности», «точки опоры», «фундамента», который только начал формироваться "
         "и находится еще в стадии «оформления». Страх и уверенность быстро друг друга сменяют, и вам не хватает "
         "внутренней стабильности, в том числе и эмоциональной, для более эффективного решения текущих вопросов."),
    (80, "Такие результаты говорят о вашей базовой удовлетворенности жизнью. Поздравляем, у вас все признаки «хозяина "
         "жизни», двигайтесь дальше по намеченному плану, и вы обязательно получите заслуженный «приз» - счастливая "
         "жизнь. Конечно, еще есть ряд вопросов, которые могут вас сильно беспокоить и, возможно, с какими-то сферами "
         "вы уже успешно разобрались, а с какими-то пока не знаете, как справиться. Главное - помните, что если вы "
         "смогли разобраться в одном, то и с оставшимися вопросами обязательно справитесь. Для начала научитесь "
         "ценить то, что уже есть, и с благодарностью в сердце идите дальше. Замечайте успехи и фиксируйте мысли и "
         "выводы. Никто, кроме вас самих, не знает вас лучше. Научитесь доверять себе, принимать и поддерживать. "
         "Станьте самым лучшим наставником, другом, учителем сами для себя. Тогда вы любой вопрос сможете решить. "
         "Посмотрите, что помогло вам в сферах, которые вас сегодня уже устраивают, и примените ту же схему, "
         "модель к вопросам, которые сегодня вас волнуют. С нашей стороны мы готовы вас поддержать и помочь вам "
         "научиться слышать себя, доверять своим желаниям и возможностям. Мы не всегда используем наш потенциал, "
         "хотя можем сделать гораздо больше и эффективнее. Мы готовы помочь вам в этом вопросе."),
    (120, "Поздравляем вас! Такие результаты говорят о вашей четкой позиции «хозяина жизни». Вас, скорее всего, "
          "в жизни практически все устраивает. Вы точно знаете составляющие счастливой жизни и что нужно сделать, "
          "чтобы поддерживать этот результат на стабильно высоком уровне. Вы смогли разобраться с основными аспектами "
          "жизни, которые сейчас создают ощущение радости, удовольствия, легкости, свободы. Вы уже делаете и знаете, "
          "что делать. Вопросы, которые сейчас перед собой ставите, не вводят вас в ступор, вы знаете и верите, "
          "что найдете ответ. ""Развитие"", ""наслаждение"", ""любопытство"", ""свобода"", ""накопление"" – вот "
          "слова, которые отражают ваше состояние сегодня. Такие люди часто являются «ловцами возможностей», "
          "они уже умеют создавать ситуации, в которых появляются нужные возможности для решения актуального вопроса, "
          "задачи. Такие люди находятся в состоянии предвкушения новых свершений, достижений и побед. Решив основные "
          "вопросы в жизни, становятся более внимательными к деталям, нюансам и мелочам. Вы знаете, что «лучшее» от "
          "«просто хорошего» отличают детали, что и привлекает вас сегодня. Желаем вам успеха в движении и дальше по "
          "жизни в позиции «хозяина»!")
]

tg_channel = "@innochkadan"
vk_group_id = "212051303"
vk_admin_id = "330652894"
