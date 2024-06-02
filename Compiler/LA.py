# Константы для классов символов
LETTER = 0          # Класс для букв
NUMBER = 1          # Класс для чисел
UNKNOWN = 99        # Класс для неизвестных символов

# Открытие входного файла
program = open("programm.txt")  # Основной файл программы
data = program.read()           # Чтение данных из основного файла
len_data = len(data)            # Длина данных

# Инициализация глобальных переменных
charClass = 0       # Класс текущего символа
word = ''           # Текущее слово, которое формируется
nextChar = ''       # Следующий символ во входной строке
lexLen = 0          # Длина текущей лексемы
token = 0           # Идентификатор токена
nextElement = 0     # Следующий элемент во входной строке
charPos = 0         # Позиция текущего символа во входной строке
count_word = 1      # Счётчик для идентификаторов, начинается с 1

# Функция для считывания следующего символа и определения его класса
def getChar():
    global charPos, nextChar, charClass

    if charPos < len_data:
        nextChar = data[charPos]
        charPos += 1
    else:
        nextChar = None

    if nextChar is not None:
        if nextChar.isalpha():  # Проверяет наличие буквы
            charClass = LETTER
        elif nextChar.isdigit():  # Проверяет, состоит ли символ только из цифр
            charClass = NUMBER
        else:
            charClass = UNKNOWN
    else:
        charClass = None

# Функция для добавления символа к текущему слову
def addChar():
    global word
    if lexLen <= 98:  # Проверка на максимальную длину слова
        if word == ' ':
            word = nextChar
        else:
            word += nextChar
    else:
        print("Ошибка - слово слишком длинное \n")

# Функция для пропуска пробелов
def space_skip():
    global nextChar
    while nextChar is not None and nextChar.isspace():  # Проверка, является ли символ пробелом
        getChar()

# Основная функция для лексического анализа
def lex():
    global word, charClass, nextElement, count_word

    word = ''        # Сброс текущего слова
    lexLen = 0       # Сброс длины текущей лексемы
    space_skip()     # Пропуск пробелов

    if charClass == LETTER:
        while charClass in (LETTER, NUMBER):  # Пока символы буквы или цифры
            addChar()
            getChar()

    elif charClass == NUMBER:
        while charClass == NUMBER:  # Пока символы цифры
            addChar()
            getChar()

    elif charClass == UNKNOWN:
        addChar()
        getChar()

    elif charClass is None:
        nextElement = None


    # Ключевые слова и их идентификаторы
    keywords = {
        "integer": "(1,1)", "read": "(1,2)", "ass": "(1,3)", "writeln": "(1,4)",
        "if": "(1,5)", "then": "(1,6)", "else": "(1,7)", "for": "(1,8)",
        "to": "(1,9)", "do": "(1,10)", "real": "(1,11)", "boolean": "(1,12)",
        "while": "(1,13)", "{": "(2,1)", "}": "(2,2)", "(": "(2,4)", ":": "(2,5)",
        "=": "(2,6)", ">": "(2,7)", "<": "(2,8)", "+": "(2,9)", "/": "(2,10)",
        ",": "(2,11)", "<>": "(2,12)", "-": "(2,13)", "*": "(2,14)", "and": "(2,15)",
        "<=": "(2,16)", ">=": "(2,17)"
    }

    if word in keywords:                        # Для ключевых слов
        print(f"{keywords[word]} - {word}")
    elif word.isdigit():                        # Для числовых констант
        print(f"(4,{int(word)}) - {word}")
    elif word:                                  # Если слово не является пустой строкой (идентификатор)
        print(f"(3,{count_word}) - {word}")
        count_word += 1                         # Увеличиваем счётчик идентификаторов

    return nextElement

# Основная функция программы
def main():
    global count_word
    if not program:
        print("Ошибка, невозможно открыть файл \n")
    else:
        getChar()
        while nextElement is not None:
            lex()
    program.close()
    return 0

main()
