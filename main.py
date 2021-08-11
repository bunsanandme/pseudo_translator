import re
from pythonds.basic.stack import Stack
# Обьявим все контейнеры для хранения комманд, переменных.
# Собственно, вся логика интрепретации работает на них

variables = {}
commands = []
funcd = {}
save = []
list_of_keys = []


def postfix(infixexpr):
    priority_of_operations = {"*": 3, "/": 3, "%": 2, "+": 1, "-": 1, "(":0}
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (priority_of_operations[opStack.peek()] >= priority_of_operations[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


# Чтение файла и получение списка строк. 
# Аргументом является название файлы
def read_file(file_name):
  with open(file_name) as f:
    for line in f:
      if line[0] != '?': # Проверка, закоментированны ли строки 
        commands.append(line)

# Функция собирает логическое выражение и решает его, выводит True или False
def logical_eval(comm, lvl):
  del comm[0]
  for i in range(2, len(comm)):

    # Здесь идет замена на служебные слова python для функции eval()

    if comm[i] == "not":
      comm[i] = "!="

    elif comm[i] == "xor":
      comm[i] = "^"

    elif comm[i] == "eqv":
      comm[i] = "=="
  
  # Отрезаем "log:"
  comm_slice = comm[2:]
  final_expression = ' '.join(comm_slice)
  # Решаем лог.выражение и выводим его
  try:
    result = eval(final_expression)

    if result == 0:
      result = False

    if result == 1:
      result = True

    print("Ответ на логическое выражение '{}' = {}".format(final_expression, str(result)))
    variables[lvl][comm[0]] = result
  # Обработка ошибки ввода
  except Exception:
    print("Ошибка в введенных данных")

  return comm

# Функция для реализации присваивания переменных, получает два значения счетчика прохода по файлу
def assignment_variable(comm, lvl, first_iter, second_iter):
  if comm[second_iter + 1] == list_of_keys[0]:
    gg = re.sub(r'[^\w\s]', '', commands[first_iter])
    ggg = gg.split()
    lvl += 1
    variables[lvl] = {}
    # Добавляем в переменные
    for k in range(2, len(ggg)):
      variables[lvl][ggg[k]] = variables[lvl - 1][ggg[k]]
    abc = funcd[comm[second_iter + 1]] + 1

    work_with_variables(abc, lvl)

  else:
    add_variable(comm, lvl)

# Функция для вычисления математических значений
# Работает по такому же принципу, как и logical_eval()
def math_eval(comm, lvl):
  del comm[0]
  
  for i in range(2, len(comm)):
    try:
      comm[i] = variables[lvl][comm[i]]
      
    except Exception:
      continue
      
  comm_slice = comm[2:]
  final_expression = ' '.join(comm_slice)
  result = eval(final_expression)
  print("Постфиксная форма: ", postfix(str(final_expression)))
  print("Ответ на математическое выражение '{}' = {}".format(final_expression, result))
  variables[lvl][comm[0]] = result
  return comm


# Сохранение значения переменной
def add_variable(comm, lvl):
  try:
    int(comm[2])
    variables[lvl][comm[0]] = comm[2]
    
  except Exception:
    pass

# Основная функция для работы со строками программы
def work_with_variables(amp, lvl):
  # Разбивает программу на список
  for i in range(amp + 1, len(commands)-1):
    comm = commands[i].split()
    
    # В зависимости от ключевого слова выполняется функции, объявленная выше
    for j in range(0, 2):
      # Пользовательский ввод переменной для работы
        if comm[j] == "reader":
          input_result = input("Введите значение переменной = ")
          variables[lvl][comm[1]] = input_result
      # Вывод переменной
        elif comm[j] == "printer":
          print("Переменная '{}' = {}".format(comm[1], variables[lvl][comm[1]]))
      # Решение математических примеров
        elif comm[j] == "mat:":
          math_eval(comm, lvl)
          continue

      # Возврат функции
        elif comm[j] == "return":
          variables[0][save[2]] = variables[lvl][comm[1]]

      #Решение логических выражений
        elif comm[j] == "log:":
          logical_eval(comm, lvl)
          continue
      # Закрытие видимости, удаление значения словаря
        elif comm[j] == "}":
          if lvl > 1:
            del variables[lvl]
          lvl -= 1
      # Открытие видимости, добавление нового ключа
        elif comm[j] == "{":
          lvl += 1
          variables[lvl] = {}
      # Присваивание переменной значения
        elif comm[j] == ":=":
          assignment_variable(comm, lvl, i, j)


# Запуск всех функций, парсер функций и main
def main():
  global list_of_keys

  for i in range(len(commands)):
    comm = commands[i].split()

    if comm[0] == "def":
      funcd = {comm[1]: i}

    elif comm[0] == "main":
      amp = i
      lvl = 0
      variables[lvl] = {}
      list_of_keys = list(funcd.keys())
      work_with_variables(amp, lvl)

# Точка входа в программу, чтение файла и запуск программы
read_file('test.txt')
main()


