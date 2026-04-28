n,k=map(int,input().split())
a=list(map(int,input().split()))
pref=[0]*(n+1)
ans=0
# min - список минимальных префиксных сумм с РАЗНЫМИ остатками
# min[0] - глобальный минимум
# min[1] - второй минимум, но только если его остаток отличается от остатка min[0]
# Изначально есть только пустой префикс (сумма 0)
min_vals = [0]

for i in range(n):
    # Шаг 1: Вычисляем префиксную сумму до i+1
    pref[i + 1] = pref[i] + a[i]

    # Шаг 2: Пытаемся найти максимальную сумму подмассива, заканчивающегося в i
    # Подмассив [l+1, i] имеет сумму = pref[i+1] - pref[l]

    # Пробуем вычесть глобальный минимум (min_vals[0])
    if (pref[i + 1] - min_vals[0]) % k != 0:
        # Если разница НЕ делится на k - отлично!
        ans = max(ans, pref[i + 1] - min_vals[0])
    elif len(min_vals) == 2:
        # Если с глобальным минимумом разница делится на k,
        # пробуем со вторым минимумом (у него другой остаток)
        ans = max(ans, pref[i + 1] - min_vals[1])

    # Шаг 3: Обновляем список минимальных префиксных сумм
    # Нужно сохранить две наименьшие суммы с РАЗНЫМИ остатками

    # Случай 1: текущая сумма меньше глобального минимума
    if pref[i + 1] < min_vals[0]:
        temp = min_vals[0]  # сохраняем старый минимум

        # Обновляем глобальный минимум
        min_vals[0] = pref[i + 1]

        # Если у нас всего один элемент в списке
        if len(min_vals) == 1:
            # Добавляем старый минимум, если его остаток отличается от нового
            if min_vals[0] % k != temp % k:
                min_vals.append(temp)
        # Если уже есть два элемента
        elif len(min_vals) == 2:
            # Заменяем второй элемент на старый минимум, если остатки разные
            if min_vals[0] % k != temp % k:
                min_vals[1] = temp

    # Случай 2: текущая сумма между min[0] и min[1]
    elif len(min_vals) == 2 and pref[i + 1] < min_vals[1]:
        # Обновляем второй минимум, только если его остаток отличается от первого
        if pref[i + 1] % k != min_vals[0] % k:
            min_vals[1] = pref[i + 1]

    # Случай 3: у нас всего один элемент, и текущая сумма больше min[0]
    elif len(min_vals) == 1:
        # Добавляем текущую сумму как второй элемент, если остаток отличается
        if pref[i + 1] % k != min_vals[0] % k:
            min_vals.append(pref[i + 1])
print(ans)



n, k = map(int, input().split())
a = list(map(int, input().split()))
pref_sum = [0] * (n + 1)
a = [0] + a
min_sum = [0]
ans = 0
for i in range(1, n + 1):
    pref_sum[i] = pref_sum[i - 1] + a[i]
    min_sum.append(pref_sum[i])
    min_sum.sort()
    for j in range(len(min_sum) - 1, 0, -1):
        if min_sum[j] % k == min_sum[j - 1] % k:
            min_sum.pop(j)
            break
    min_sum = min_sum[:2]
    for ms in min_sum:
        if ms % k != pref_sum[i] % k:
            ans = max(ans, pref_sum[i] - ms)
print(ans)

