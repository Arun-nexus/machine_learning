import pandas as pd
import os
import requests
import datetime

API_ID="f3ea175a"
API_KEY="eaa480a05e96324249b5ad419fd89288"
file = "details.xlsx"


if os.path.exists(file):
    df = pd.read_excel(file)
    if df.isnull().values.any() or df.empty:
        user_input = True  
    else:
        user_input = False 
else:
    user_input = True 
if user_input:
    personal = {
        "name": input("Enter your name: "),
        "age": int(input("Enter your age: ")),
        "height": int(input("Enter your height in cm: ")),
        "weight": int(input("Enter your weight in kg: ")),
        "gender": int(input("Choose your gender:\n1. Male\n2. Female\n")),
        "type" : int(input("choose your dietary type\n1. vegetarian\n2.eggetarian\n3.non-vegetarian")),
        "disease": int(input("Do you have any disease?\n1. Heart Issue\n2. Diabetes\n3. None\n")),
        "exercise": int(input("Choose your daily workout:\n1. Intense\n2. High\n3. Medium\n4. Light\n")),
    }
    df = pd.DataFrame([personal])
    df.to_excel(file, index=False)
    print("congo your detwils was listed \n")
else:
    print("User details already exist.\n")
    personal = df.iloc[0].to_dict()  


if personal["gender"] == 1:  
    calorie_in = int((10 * personal["weight"]) + (6.25 * personal["height"]) - (5 * personal["age"]) + 5)
elif personal["gender"] == 2:  
    calorie_in = int((10 * personal["weight"]) + (6.25 * personal["height"]) - (5 * personal["age"]) - 161)
else:
    print("Invalid gender selection.")
    calorie_in = 0


protein = personal["weight"] * 0.75 
protein=format(protein,".2f")
carbs = (calorie_in / 100) * 45.65  
carbs=format(carbs,".2f")
fat = (calorie_in / 100) * 30 
fat = format(fat,".2f")
water_in=personal["weight"] * 0.035
water_in=format(water_in,".2f")
calcium=1000
if personal["gender"] == 1:
    if personal["age"]<18:
        calcium=1300
elif personal["gender"] == 1:
    if (personal["age"]>18) and personal["age"]>70:
        calcium=1000
elif personal["gender"] == 1:
    if personal["age"]>70:
        calcium=1300
elif personal["gender"] == 2:
    if personal["age"]<18:
        calcium=1300
elif personal["gender"] == 2:
    if personal["age"]>18 and personal["age"]<50:
        calcium=1000
elif personal["gender"] == 2:
    if personal["age"]>50:
        calcium=1300

if personal["type"]==1:
    dish="vegetarian"
else:
    dish=""

if os.path.exists(nutrition):
    nutrit=pd.read_excel(nutrition)
    last_updated = nutrit.iloc[0]["date"]
else:
    last_updated = None
today = datetime.date.today().strftime("%Y-%m-%d")
if last_updated!=today:
    water_take=0.00
    protein_take=0.00
    carbs_take=0.00
    fat_take=0.00
    calorie_take=0.00
    calcium_take=0.00
    data_save = pd.DataFrame([{
        "date": today,
        "water": water_take,
        "protein": protein_take,
        "carbs": carbs_take,
        "fat": fat_take,
        "calories": calorie_take,
        "calcium": calcium_take
    }])
    data_save.to_excel(nutrition, index=False)
else:
    water_take = nutrit.iloc[0]["water"]
    protein_take = nutrit.iloc[0]["protein"]
    carbs_take = nutrit.iloc[0]["carbs"]
    fat_take = nutrit.iloc[0]["fat"]
    calorie_take = nutrit.iloc[0]["calories"]
    calcium_take = nutrit.iloc[0]["calcium"]
def water(water_take):
    return water_take + 0.20
def suggest(target):
    
    url = "https://trackapi.nutritionix.com/v2/search/instant"
    headers = {
        "x-app-id": API_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params={"query": f"{dish}food which have with weight{float(protein)-protein_take}g, Carbs: {float(carbs)-carbs_take}g, Fat: {float(fat)-fat_take}g, Total Calories: {float(calorie_in)-calorie_take}kcal"})

    if response.status_code == 200:
        foods = response.json().get("common",[])
        print("\n Suggested meals to reach your calorie goal:")
        for item in foods[:5]:  
            print(f"{item['food_name'].title()}")
    else:
        print("\nError fetching meal suggestions.") 

def view_nutrition_progress():
   
    print("Nutrition Progress")
    print(f"Calories: {calorie_take:.2f} kcal / {calorie_in} kcal ({(calorie_take / calorie_in) * 100:.2f}%)")
    print(f"Protein: {protein_take:.2f}g / {protein}g ({(protein_take / float(protein)) * 100:.2f}%)")
    print(f"Carbs: {carbs_take:.2f}g / {carbs}g ({(carbs_take / float(carbs)) * 100:.2f}%)")
    print(f"Fat: {fat_take:.2f}g / {fat}g ({(fat_take / float(fat)) * 100:.2f}%)")
    print(f"Water: {water_take:.2f}L / {water_in}L ({(water_take / float(water_in)) * 100:.2f}%)")
    print(f"Calcium: {calcium_take:.2f}mg / {calcium}mg ({(calcium_take / calcium) * 100:.2f}%)")
       
calorie_goal=calorie_in

if __name__=="__main__":
    while(1):
        
        try:
            print("1. if you eat something\n""2. if you dring water\n""3. calories recommended to complete your goal\n4.total progress of your calories")
        
            choice=int(input(" "))
            if choice==1:


                eat=input("enter your meal name with weight:")
                
                
                
                url="https://trackapi.nutritionix.com/v2/natural/nutrients"
                headers = {"x-app-id": API_ID,"x-app-key": API_KEY, "Content-Type": "application/json"}
                data = {"query":eat}
                response=requests.post(url,json=data,headers=headers)
                if response.status_code== 200:
                    nutrients = response.json()
                    for item in nutrients["foods"]:
                        print(f"{item['food_name'].title()} - {item['serving_weight_grams']}g:")
                        print(f"Calories: {item['nf_calories']} kcal")
                        print(f"Protein: {item['nf_protein']}g")
                        print(f"Carbs: {item['nf_total_carbohydrate']}g")
                        print(f"Fat: {item['nf_total_fat']}g")

                        
                        calorie_take += item['nf_calories']
                        protein_take += item['nf_protein']
                        carbs_take += item['nf_total_carbohydrate']
                        fat_take += item['nf_total_fat']
                
                else:
                    print("\nError fetching nutritional data. Please try again.")


            elif choice==2:
                water_take=water(water_take)
            
            elif choice == 3:
                print(f"for your diet you want Protein: {float(protein)-protein_take}g, Carbs: {float(carbs)-carbs_take}g, Fat: {float(fat)-fat_take}g, Total Calories: {float(calorie_in)-calorie_take}kcal")
                remaining_calories = calorie_in - calorie_take
                if remaining_calories > 0:
                    suggest(remaining_calories)
                else:
                    print("You have reached your calorie goal!")
            elif choice == 4:
                view_nutrition_progress() 
            elif choice == 5:
                print("exiting program.stay healthy")
                break
            data_=pd.DataFrame([{
                "date": today,
                "water": water_take,
                "protein": protein_take,
                "carbs": carbs_take,
                "fat": fat_take,
                "calories": calorie_take,
                "calcium": calcium_take
            }])
            data_.to_excel(nutrition, index=False)
        except:
             print("may be you enter something wrong...pls restart the system")