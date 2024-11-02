from database import create_tables
from frontend import main as run_frontend
from recipe_functions import add_recipe

if __name__ == "__main__":
    create_tables()
    run_frontend()
    
