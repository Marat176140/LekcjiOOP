# import requests
# import json

# def fetch_nasa_images(query):
#     url = "https://images-api.nasa.gov/search"

#     params_query = {
#         'q': query
#     }

#     response = requests.get(url,params=params_query)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f'Nie udalo sie pobrac danych, kod status: {response.status_code}')

# # data = fetch_nasa_images('sun')
# # print(json.dumps(data, indent=4))

# def main():
#     query = input("Podaj zapytanie: ") # To nam wyswitla terminal z trzescia zadania do wykonania
#     try:
#         data = fetch_nasa_images(query)
#         items = data.get('collection', {}).get('items', [])
#         if not items:
#             print("Brak wynikow dla podanego zapytania.")
#             return

#         for item in items[:5]:
#             item_data = item.get('data', [])

#             if item_data:
#                 title = item_data[0].get('title', 'Brak tytulu')
#                 print(f"Tytul:  {title}")

#             link = item.get('link', [])

#             if link:
#                 href = link[0].get("href", "Brak linku")
#                 print(f"link: {href}")

#             print("-" * 40)
    


        

        

#     except Exception as e:
#         print(f"Wystapił błąd: {e}")


# if __name__ == "__main__":
#     main()




# import requests
# import json

# def fetch_nasa_images(query):
#     url = "https://images-api.nasa.gov/search"
#     params_query = {'q': query}
    
#     response = requests.get(url, params=params_query)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f'Nie udało się pobrać danych, kod statusu: {response.status_code}')

# def main():
#     query = input("Podaj zapytanie: ")  # Pobranie zapytania od użytkownika
#     try:
#         data = fetch_nasa_images(query)
#         items = data.get('collection', {}).get('items', [])
        
#         if not items:
#             print("Brak wyników dla podanego zapytania.")
#             return

#         for item in items[:5]:
#             item_data = item.get('data', [])

#             title = "Brak tytułu"
#             if item_data and isinstance(item_data, list):
#                 title = item_data[0].get('title', 'Brak tytułu')

#             print(f"Tytuł: {title}")

#             links = item.get('links', [])
#             href = "Brak linku"
#             if links and isinstance(links, list):
#                 href = links[0].get("href", "Brak linku")

#             print(f"Link: {href}")
#             print("-" * 40)

#     except Exception as e:
#         print(f"Wystąpił błąd: {e}")

# if __name__ == "__main__":
#     main()





import requests
import json

class NasaAPI:
    def __init__(self, query): 
        self.url = "https://images-api.nasa.gov/search"
        self.query = query
        self.params = {'q': self.query}

    def fetch_data(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Nie udało się pobrać pliku: {response.status_code}')

    def get_images(self):
        data = self.fetch_data()
        return data.get("collection", {}).get("items", [])

def main():
    query = input("Podaj zapytanie: ")
    try:
        nasa_api = NasaAPI(query)
        items = nasa_api.get_images()

        if not items:
            print("Brak wyników")
            return
        
        for item in items[:5]:
            item_data = item.get("data", [])
            title = item_data[0].get("title", "Brak tytułu") if item_data else "Brak tytułu"

            links = item.get("links", []) 
            href = links[0].get("href", "Brak linku") if links else "Brak linku"

            print(f"Tytuł: {title}")
            print(f"Link: {href}")
            print("-" * 40)
    
    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":  
    main()
