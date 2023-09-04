import requests, os, logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def main():
    logging.basicConfig(filename='main.py.log', encoding='utf-8', level=logging.DEBUG)
    def store_number(number: int):
        with open("chapter.txt", "w") as file:
            file.write(str(number))

    def read_number()->int:
        number = 0;
        with open("chapter.txt", "r") as file:
            number = file.read()
        return int(number)

    logging.info("getting content")
    url = "https://mangareader.to/one-piece-3"
    response = requests.get(url)
    html_content = response.content

    logging.info("parsing html")
    soup = BeautifulSoup(html_content, "html.parser")
    element_amt = 10
    count = 0
    target_content = []
    first_element = soup.find(class_="item reading-item chapter-item")
    current_element = first_element
    while current_element and count < element_amt:
        content = current_element.get_text()
        modified_content = content[3:-9]
        target_content.append(modified_content)
        count += 1
        current_element = current_element.find_next(class_="item reading-item chapter-item")

    chapter_numbers = []
    for i in target_content:
        item = i[8:]
        chapter_numbers.append(int(item[:4]))

    logging.info("sending webhook (if needed)")
    newest_chapter = max(chapter_numbers)
    if newest_chapter > read_number():
        store_number(newest_chapter)
        load_dotenv()
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if webhook_url is None:
            logging.info("Webhook URL not found in environment variables.")
        else:
            content = f'@everyone NEW ONEPICE CHAPTER "{{}}" IS OUT'.format(target_content[0][8:])
            message_data = { 'content': content }
            response = requests.post(webhook_url, json=message_data)
            if response.status_code == 204:
                print('Webhook sent successfully!')
            else:
                print('Failed to send webhook. Status code:', response.status_code)
                print('Response:', response.text)

if __name__ == "__main__":
    main()
