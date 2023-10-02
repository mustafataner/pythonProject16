import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Veritabanını yükleme
data = pd.read_csv("final_diyarbakır_data_unique(1).csv")

st.title("Bugün Ne Yesem?")

st.write("""
Diyarbakır'da yemek yemek için bir mekan arıyorsanız, size rastgele bir öneride bulunabiliriz! 
Lütfen konumunuzu girin ve gidebileceğiniz maksimum mesafeyi seçin.
""")

# Kullanıcının konumunu girmesi
user_location = st.text_input("Konumunuzu girin (örn. 37.945993, 40.161745):")

# Kullanıcının maksimum mesafeyi seçmesi
max_distance_km = st.slider("Maksimum Mesafe (km)", 1, 20, 5)

if st.button("Bugün Ne Yesem?"):
    if user_location:
        user_lat, user_lon = map(float, user_location.split(','))

        # Kullanıcının konumuna olan mesafeyi hesaplayın ve uygun mekanları seçin
        data['distance'] = data.apply(
            lambda row: geodesic((user_lat, user_lon), (row['latitude'], row['longitude'])).kilometers, axis=1)
        suitable_restaurants = data[data['distance'] <= max_distance_km]

        if not suitable_restaurants.empty:
            random_restaurant = suitable_restaurants.sample(1)
            restaurant_name = random_restaurant.iloc[0]['name']
            st.success(f"Bugün {restaurant_name} adlı restoranda yemek yiyebilirsiniz!")

            # Kullanıcının hedef restoranın enlem ve boylamını alın
            destination_lat = random_restaurant.iloc[0]['latitude']
            destination_lon = random_restaurant.iloc[0]['longitude']

            # Yol tarifi bağlantısı oluşturma
            directions_link = f"https://www.google.com/maps/dir/?api=1&destination={destination_lat},{destination_lon}"
            st.write(f"[Yol Tarifi Al]({directions_link})")
        else:
            st.warning("Seçilen mesafede uygun bir restoran bulunamadı.")

st.write("Her seferinde farklı bir öneri almak için butona tekrar basabilirsiniz.")



