# SkyBank — анализ банковских операций

## Описание:

Приложение для анализа транзакций, которые находятся в Excel-файле. Приложение умеет генерировать JSON-данные для веб-страниц приложения, формировать Excel-отчеты и предоставляет ряд других сервисов.

## Установка:

Рекомендуется использовать PyCharm

Ссылка для добавления проекта
[git@github.com:kirillbarkhatov/SkyBank.git]()

Для создания виртуального окружения и установки зависимостей используйте Poetry

Модуль `external_api` использует сервисы https://apilayer.com и https://www.alphavantage.co. Создайте `.env` и добавьте токен API в `.env` как описано в шаблоне

## Использование:

1. Запускайте модули для получения результата

## Функционал

Функционал разбит на 7 модулей:
1. `utils`
2. `external_api`
3. `reports`
4. `services`
5. `views`

Для всех модулей реализовано логирование

Поддерживается чтение данных о транзакциях из файлов формата `xlsx`

Описания функций приведены в докстрингах и в документации ниже

## Тестирование:

Код в модулях пакета `src/` покрыт тестами
Для запуска тестов используйте команду `pytest`

Для проверки покрытия тестами используйте команду `pytest --cov`


## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)