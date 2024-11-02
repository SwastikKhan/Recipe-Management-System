import streamlit as st
import urllib.parse
import os
from recipe_functions import add_recipe, get_recipe, get_all_recipes, update_recipe, delete_recipe

def generate_share_links(recipe_name, recipe_id):
    base_url = os.environ.get('RECIPE_APP_URL', 'http://localhost:8501')
    recipe_url = f"{base_url}?recipe_id={recipe_id}"
    encoded_name = urllib.parse.quote(recipe_name)
    encoded_url = urllib.parse.quote(recipe_url)

    whatsapp_link = f"https://api.whatsapp.com/send?text={encoded_name}%20-%20{encoded_url}"
    facebook_link = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
    twitter_link = f"https://twitter.com/intent/tweet?text={encoded_name}&url={encoded_url}"

    return {
        "whatsapp": whatsapp_link,
        "facebook": facebook_link,
        "twitter": twitter_link,
        "direct": recipe_url
    }

def display_recipe(recipe_id):
    recipe_details = get_recipe(recipe_id)
    if recipe_details:
        st.subheader(recipe_details['name'])
        st.write(f"**Instructions:** {recipe_details['instructions']}")
        st.write("**Ingredients:**")
        for ingredient in recipe_details['ingredients']:
            st.write(f"- {ingredient['name']}: {ingredient['quantity']}")

        # Add sharing options
        st.subheader("Share this recipe")
        share_links = generate_share_links(recipe_details['name'], recipe_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Share on WhatsApp"):
                st.markdown(f"[Open WhatsApp]({share_links['whatsapp']})")
        with col2:
            if st.button("Share on Facebook"):
                st.markdown(f"[Open Facebook]({share_links['facebook']})")
        with col3:
            if st.button("Share on Twitter"):
                st.markdown(f"[Open Twitter]({share_links['twitter']})")
        
        st.text("Or copy this link:")
        st.code(share_links['direct'])
    else:
        st.error("Recipe not found.")

def add_recipe_ui():
    st.subheader("Add a New Recipe")
    recipe_name = st.text_input("Recipe Name")
    instructions = st.text_area("Cooking Instructions")
    
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []
    
    st.write("Current Ingredients:")
    for idx, ing in enumerate(st.session_state.ingredients):
        st.write(f"{idx + 1}. {ing['name']} - {ing['quantity']}")

    with st.form(key='add_ingredient'):
        ingredient_name = st.text_input("Ingredient Name")
        ingredient_quantity = st.text_input("Ingredient Quantity")
        submit_ingredient = st.form_submit_button("Add Ingredient")

        if submit_ingredient and ingredient_name and ingredient_quantity:
            st.session_state.ingredients.append({"name": ingredient_name, "quantity": ingredient_quantity})
            st.success(f"Added: {ingredient_name} - {ingredient_quantity}")

    if st.button("Save Recipe"):
        if recipe_name and instructions and st.session_state.ingredients:
            recipe_id = add_recipe(recipe_name, instructions, st.session_state.ingredients)
            st.success(f"Recipe '{recipe_name}' added successfully!")
            st.session_state.ingredients = []
        else:
            st.warning("Please fill in all fields and add at least one ingredient.")

def view_recipes_ui():
    st.subheader("View Recipes")
    recipes = get_all_recipes()
    recipe_choice = st.selectbox("Select a recipe", [recipe["name"] for recipe in recipes])
    
    if recipe_choice:
        selected_recipe = next(recipe for recipe in recipes if recipe["name"] == recipe_choice)
        display_recipe(selected_recipe["id"])

def update_recipe_ui():
    st.subheader("Update Recipe")
    recipes = get_all_recipes()
    recipe_to_update = st.selectbox("Select a recipe to update", [recipe["name"] for recipe in recipes])
    
    if recipe_to_update:
        selected_recipe = next(recipe for recipe in recipes if recipe["name"] == recipe_to_update)
        recipe_details = get_recipe(selected_recipe["id"])
        
        updated_name = st.text_input("Recipe Name", value=recipe_details["name"])
        updated_instructions = st.text_area("Cooking Instructions", value=recipe_details["instructions"])
        
        if 'update_ingredients' not in st.session_state:
            st.session_state.update_ingredients = recipe_details["ingredients"]
        
        st.write("Current Ingredients:")
        for idx, ing in enumerate(st.session_state.update_ingredients):
            st.write(f"{idx + 1}. {ing['name']} - {ing['quantity']}")

        with st.form(key='update_ingredient'):
            ingredient_name = st.text_input("New Ingredient Name")
            ingredient_quantity = st.text_input("New Ingredient Quantity")
            submit_ingredient = st.form_submit_button("Add Ingredient")

            if submit_ingredient and ingredient_name and ingredient_quantity:
                st.session_state.update_ingredients.append({"name": ingredient_name, "quantity": ingredient_quantity})
                st.success(f"Added: {ingredient_name} - {ingredient_quantity}")

        if st.button("Update Recipe"):
            update_recipe(recipe_details["id"], updated_name, updated_instructions, st.session_state.update_ingredients)
            st.success(f"Recipe '{updated_name}' updated successfully!")
            st.session_state.update_ingredients = get_recipe(recipe_details["id"])["ingredients"]

def delete_recipe_ui():
    st.subheader("Delete Recipe")
    recipes = get_all_recipes()
    recipe_to_delete = st.selectbox("Select a recipe to delete", [recipe["name"] for recipe in recipes])
    
    if recipe_to_delete:
        selected_recipe = next(recipe for recipe in recipes if recipe["name"] == recipe_to_delete)
        if st.button(f"Delete {recipe_to_delete}"):
            delete_recipe(selected_recipe["id"])
            st.success(f"Recipe '{recipe_to_delete}' deleted successfully!")

def main():
    st.title("Recipe Management System")

    # Check if a specific recipe is being requested
    recipe_id = st.query_params.get("recipe_id")
    if recipe_id:
        display_recipe(recipe_id)
    else:
        menu = ["Home", "Add Recipe", "View Recipes", "Update Recipe", "Delete Recipe"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            st.subheader("Welcome to the Recipe Management System")
            st.write("Use the sidebar to navigate through different functions.")
        elif choice == "Add Recipe":
            add_recipe_ui()
        elif choice == "View Recipes":
            view_recipes_ui()
        elif choice == "Update Recipe":
            update_recipe_ui()
        elif choice == "Delete Recipe":
            delete_recipe_ui()

if __name__ == "__main__":
    main()