from functools import wraps
from collections import namedtuple
from collections import defaultdict

statistics = defaultdict(list)
Order = namedtuple('Order', ['success', 'portions'])

def collect_statistics(statistics):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      food = args[0]
      count = args[1]
      response_code, portions = func(*args, **kwargs)
      statistics[food].append(Order(response_code, count if response_code == 1 else count - portions))
      return response_code, portions
    return wrapper
  return decorator
        
@collect_statistics(statistics)
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
