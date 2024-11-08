from flask import Flask, render_template, request, redirect, url_for

from functional_utils import sort_recipes
from models import Recipe

app = Flask(__name__)

# Datenbank der Rezepte als Liste
recipes = []


def initialize_recipes():
    recipes.append(Recipe(id=0, name="Spaghetti Bolognese",
                          ingredients=["Spaghetti", "Rinderhackfleisch", "Tomatensauce", "Zwiebeln", "Knoblauch"],
                          instructions=["Nudeln kochen", "Fleisch anbraten", "Sauce hinzufügen"]))
    recipes.append(Recipe(id=1, name="Caesar Salad",
                          ingredients=["Römersalat", "Hähnchenbrust", "Caesar Dressing", "Parmesan", "Croutons"],
                          instructions=["Salat waschen", "Hähnchen anbraten", "Dressing hinzugeben"]))
    recipes.append(
        Recipe(id=2, name="Tomatensuppe", ingredients=["Tomaten", "Zwiebeln", "Knoblauch", "Brühe", "Basilikum"],
               instructions=["Zwiebeln und Knoblauch anbraten", "Tomaten hinzufügen", "Mit Brühe aufkochen"]))
    recipes.append(Recipe(id=3, name="Pancakes", ingredients=["Mehl", "Milch", "Eier", "Backpulver", "Zucker"],
                          instructions=["Zutaten vermischen", "Teig in Pfanne geben", "Beidseitig braten"]))
    recipes.append(
        Recipe(id=4, name="Avocado Toast", ingredients=["Avocado", "Brot", "Salz", "Pfeffer", "Zitronensaft"],
               instructions=["Brot toasten", "Avocado zerdrücken", "Auf Brot verteilen"]))


# Rezepte initialisieren
initialize_recipes()


@app.route('/')
def index():
    """# B1G: Algorithmus erklären
    Zeigt alle Rezepte an, sortiert nach Namen.
    """
    sorted_recipes = sort_recipes(recipes)
    return render_template('index.html', recipes=sorted_recipes)


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    """# B3E: Lambda-Ausdrücke zur Steuerung des Programmflusses
    Fügt ein neues Rezept hinzu und verwendet Lambda-Ausdrücke zur Datenverarbeitung.
    """
    if request.method == 'POST':
        # Verwenden von Lambda-Ausdrücken zur sicheren Verarbeitung der Eingaben
        get_form_field = lambda field: request.form.get(field, '').strip()

        name = get_form_field('name')
        ingredients = list(filter(lambda x: x, get_form_field('ingredients').split(
            ',')))  # B3F: Lambda-Ausdruck mit mehreren Argumenten
        instructions = list(filter(lambda x: x, get_form_field('instructions').split(',')))

        if name and ingredients and instructions:
            # Generieren einer eindeutigen ID für das neue Rezept
            new_id = max(map(lambda r: r.id, recipes), default=-1) + 1

            new_recipe = Recipe(id=new_id, name=name, ingredients=ingredients, instructions=instructions)
            recipes.append(new_recipe)
            return redirect(url_for('index'))
        else:
            return render_template('add_recipe.html', error="Bitte füllen Sie alle Felder aus.")

    return render_template('add_recipe.html')


@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # B1F: Ich kann Algorithmen in funktionale Teilstücke aufteilen
    # C1G: Refactoring-Techniken verwendet, um den Code lesbarer und verständlicher zu machen
    # C1F: Refaktorisierter Code zur Verbesserung der Lesbarkeit und Wartbarkeit
    # C1E: Sicherstellen, dass das Refactoring keine unerwünschten Nebeneffekte einführt
    recipe = next((r for r in recipes if r.id == recipe_id), None)

    if recipe is None:
        return render_template('error.html', message="Rezept nicht gefunden")

    if request.method == 'POST':
        # B4G: Ich kann die Funktionen Map, Filter und Reduce einzeln auf Listen anwenden
        name = request.form.get('name', '').strip()
        ingredients = list(map(str.strip, request.form.get('ingredients', '').split(',')))
        instructions = list(filter(bool, map(str.strip, request.form.get('instructions', '').split(','))))

        if name and ingredients and instructions:
            # B2G: Ich kann Funktionen als Objekte behandeln und diese in Variablen speichern und weitergeben
            updated_recipe = Recipe(id=recipe_id, name=name, ingredients=ingredients, instructions=instructions)

            # B1E: Ich kann Funktionen in zusammenhängende Algorithmen implementieren
            for i, r in enumerate(recipes):
                if r.id == recipe_id:
                    recipes[i] = updated_recipe
                    break

            return redirect(url_for('index'))
        else:
            return render_template('edit_recipe.html', recipe=recipe, error="Bitte füllen Sie alle Felder aus.")

    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/filter', methods=['POST'])
def filter_recipes():
    """
    # B2F: Funktionen als Argumente
    # A1G: Beispiel einer Funktion mit Rückgabewert, im Gegensatz zu einer Prozedur
    """
    search_term = request.form['ingredient'].lower()  # Wir behalten den Namen 'ingredient' für die Kompatibilität bei

    def apply_filters(recipes_list, term):
        return [recipe for recipe in recipes_list
                if term in recipe.name.lower()
                or any(term in ingredient.lower() for ingredient in recipe.ingredients)]

    filtered_recipes = apply_filters(recipes, search_term)
    return render_template('index.html', recipes=filtered_recipes, filtered=True)  # A1G: Rückgabewert


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """# B3E: Lambda-Ausdrücke zur Steuerung des Programmflusses
    Zeigt Details eines bestimmten Rezepts an.
    """
    try:
        # Verwenden eines Lambda-Ausdrucks, um das richtige Rezept zu finden
        recipe = next(filter(lambda r: r.id == recipe_id, recipes), None)
        if recipe:
            return render_template('recipe_detail.html', recipe=recipe)
        else:
            raise IndexError
    except IndexError:
        return render_template('error.html', message="Ungültige Rezept-ID")


if __name__ == '__main__':
    app.run(debug=True)
