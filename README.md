# Assembler
# Задание 4

Разработать ассемблер и интерпретатор для учебной виртуальной машины(УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задается из командной строки. Результатом работы ассемблера является бинарный файл в виде последовательности байт, путь к которому задается из командной строки. Дополнительный ключ командной строки задает путь к файлулогу, в котором хранятся ассемблированные инструкции в духе списков “ключ=значение”, как в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон также указывается из командной строки.

Форматом для файла-лога и файла-результата является csv.

Необходимо реализовать приведенные тесты для всех команд, а также написать и отладить тестовую программу

### Поддерживаемые инструкции
Реализованы следующие команды УВМ:

1. **Загрузка константы**
   - Код операции: `120`
   - Описание: Загружает константное значение в адрес памяти.
   - Размер инструкции: 5 байт.

2. **Чтение из памяти**
   - Код операции: `101`
   - Описание: Читает значение из одного адреса памяти и записывает в другой.
   - Размер инструкции: 5 байт.

3. **Запись в память**
   - Код операции: `36`
   - Описание: Записывает значение из одного адреса памяти в другой с учетом смещения.
   - Размер инструкции: 5 байт.

4. **Бинарная операция: "!="**
   - Код операции: `51`
   - Описание:  Оператор сравнения, который проверяет, различаются ли значения двух операндов.
   - Размер инструкции: 5 байт.

---

## Использование

### Ассемблирование
Преобразует исходный файл ассемблера в бинарный файл и генерирует файл лога.
```bash
python main.py assemble file.txt --output_file output.bin --log_file log.csv
```

### Интерпретация
Исполняет бинарную программу и сохраняет значения памяти в указанном диапазоне в файл результата.
```bash
python main.py interpret output.bin --result_file result.csv --memory_range 0:10
```

## Формат инструкций

### Загрузка константы
- **Код операции**: 120
- **Размер**: 5 байт
- **Описание**: Загружает константу в память.
- **Пример**:
  - Входные данные: `A=120, B=650`
  - Бинарный код: `0x78, 0x45, 0x01, 0x00, 0x00`

### Чтение из памяти
- **Код операции**: 101
- **Размер**: 5 байт
- **Описание**: Читает значение из одного адреса памяти и записывает в другой.
- **Пример**:
  - Входные данные: `A=101, B=289`
  - Бинарный код: `0x67, 0x15, 0x00, 0x80, 0xFF, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00`

### Запись в память
- **Код операции**: 36
- **Размер**: 5 байт
- **Описание**: Записывает значение из одного адреса памяти в другой с учетом смещения.
- **Пример**:
  - Входные данные: `A=36, B=814`
  - Бинарный код: `0x24, 0x97, 0x01, 0x00, 0x00`

### Бинарная операция: "!="
- **Код операции**: 51
- **Размер**: 5 байт
- **Описание**: Оператор сравнения, который проверяет, различаются ли значения двух операндов.
- **Пример**:
  - Входные данные: `A=51, B=355`
  - Бинарный код: `0xB3, 0xB1, 0x00, 0x00, 0x00`

 ## Пример работы

### Входной файл ассемблера
```assembly
120,650
101,289
36,814
51,355
```

## Логический файл

```assembly
A,B,Bytes
120,650,"[120, 138, 2, 0, 0]"
101,289,"[101, 33, 1, 0, 0]"
36,814,"[36, 46, 3, 0, 0]"
51,355,"[51, 99, 1, 0, 0]"

```

### Команды
```bash 
python main.py assemble file.txt --output_file output.bin --log_file log.csv
python main.py interpret output.bin --result_file result.csv --memory_range 0:10
```

