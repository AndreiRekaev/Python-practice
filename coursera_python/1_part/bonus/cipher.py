Шифр простой замены

Напишите программу для дешифровки сообщений, зашифрованных шифром простой замены . На вход программе подается зашифрованная строка и таблица дешифровки.

Таблица дешифровки - это последовательность символов, каждый из которых соотносится с соответствующим (по порядку) символом оригинального алфавита. Для наглядности, можно записать таблицу дешифровки и алфавит друг под другом:
cdefghijklmnopqrstuvwxyzab  # таблица дешифровки
abcdefghijklmnopqrstuvwxyz  # оригинальный алфавит
Такое расположение показывает соответствие букв из зашифрованного текста буквам оригинального текста. Например: символ j в зашифрованном тексте соответствует h оригинального.

Расшифруйте сообщения и выведите его на печать. Программа должна быть не чувствительна к регистру букв (все буквы исходного сообщения должны быть переведены в нижний регистр).
Пример работы программы:
_____________________________________________
Sample Input 1:

  jgnnq!
  cdefghijklmnopqrstuvwxyzab
_____________________________________________
Sample Output 1:

  hello!
_____________________________________________
Sample Input 2:

  lxt ybekr gdqhm cqj abnus qwtd lxt oipv zqf.
  igkztcfxearonmquydslbwhjvp
_____________________________________________
Sample Output 2:

  the quick brown fox jumps over the lazy dog.
_____________________________________________


def decrypt_message(ciphertext, decryption_table):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    decrypted_text = ''
    
    for char in ciphertext.lower():
        if char.isalpha():
            index = decryption_table.index(char)
            decrypted_text += alphabet[index]
        else:
            decrypted_text += char
    return decrypted_text

# Читаем зашифрованное сообщение и таблицу дешифровки
ciphertext = input().strip()
decryption_table = input().strip()

# Дешифруем сообщение
plaintext = decrypt_message(ciphertext, decryption_table)

print(plaintext)
