# Позиции букв. На вход программе подаются две непустые строки, содержащие хотя бы один символ. 
# Для каждой буквы из второй строки необходимо определить на каких позициях встречается эта буква в первой строке и вывести их на печать в формате: <буква> <номера позиций через пробел>.
Если буква не имеет вхождений, необходимо напечатать None вместо номеров позиций. Последовательность вывода букв должна соответствовать последовательности, в которой они встречаются во второй строке (то есть не должна измениться). Буквы в разных регистрах следует считать эквивалентными. 
Если некоторая буква входит во вторую строку несколько раз, вывод нужно сделать только для первого вхождения. К буквам относятся только буквы латинского алфавита a-z, A-Z.
 
# Примечание: гарантируется, что на вход программы подаются только символы латинского алфавита, цифр, пунктуации и спецсимволы.
 
 
# Пример работы программы:
# ________________________________________________
# Sample Input 1:
 
# Abracadabra
# Fabric
# ________________________________________________
# Sample Output 1:

#  f None
# a 1 4 6 8 11
# b 2 9
# r 3 10
# i None
# c 5
# ________________________________________________
# Sample Input 2:

# abc
# abA
#________________________________________________
# Sample Output 2:

# a 1
# b 2
#________________________________________________

# put your python code here

s1 = input().lower()
s2 = input().lower()

positions = {}
for i, char in enumerate(s1):
    if char.isalpha():
        if char not in positions:
            positions[char] = [i + 1]
        else:
            positions[char].append(i + 1)


seen = set()
for char in s2:
    if char.isalpha() and char not in seen:
        seen.add(char)
        if char in positions:
            print(f"{char} {' '.join(map(str, positions[char]))}")
        else:
            print(f"{char} None")
            