# face-authentication

<img src=https://img.shields.io/badge/python-3.9-blue>

Приложение для аутентификации человека по его лицу. На вход программе подаётся изображение с веб-камера компьютера, на выходе она должна сообщить, проходит ли человек аутентификацию или нет.

## Установка и запуск
Для установки требуется Python версии 3.9 или выше.

1. Клонировать репозиторий: 
```
git clone https://github.com/advatrix/face-authentication.git
```

2. Желательно активировать виртуальное окружение:
```bash
python -m venv env
source env/bin/activate
```
3. Установить зависимости (PySide2, OpenCV):
```
pip install requirements.txt
```
4. Запустить приложение с использованием графического пользовательского интерфейса (GUI):
```
python gui_manager.py
```
---
A simple opencv-based face authentication app
