С помощью этого приложения вы можете загрузить через админку джанги архив со статьей Тильды и потом посмотреть статью по адресу `http://localhost:8000/tilda/:id/`

Иллюстрирует возможности по интеграции `Tilda` и `Django`.

В моей версии контент и стили хранятся в базе данных, а статичные файлы распаковываются в папку внутри `MEDIA_ROOT` на сервере.

В момент вывода контент обрабатывается таким образом, чтобы статичные файлы загружались из распакованной папки.

Больше информации в статье: http://codepoetry.ru/post/tilda-django-integration/


## Установка

```
git clone git@github.com:dpetukhov/tilda-django.git
cd tilda-django/
virtualenv --python `which python3` env
. env/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

1. Дальше откройте http://127.0.0.1:8000/admin/tilda/tildaarticle/ и создайте новую статью.
2. Загрузите тестовый контент из файла `project1556959_1565771385.zip` в поле Импорт.
3. Откройте статью: http://127.0.0.1:8000/tilda/1/
