import sys


def solve():

    g, s= map(int, input().split())
    W = input()
    S = input()

    if g > len(S):
        print(0)
        return

    # Предварительно вычисляем индексы для всех символов S
    # Преобразуем строку в массив индексов
    indices = [0] * len(S)

    for i, ch in enumerate(S):
        if 'a' <= ch <= 'z':
            indices[i] = ord(ch) - ord('a') + 26
        else:
            indices[i] = ord(ch) - ord('A')

    print(indices)
    # Индексы для W
    need = [0] * 52
    for ch in W:
        if 'a' <= ch <= 'z':
            need[ord(ch) - ord('a') + 26] += 1
        else:
            need[ord(ch) - ord('A')] += 1

    print(need)
    window = [0] * 52
    bad = 0

    # Инициализация первого окна
    for i in range(g):
        window[indices[i]] += 1

    # Подсчёт bad
    for i in range(52):
        if window[i] != need[i]:
            bad += 1

    ans = 1 if bad == 0 else 0

    # Скользящее окно с использованием предвычисленных индексов
    for i in range(g, len(S)):
        left = indices[i - g]
        right = indices[i]

        # Удаляем левый
        if window[left] == need[left]:
            bad += 1
        window[left] -= 1
        if window[left] == need[left]:
            bad -= 1

        # Добавляем правый
        if window[right] == need[right]:
            bad += 1
        window[right] += 1
        if window[right] == need[right]:
            bad -= 1

        if bad == 0:
            ans += 1

    print(ans)


if __name__ == "__main__":
    solve()
