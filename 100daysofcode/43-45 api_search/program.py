import api
import webbrowser

def main():
    query = input('What do you want to search: ')
    results = api.search(query)

    print(f'There are {len(results)} results found.')
    for r in results:
        print(f"id {r.id} - {r.title}")

    display = input('Enter id episode for show up some details: ')
    for i in results:
        if i.id == int(display):
            print(f"\nCategory: {i.category}\n"
                  f"id: {i.id}\n"
                  f"url: {i.url}\n"
                  f"title: {i.title}\n"
                  f"description: {i.description}")
            url_list = ['https://talkpython.fm', i.url]
            full_url = ''.join(url_list)
            if i.category == 'Episode':
                webbrowser.open(full_url, new=2)

if __name__ == '__main__':
    main()
