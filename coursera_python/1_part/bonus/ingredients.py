recipes = {'Бутерброд с ветчиной': {'Хлеб': 50, 'Ветчина': 20, 'Сыр': 20},
           'Салат Витаминный': {'Помидоры': 50, 'Огурцы': 20, 'Лук': 20, 'Майонез': 50, 'Зелень': 20}}

store = {'Хлеб': 250, 'Ветчина': 120, 'Сыр': 120,
         'Помидоры': 50, 'Огурцы': 20, 'Лук': 20,
         'Майонез': 50, 'Зелень': 20}

def check_portions(food, count, recipes=recipes, store=store):
    # напишите вашу реализацию функции здесь
    if food not in recipes:
        return 0, 0
    max_portions = float('inf')
    for ingredient, amount_per_portion in recipes[food].items():
        if ingredient in store:
            available_amount = store[ingredient]
            max_portions = min(max_portions, available_amount / amount_per_portion)
        else:
            return 0, 0

    possible_portions = int(max_portions)
    if possible_portions >= count:
        return 1, count
    else:
        return 0, possible_portions
