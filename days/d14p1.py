from utils.parse import Parser
from itertools import groupby
from collections import deque
from operator import itemgetter


def is_direct_ore_product(recipes, name):
    _, ings = recipes[name]
    return all(ing == 'ORE' for ing, _ in ings)


parser = Parser("Day 14: Space Stoichiometry - Part 1")
parser.parse()
with parser.input as input:
    split = (l.strip().split('=>') for l in input)
    recipes = {}
    for ingredients, product in split:
        ings = ingredients.strip().split(', ')
        tmp = (el.split() for el in ings)
        ings = [(name, int(amount)) for amount, name in tmp]

        product_amount, product_name = product.split()

        recipes[product_name] = int(product_amount), ings

current_searchspace = deque([('FUEL', 1)])
surpluses = {}
direct_ore_products = []
while current_searchspace:
    name, amount = current_searchspace.popleft()

    unit, ingredients = recipes[name]
    available_surplus = surpluses.get(name, 0)
    reduced_amount = max(amount - available_surplus, 0)
    remaining_surplus = max(available_surplus - amount, 0)
    mod = reduced_amount % unit
    produced_recipes = reduced_amount // unit + (1 if mod > 0 else 0)
    produced_surplus = unit - mod if mod > 0 else 0
    new_surplus = remaining_surplus + produced_surplus

    surpluses[name] = new_surplus

    if produced_recipes > 0:
        requirements = ((n, a * produced_recipes)
                        for n, a in ingredients if n != 'ORE')
        current_searchspace.extend(requirements)

        if is_direct_ore_product(recipes, name):
            direct_ore_products.append((name, produced_recipes))

sorted_products = sorted(direct_ore_products, key=itemgetter(0))
accumulated = {n: sum(v[1] for v in vals)
               for n, vals in groupby(sorted_products, key=itemgetter(0))}

ore_recipes = {
    name: sum(v for _, v in recipes[name][1]) for name in accumulated.keys()}

required_ore = sum(n_recipes * ore_recipes[name]
                   for name, n_recipes in accumulated.items())

print(required_ore)
