Только буквы.

Напишите  программу, на вход которой подается строка. Программа должна выбрать все буквы, встречающиеся в строке и вывести их в алфавитном порядке одной строкой (буквы должны быть в нижнем регистре), без пробелов и повторений на стандартный вывод. К буквам относятся только символы латинского алфавита (A-Z, a-z). Программа не должна быть чувствительна к регистру букв. 
Примечание: гарантируется, что на вход программы подаются только символы латинского алфавита, пунктуации и спецсимволы.
Пример работы программы:
____________________________________
Sample Input 1:

  Beautiful is better than ugly.
____________________________________
Sample Output 1:

  abefghilnrstuy
____________________________________
Sample Input 2:

  [Z-9ZZ%Z8__AA77]aazz(1234)
____________________________________
Sample Output 2:

  az
____________________________________


def only_letters():

    s = input().lower()
    
    unique_letters = set(char for char in s if char.isalpha())
   
    result = ''.join(sorted(unique_letters))
    
    print(result)



# Вызываем функцию
only_letters()