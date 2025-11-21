Установка:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Muta-Mad/async-foodgram.git
cd async-foodgram
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
Если у вас Linux/macOS
```
source venv/bin/activate
```
Если у вас windows
```
source venv/scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```
создать и применить миграции 
```
alembic revision --autogenerate -m "название миграции"
alembic upgrade head
```
запуск приложения
```
python main.py
```