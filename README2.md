Задание №1
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме CLI.
Конфигурационный файл имеет формат csv и содержит:

• Имя компьютера для показа в приглашении к вводу.

• Путь к архиву виртуальной файловой системы.

• Путь к лог-файлу.

Лог-файл имеет формат xml и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указаны дата и время.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. clear.
2. tree.
4. whoami.
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.
_____________________________________________________________________________________________________________________________
## 1. Запуск программы
```
python -m src.main --config config.csv
```
_____________________________________________________________________________________________________________________________
## 2. Тест работоспособности

##Запуск тестирования 

```
python -m unittest discover -s src/tests
```
Результат
![image](https://github.com/user-attachments/assets/73a3e43a-f795-4f49-a0e4-af2e50ebea4b)
