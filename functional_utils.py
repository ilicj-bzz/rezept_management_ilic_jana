from functools import reduce
from unicodedata import normalize


# A1F, B4G, B4F: Filter nach Zutat
def apply_filters(recipes, ingredient):
    # B3G: Einfacher Lambda-Ausdruck zur Normalisierung des Suchbegriffs
    normalized_ingredient = lambda x: normalize('NFKD', x.lower())
    ingredient = normalized_ingredient(ingredient)

    # B4F: Kombination von Map, Filter und Reduce (obwohl hier nicht explizit Reduce verwendet wird)
    # B2E: Verwendung von Funktionen als Objekte und Argumente, Anwendung von Closures

    return list(filter(
        lambda r: any(normalized_ingredient(ingr) in normalized_ingredient(ingredient) for ingr in r.ingredients),
        recipes
    ))


# B4E: Aggregation der Rezeptnamen
def sort_recipes(recipes):
    return sorted(recipes, key=lambda r: r.name)


# B4E: Aggregation der Anzahl der Schritte über alle Rezepte
def total_steps(recipes):
    return reduce(lambda acc, recipe: acc + len(recipe.steps), recipes, 0)
