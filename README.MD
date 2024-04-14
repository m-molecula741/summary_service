## Основной сервис приложения "Конспект"

![PyPI - Version](https://img.shields.io/pypi/v/fastapi?style=flat&logoColor=green&label=fastapi&color=green&link=https%3A%2F%2Fblog.yezz.me%2Fstatic%2Fimages%2Fblog%2F07%2F01.png)
![PyPI - Version](https://img.shields.io/pypi/v/sqlalchemy?label=sqlalchemy)
![PyPI - Version](https://img.shields.io/pypi/v/pydantic?style=flat&logoColor=green&label=pydantic&color=blue&link=https%3A%2F%2Fblog.yezz.me%2Fstatic%2Fimages%2Fblog%2F07%2F01.png)

![konspeck](https://sun9-77.userapi.com/impg/8TQJRzmJbG-d0PScf8cWjCFn-tYt9Cn4zCWgbg/TLpXigIWOIk.jpg?size=828x1063&quality=96&sign=b31f826cf731e93c77e84e8f0537b165&type=album)

**Описание** : Данный проект является основным сервисом по обмену учебными материалами между студетами. В рамках сервиса можно создавать конспект, производить поиск конспектов по фильтьтрам (вуз, предмет, преподаватель, наименование), читать лекции определенного конспекта.

## Внимание

> Для успешной установки и запуска проекта без docker-compose у вас должна стоять версия python, указанная в pyproject.toml.

> Также запуск вне docker-compose не возможен без poetry

## Instalation

установить при помощи poetry:

```
poetry install --no-root
```
активировать окружение:
```
poetry shell
```
обновить пакеты:
```
poetry update
```

## Usage

создайте файл .env в корне
```
touch .env
```

скопируйте содержимое из .env.example

вместо xxx -> свои значения

## Run
запустить:
```
uvicorn app.main:app --reload
```

## Run with docker-compose

выполнить сборку
```
docker-compose build
```

запустить
```
docker-compose up
```

## License
Данный проект "Конспект" лицензируется только для личного пользования и использования в некоммерческих целях. Любое другое использование без согласия правообладателя запрещено.

![fastapi](https://blog.yezz.me/static/images/blog/07/01.png)
<div align="center">
    <p>&copy; 2024 Magomedali Magomedov. All rights reserved.</p>
</div>