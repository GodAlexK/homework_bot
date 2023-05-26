import os
import requests
import sys
import telegram
import time
import logging

from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()

PRACTICUM_TOKEN = os.getenv('SECRET_PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('SECRET_TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('SECRET_TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def check_tokens():
    """Проверка доступности переменных окружения."""
    return all([PRACTICUM_TOKEN,
                TELEGRAM_TOKEN,
                TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправка сообщения в telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, text=message)
        logging.debug('Сообщение отправлено')
    except Exception as error:
        logging.error(f'Сбой при отправке сообщения: {error}')


def get_api_answer(timestamp):
    """Запрос к эндойнту API-сервиса."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
        response.raise_for_status()
    except requests.RequestException:
        logging.error('Сбой запроса к Api')
    if response.status_code != HTTPStatus.OK:
        status_code = response.status_code
        message_error = (f'API {ENDPOINT} недоступен,'
                         f'код ошибки {status_code}')
        raise TypeError(message_error)
    return response.json()


def check_response(response):
    """Проверка API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Неккоректный тип данных')
    if 'homeworks' not in response:
        raise KeyError('Отсутствуют ожидаемые ключи в ответе')
    if not isinstance(response['homeworks'], list):
        raise TypeError('Неккоректный тип данных у homeworks')
    return response['homeworks']


def parse_status(homework):
    """Извлечение информации статуса домашней работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status is None:
        raise KeyError('Отсутствует новый статус')
    if homework_name is None:
        logging.debug('Отсутсвует новый статус ответа')
        raise KeyError('Отсутствие домашней работы')
    if homework_status not in HOMEWORK_VERDICTS:
        logging.debug('Неверный формат')
        raise KeyError('Ответ не соответствует ожидаемому')
    verdict = HOMEWORK_VERDICTS[homework_status]
    logging.debug('Изменился статус проверки')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Необходимые переменные окружения отсутсвуют')
        sys.exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    send_message(bot, 'Bot activate')
    error_message = ''

    while True:
        logger.info('Запуск бота')
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            if len(homework) > 0:
                current_homework = homework[0]
                timestamp = response.get('current_date')
                status = parse_status(current_homework)
                send_message(bot, status)
                logger.debug(f'Сообщение отправлено: {status}')
            else:
                logger.debug('Новый статус не присвоен')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.exception(message)
            if message != error_message:
                send_message(bot, HOMEWORK_VERDICTS)
                logger.error(message)
                error_message = message
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
