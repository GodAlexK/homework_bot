# **Ассистент Telegram-бот**

## ****Описание****
Ассистент Telegram-бот - обращается к API сервиса узнает статус проверки выполненной работы.
Реализованы запросы бота к эндойнту API-сервиса, уведомления о смене статуса и важных событиях уровня "ERROR" отправляются в Telegram, логируются основные события.

## ****Использованные технологии****
- [Python](https://www.python.org/) - язык программирования;
- [Client API](https://appmaster.io/ru/glossary/api-klient)- client API позволяет создавать "юзерботов". Юзерботы — это специальные аккаунты, которые помечены как пользователи, но могут выполнять автоматизированные функции;
- [StreamHandler](https://docs.python.org/3/library/logging.handlers.html#streamhandler) - обработчик, для работы с логами проекта;
- [Sys.stdout](https://docs.python.org/3/library/sys.html#sys.stdout) -стандартный поток для вывода логов;
- [JSON(JavaScript Object Notation)](https://www.json.org/json-en.html) - это текстовый формат обмена данными, основанный на JavaScript;
- [Python-telegram-bot)](https://docs.python-telegram-bot.org/en/stable/index.html) - это официальная библиотека от Telegram для разработки ботов на Python, предоставляет простой и удобный интерфейс для работы с Telegram API, поддерживает обработку команд, обновлений, отправку сообщений и многое другое, содержит детализированную документацию и активное сообщество на GitHub;
- [Telegram](https://web.telegram.org/k/) - кроссплатформенная система мгновенного обмена сообщениями (мессенджер) с функциями обмена текстовыми, голосовыми и видеосообщениями, а также стикерами, фотографиями и файлами многих форматов;


## ****Установка проекта****
#### Подключение проекта и установка на сервер:
 - [ ] Подключитесь к удалённому серверу по SSH-ключу:
```
ssh -i путь_до_SSH_ключа/название_файла_с_SSH_ключом_без_расширения login@ip
```
 - [ ] Клонируйте проект с GitHub на сервер:
```
git clone git@github.com:ваш_аккаунт/infra_sprint1.git
```
#### Настройка бэкенд-приложения:
 - [ ] Создайте и активируйте виртуальное окружение:
```
source venv/bin/activate
```
 - [ ] Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
 - [ ] В папке с файлом manage.py выполните миграции:
```
python manage.py migrate
```
 - [ ] Создайте суперпользователя:
```
python3 manage.py createsuperuser
```
 - [ ] Соберите статику бэкенд-приложения:
```
python3 manage.py collectstatic
```
```
sudo cp -r путь_к_директории_с_бэкендом/static_backend /var/www/название_проекта
```
#### Создания пространства переменных окружения в файле .env:
 - [ ] Создайте файл .env в той же директории, что и исполняемый файл:
```
touch .env
```
 - [ ] Добавьте в файл .env переменные:
```
nano .env
```
```
SECRET_KEY = 'ВАШ_ТОКЕН'
````
```
DEBUG = 'False'
```
```
ALLOWED_HOSTS = 'IP сервера' 'ваш_домен'
```

#### Настройка фронтенд-приложения:
 - [ ] Находясь в директории с фронтенд-приложением, установите зависимости для него:
```
npm i
```
 - [ ] Из директории с фронтенд-приложением выполните команду:
```
npm run build
```
```
sudo cp -r путь_к_директории_с_фронтенд-приложением/build/. /var/www/имя_проекта/
```
#### Установка и настройка WSGI-сервера Gunicorn:
 - [ ] Подключитесь к удалённому серверу, активируйте виртуальное окружение
бэкенд-приложения и установите пакет gunicorn:
```
pip install gunicorn==20.1.0
```
```
gunicorn --bind 0.0.0.0:8080 kittygram_backend.wsgi
```
 - [ ] Создайте файл конфигурации юнита systemd для Gunicorn в директории (скопируйте файл gunicorn_kittygram.service с папки infra)
/etc/systemd/system/gunicorn_kittygram.service:
```
sudo nano /etc/systemd/system/gunicorn_kittygram.service
```
 - [ ] Команда sudo systemctl с параметрами start, stop или restart запустит, остановит
или перезапустит Gunicorn:
```
sudo systemctl start gunicorn_kittygram.service
```
#### Установка и настройка WSGI-сервера Gunicorn:
 - [ ] Установите Nginx на удалённый сервер:
```
sudo apt install nginx -y
```
```
sudo systemctl start nginx
```
 - [ ] Обновите настройки Nginx в файле конфигурации веб-сервера default(скопируйте файл default с папки infra):
```
sudo nano /etc/nginx/sites-enabled/default
```
 - [ ] Перезагрузите конфигурацию Nginx::
```
sudo systemctl reload nginx
```
#### Настройка файрвола ufw:
 - [ ] Файрвол установит правило, по которому будут закрыты все порты, кроме тех, которые
вы явно укажете:
```
sudo ufw allow 'Nginx Full'
```
```
sudo ufw allow OpenSSH
```
```
sudo ufw enable
```
```
sudo ufw status
```
#### Автоматизация тестирования и деплой проекта с помощью GitHub Actions:
 - [ ]  Файл .github/workflows/main.yml workflow будет:
```
Проверять код бэкенда в репозитории на соответствие PEP8;
```
```
Запускать тесты для фронтенда и бэкенда (тесты уже написаны);
```
```
Собирать образы проекта и отправлять их на Docker Hub (замените username на ваш логин на Docker Hub):
username/kittygram_backend,
username/kittygram_frontend,
username/kittygram_gateway.
```
```
Обновлять образы на сервере и перезапускать приложение при помощи Docker Compose;
```
```
Выполнять команды для сборки статики в приложении бэкенда, переносить статику в volume; выполнять миграции;
```
```
Извещать вас в Telegram об успешном завершении деплоя.
```

## **Автор**
- Алексей Коренков
