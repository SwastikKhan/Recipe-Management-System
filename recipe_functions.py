from database import create_connection

def add_recipe(name, instructions, ingredients):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO recipes (name, instructions) VALUES (?, ?)", (name, instructions))
    recipe_id = cursor.lastrowid

    for ingredient in ingredients:
        cursor.execute("INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)",
                       (recipe_id, ingredient['name'], ingredient['quantity']))

    conn.commit()
    conn.close()
    return recipe_id

def get_recipe(recipe_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()

    if recipe:
        cursor.execute("SELECT name, quantity FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        ingredients = cursor.fetchall()
        
        return {
            "id": recipe[0],
            "name": recipe[1],
            "instructions": recipe[2],
            "ingredients": [{"name": ing[0], "quantity": ing[1]} for ing in ingredients]
        }
    
    conn.close()
    return None

def get_all_recipes():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM recipes")
    recipes = cursor.fetchall()

    conn.close()
    return [{"id": recipe[0], "name": recipe[1]} for recipe in recipes]

def update_recipe(recipe_id, name, instructions, ingredients):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE recipes SET name = ?, instructions = ? WHERE id = ?", (name, instructions, recipe_id))
    
    cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    
    for ingredient in ingredients:
        cursor.execute("INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)",
                       (recipe_id, ingredient['name'], ingredient['quantity']))

    conn.commit()
    conn.close()

def delete_recipe(recipe_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))

    conn.commit()
    conn.close()