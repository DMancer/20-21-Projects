import streamlit as st
from prettytable import PrettyTable
st.title('Simulator')
streamlit run streamlit_app.py

# Définition des valeurs possibles pour les colonnes "Build vs Target" et "Buildpace"
build_vs_target_values = ["Very Strong", "Strong", "On track", "Soft", "Very Soft"]
buildpace_values = ["quick", "slow"]

# Définition des stratégies de prix
strategies = {
    ("Very Strong", "quick"): 1.01,
    ("Very Strong", "slow"): 0.98,
    ("Strong", "quick"): 0.98,
    ("Strong", "slow"): 1.05,
    ("On track", "quick"): 1.05,
    ("On track", "slow"): 1.005,
    ("Soft", "quick"): 1.005,
    ("Soft", "slow"): 0.95,
    ("Very Soft", "quick"): 0.95,
    ("Very Soft", "slow"): 0.9,
}

# Fonction de calcul du prix final pour une combinaison donnée
def calculate_final_price(prices, build_vs_target, buildpace):
    third_concurrent_price = min(prices)

    if build_vs_target == "Very Strong" and buildpace == "quick":
        return prices[1] * strategies[("Very Strong", "quick")]
    elif build_vs_target == "Very Strong" and buildpace == "slow":
        return prices[1] * strategies[("Very Strong", "slow")]
    elif build_vs_target == "Strong" and buildpace == "quick":
        return prices[1] * strategies[("Strong", "quick")]
    elif build_vs_target == "Strong" and buildpace == "slow":
        return third_concurrent_price * strategies[("Strong", "slow")]
    elif build_vs_target == "On track" and buildpace == "quick":
        return third_concurrent_price * strategies[("On track", "quick")]
    elif build_vs_target == "On track" and buildpace == "slow":
        return third_concurrent_price * strategies[("On track", "slow")]
    elif build_vs_target == "Soft" and buildpace == "quick":
        return third_concurrent_price * (1 + 0.005)
    elif build_vs_target == "Soft" and buildpace == "slow":
        return third_concurrent_price * strategies[("Soft", "slow")]
    elif build_vs_target == "Very Soft" and buildpace == "quick":
        return third_concurrent_price * strategies[("Very Soft", "quick")]
    elif build_vs_target == "Very Soft" and buildpace == "slow":
        return third_concurrent_price * strategies[("Very Soft", "slow")]
    else:
        return third_concurrent_price  # Valeur par défaut si aucune condition n'est satisfaite

# Fonction de calcul du tableau de nouveaux prix en fonction des prix des concurrents
def calculate_final_prices(prices):
    table = PrettyTable()
    table.field_names = ["Build vs Target", "Buildpace", "New Price"]

    for build_vs_target in build_vs_target_values:
        for buildpace in buildpace_values:
            new_price = calculate_final_price(prices, build_vs_target, buildpace)
            table.add_row([build_vs_target, buildpace, round(new_price, 2)])

    return table

# Demander à l'utilisateur d'entrer les prix des concurrents
prices = []
for i in range(3):
    while True:
        try:
            price = float(input(f"Entrez le prix du concurrent {i+1}: "))
            if price > 0:
                prices.append(price)
                break
            else:
                print("Le prix doit être un nombre positif.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

# Calculer et afficher les nouveaux prix
result_table = calculate_final_prices(prices)
print(result_table)
