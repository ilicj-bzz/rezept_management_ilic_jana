class Recipe:
    #A1F Immutable (String), Mutable (List)
    # A1E: Beispiel für OOP-Ansatz.
    def __init__(self, id, name, ingredients, instructions):
        self.id = id
        self.name = name  # Immutable (String)
        self.ingredients = ingredients  # Mutable (List)
        self.instructions = instructions  # Mutable (List)


def __repr__(self):
    return f"<Recipe(name={self.name})>"
