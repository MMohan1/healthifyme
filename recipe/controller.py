from models import Recipe, Ingrendient
import converter
SUPPORTED_MEASUREMENT_UNITS = ["KG", "G", "L", "ML"]


def calculate_pfcf_value(ingredients_data):
    """
    """
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_F = 0
    total_item = 0
    for ingredient in ingredients_data:
        total_item += 1
        unit = ingredient.get("measurement_units")
        name = ingredient.get("name")
        quantity = ingredient.get("quantity")
        if unit not in SUPPORTED_MEASUREMENT_UNITS:
            msg = "Please provide correct measurement units  for "+name
            return {"success": False, "message": msg}
        ingrendient = check_ingredient_pfcf(name)
        if not ingrendient.get("success"):
            return ingrendient
        func_name = unit + "_convert"
        protein, carbs, fat, F = getattr(converter, func_name)(quantity, ingrendient["data"]["protein"],
                                                               ingrendient["data"]["carbs"], ingrendient["data"]["fat"],
                                                               ingrendient["data"]["F"])
        ingrendient["protein"] = protein
        ingrendient["carbs"] = carbs
        ingrendient["fat"] = fat
        ingrendient["F"] = F
        total_protein += protein
        total_carbs += carbs
        total_fat += fat
        total_F += F
    return {"success": True, "data": {"protein": protein/float(total_item),
                                      "carbs": carbs/float(total_item),
                                      "fat": fat/float(total_item),
                                      "F": F/float(total_item),
                                      "ingredient": ingredient}}


def check_ingredient_pfcf(ingredient_name):
    """
    """
    ingrendient = Ingrendient.objects(name=ingredient_name).first()
    if not ingrendient:
        msg = "Please provide correct ingredient for "+ingredient_name
        return {"success": False, "message": msg}
    return {"success": True, "data": ingrendient.to_mongo().to_dict()}


def recipe_store(data):
    """
    """
    recipe_name = data.get("recipe_name")
    if not recipe_name:
        return {"success": False, "message": "Please provide the recipe name"}
    ingredients = data.get("ingredients_details")
    if not ingredients:
        return {"success": False, "message": "Please provide the ingredients"}
    if Recipe.objects(name=recipe_name).first():
        rcp = Recipe.objects(name=recipe_name).first()
    else:
        rcp = Recipe(name=recipe_name)
    pfcf_value = calculate_pfcf_value(ingredients)
    if not pfcf_value["success"]:
        return pfcf_value
    rcp.ingredients = pfcf_value["data"]["ingredient"]
    rcp.protein = pfcf_value["data"]["protein"]
    rcp.carbs = pfcf_value["data"]["carbs"]
    rcp.fat = pfcf_value["data"]["fat"]
    rcp.F = pfcf_value["data"]["F"]
    rcp.save()
    return {"success": True, "message": "recipe stored successfully"}


def get_recipe_details(name):
    """
    """
    data = Recipe.objects(name=name).only("name", "ingredients", "protein", "carbs", "fat", "F").exclude("_id").first()
    if not data:
        return {"success": False, "message": "Recipe is not stored"}
    all_data = data.to_mongo().to_dict()
    all_data.pop("inserted_at")
    return {"success": True, "data": all_data}

def delete_recipe_details(name):
    """
    """
    data = Recipe.objects(name=name).first()
    if not data:
        return {"success": False, "message": "Recipe is not stored"}
    data.delete()
    return {"success": True, "message": "data deleted successfully"}
