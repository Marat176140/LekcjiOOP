import requests

class SearchEngine:
    def __init__(self, api_url):
        self.api_url = api_url

    def search(self, query):
        params = {'q': query}
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Błąd zapytania: {e}")
            return None

    def display_results(self, query):
        results = self.search(query)
        if results and 'collection' in results and 'items' in results['collection']:
            print(f"Wyniki wyszukiwania dla '{query}':")
            for index, item in enumerate(results['collection']['items'], start=1):
                title = item.get('data', [{}])[0].get('title', 'Brak tytułu')
                link = item.get('links', [{}])[0].get('href', 'Brak linku')
                print(f"{index}. {title} - {link}")
        else:
            print("Nie udało się znaleźć wyników.")

if __name__ == "__main__":
    api_url = "https://images-api.nasa.gov/search"
    search_engine = SearchEngine(api_url)

    query = input("Wpisz zapytanie do wyszukiwania: ")
    search_engine.display_results(query)
