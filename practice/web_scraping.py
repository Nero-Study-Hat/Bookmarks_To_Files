from bs4 import BeautifulSoup

soup = BeautifulSoup()
with open('bookmarks_12_25_22.html') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

dt_items = soup.find_all('dt')
folder_name = ''
for item in dt_items:
    next_item = item.find_next()
    if next_item.name == 'h3':
        folder_name = next_item.text
        continue
    else:
        print(f'url = {next_item.get("href")}')
        print(f'website name = {next_item.text}')
        print(f'add date = {next_item.get("add_date")}')
        print(f'folder name = {folder_name}')
    print()