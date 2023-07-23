import argparse
import sqlite3


class FoodBlog:
    create = 'CREATE TABLE IF NOT EXISTS'
    meals = 'meals (meal_id INTEGER PRIMARY KEY,meal_name TEXT NOT NULL UNIQUE);'
    ingredients = 'ingredients (ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT UNIQUE NOT NULL);'
    measures = 'measures (measure_id INTEGER PRIMARY KEY, measure_name TEXT UNIQUE);'
    recipes = 'recipes (recipe_id INTEGER PRIMARY KEY, recipe_name TEXT NOT NULL, recipe_description TEXT);'
    serve = 'serve (serve_id INTEGER PRIMARY KEY, recipe_id INTEGER NOT NULL, meal_id INTEGER NOT NULL,' \
            'FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id), FOREIGN KEY (meal_id) REFERENCES meals(meal_id));'
    quantity = 'quantity (quantity_id INTEGER PRIMARY KEY, quantity INTEGER NOT NULL, recipe_id INTEGER NOT NULL,' \
               'measure_id INTEGER NOT NULL, ingredient_id INTEGER NOT NULL,' \
               'FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id), ' \
               'FOREIGN KEY (measure_id) REFERENCES measures(measure_id),' \
               'FOREIGN KEY (ingredient_id) REFERENCES meals(ingredient_id));'
    tables = {meals, ingredients, measures, recipes, serve, quantity}
    data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
            "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
            "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

    def __init__(self, food_blog_db):
        self.conn = sqlite3.connect(food_blog_db)
        self.cur = self.conn.cursor()

    def create_tables(self):
        for table_name in self.tables:
            self.cur.execute(f'{self.create} {table_name}')
        for table in self.data:
            self.cur.execute(f"""INSERT INTO {table} ({table.rstrip('s')}_name) 
                            VALUES ('{"'), ('".join([value for value in self.data[table]])}');""")
        self.conn.commit()

    def input_data(self):
        print('Pass the empty recipe name to exit.')
        while recipe_name := input('Recipe name: '):
            recipe_description = input('Recipe description: ')
            self.cur.execute(f"INSERT INTO recipes (recipe_name, recipe_description)"
                             f"VALUES ('{recipe_name}', '{recipe_description}');")
            recipe_id = self.cur.execute(f"SELECT recipe_id FROM recipes WHERE recipe_name = '{recipe_name}'").lastrowid

            print(' '.join([f'{_id}) {meal}' for _id, meal in self.cur.execute(f"SELECT * FROM meals;").fetchall()]))
            input_meal_ids = input('When the dish can be served:').split()

            append = [f"({int(meal_id)}, '{recipe_id}')" for meal_id in input_meal_ids]
            self.cur.execute(f"INSERT INTO serve (meal_id, recipe_id) VALUES {', '.join(append)};")
            self.conn.commit()

            while quantity := input('Input quantity of ingredient <press enter to stop>: ').split():
                measure_id = self.cur.execute(f"SELECT measure_id FROM measures WHERE measure_name "
                                              f"like '{quantity[1] + '%' if len(quantity) == 3 else ''}'").fetchall()
                ingredient_id = self.cur.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient_name "
                                                 f"like '%{quantity[1 if len(quantity) == 2 else 2]}%'").fetchall()
                if len(measure_id) != 1 or len(ingredient_id) != 1:
                    lack_item = ' '.join(['measure' if len(measure_id) != 1 else '\b',
                                          'ingredient' if len(ingredient_id) != 1 else '\b'])
                    print(f"The {lack_item} is not conclusive!")
                    continue
                else:
                    self.cur.execute(f"INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id)"
                                     f"VALUES ({quantity[0]}, {recipe_id}, {measure_id[0][0]}, {ingredient_id[0][0]})")
                self.conn.commit()

    def select_recipe(self, meals, ingredients):
        sql = f"""SELECT recipes.recipe_id, recipes.recipe_name FROM recipes
        JOIN  quantity on recipes.recipe_id = quantity.recipe_id
        JOIN serve on serve.recipe_id = recipes.recipe_id
        JOIN meals on meals.meal_id = serve.meal_id
        JOIN ingredients on ingredients.ingredient_id = quantity.ingredient_id
        WHERE meals.meal_name in {tuple((str(meals) + ', ').split(','))} 
        and ingredients.ingredient_name in {tuple((str(ingredients) + ', ').split(','))}
        GROUP BY recipes.recipe_id
        HAVING COUNT(DISTINCT ingredients.ingredient_name) >= {len(str(ingredients).split(','))}"""

        recipe_commend = [recipe[1] for recipe in self.cur.execute(sql).fetchall()]
        print('Recipes selected for you: ' + ', '.join(recipe_commend) if recipe_commend else
              'There are no such recipes in the database.')


fb = argparse.ArgumentParser()
fb.add_argument('FoodBlogDB')
fb.add_argument('-igd', '--ingredients')
fb.add_argument('-m', '--meals')
# fb_arg = fb.parse_args()
fb_arg = fb.parse_args('food_.db -igd sugar,milk -m breakfast,brunch'.split())  # example2
# fb_arg = fb.parse_args('food_.db -igd sugar,milk,strawberry -m brunch'.split())  # example3
# fb_arg = fb.parse_args('food_.db -igd strawberry,sugar -m brunch,supper'.split())  # test3
# fb_arg = fb.parse_args('food_.db -igd milk,cacao -m brunch,breakfast'.split())  # ['Hot cacao', 'Hot cacao']

if fb_arg.ingredients is not None:
    FoodBlog(fb_arg.FoodBlogDB).select_recipe(fb_arg.meals, fb_arg.ingredients)
else:
    FoodBlog(fb_arg.FoodBlogDB).create_tables()
    FoodBlog(fb_arg.FoodBlogDB).input_data()
