# telegram_bot_vk
##**Description**
С помощью данного проекта вы можете создать своего телеграм бота, который будет получать посты из сообществ _ВКонтакте_
**Примичание**: данный бот может получать только текстовые посты или посты с фотографиями, в случае если ваш пост содержит что-то еще, эти данные не будут отображаться в конечном результате
##**Technologic**
Для создания этого проекта были использованны библиотека PyTelegramBotAPI и API vk.API
##**Запуск**
Чтобы запустить проект, вам дополнительно потребуется создать файл **Tokens.py** и добавить в него 2 строки:
'''
vkServiceToken = 'XXXXXXXXXXX'
telegramToken = 'XXXXXXXXX'
'''
где _vkSevkServiceToken_ это сервисный ключ который можно получить из вашего приложения в вк, а _telegramToken_ - это токен вашего бота в telegram, который можно получить у **BotFather**
после создания данного файла, необходимо будет любым способом, например через консоль, запустить скрипт _telegram.py_
##Autor
Андрей NN
