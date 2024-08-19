import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gutenberg.org"

def fetch_main_categories():
    url = f"{BASE_URL}/ebooks/bookshelf/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = {}

    bookshelf_div = soup.find('div', class_="bookshelves")

    for ul in bookshelf_div.find_all('ul'):
        for li in ul.find_all('li'):
            link = li.find('a')
            if link:
                categories[link.text.strip()] = BASE_URL + link['href']
    return categories

def fetch_subcategories(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    subcategories = {}
    suggestions = {}

    subcategories_results = soup.find('ul', class_="results")

    if subcategories_results:
        for li in subcategories_results.find_all('li', class_="navlink"):
            if 'grayed' in li.get('class', []):
                continue
            link = li.find('a')
            if link:
                # ignore any span classes
                for span in li.find_all('span', class_="extra"):
                    span.decompose()
                    
                # check for suggestions -- "Did you mean?"
                if 'did you mean' in li.text.lower():
                    suggestions[link.text.strip()] = BASE_URL + link['href']
                else:
                    subcategories[link.text.strip()] = BASE_URL + link['href']
        return subcategories, suggestions

"""
def fetch_ebooks(subcategory_url):
    response = requests.get(subcategory_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ebooks = {}
    
    for li in soup.select('li.booklink'):
        link = li.find('a')
        title = li.find('span', class_='title')
        if link and title:
            ebooks[title.text.strip()] = BASE_URL + link['href']
    
    return ebooks

def scrape_and_save_ebook(book_url, output_filename):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    files_table = soup.find('table', class_='files')

    if files_table:
        link = None
        for row in files_table.find_all('tr'):
            if 'Plain Text UTF-8' in row.get_text():
                link = row.find('a', href=True)
                break

        if link:
            book_url = "https:" + link['href']
            book_response = requests.get(book_url)
            if book_response.status_code == 200:
                with open(output_filename, 'w', encoding='utf-8') as file:
                    file.write(book_response.text)
                print(f"Book content saved successfully to {output_filename}!")
            else:
                print(f"Failed to retrieve the book content. Status code: {book_response.status_code}")
        else:
            print("Plain Text UTF-8 version not found.")
    else:
        print("Files table not found on the page.")
"""

def main():
    # Fetch and display main categories
    categories = fetch_main_categories()
    print("Main Categories:")
    for idx, category in enumerate(categories, start=1):
        print(f"{idx}. {category}")

    category_choice = int(input("Choose a category number: ")) -1 

    # handle invalid input
    if category_choice < 0 or category_choice >= len(categories):
        print("Invalid choice. Please choose a valid number.")
        return

    category_url = list(categories.values())[category_choice]

    print(f'You selected: {list(categories.keys())[category_choice]}')

    # Fetch and display subcategories
    subcategories, suggestions = fetch_subcategories(category_url)

    if suggestions:
        print("\nSuggestions: ")
        for idx, suggestion in enumerate(suggestions, start=1):
            print(f'{idx}. {suggestion}')

    if subcategories:
        print("\nSubcategories:")
        for idx, subcategory in enumerate(subcategories, start=1):
            print(f"{idx}. {subcategory}")

        subcategory_choice = int(input("Choose a subcategory number: ")) - 1
        subcategory_url = list(subcategories.values())[subcategory_choice]

    # handle invalid input
        if subcategory_choice < 0 or subcategory_choice >= len(subcategories):
            print("Invalid choice. Please choose a valid number.")
            return

        subcategory_url = list(subcategories.values())[subcategory_choice]

        print(f'You selected: {list(subcategories.keys())[subcategory_choice]}')
    else:
        print("No subcategories were found for this category.")

"""
    # Fetch and display ebooks
    ebooks = fetch_ebooks(subcategory_url)
    print("\nEbooks:")
    for idx, ebook in enumerate(ebooks, start=1):
        print(f"{idx}. {ebook}")

    ebook_choice = int(input("Choose an ebook number: ")) - 1
    ebook_url = list(ebooks.values())[ebook_choice]

    # Scrape and save the chosen ebook
    output_filename = input("Enter the output filename (with .txt extension): ")
    scrape_and_save_ebook(ebook_url, output_filename)
"""
    
if __name__ == "__main__":
    main()
