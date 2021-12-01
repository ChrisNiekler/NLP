import bs4
import requests

def get_page_content():
    url = input("URL: ")
    
    emotion = get_emotion()
   
    response = requests.get(url)

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        tag = get_tag()

        pars = soup.find_all(tag)

        status_texts = [t.getText() for t in pars]

        cut_until_first_status(status_texts)

        cut_after_last_status(status_texts)
    
        title = get_title(soup)
    

        write_data_to_file(emotion, status_texts, title)

def write_data_to_file(emotion, status_texts, title):
    with open(f'{title}.txt', 'w', encoding='utf-8') as content:
        for status in status_texts:
            if status == "":
                continue

            if not "," in status:
                content.write(status + f",{emotion}\n")
            else:
                content.write('"' + status +f'",{emotion}\n')

def get_title(soup):
    title = soup.find('title').string
    for char in r' \/:*"<>|+=-':
        title = title.replace(char, "")
    return title

def cut_after_last_status(status_texts):
    last = input("What is the last status?: ")
    last_i = len(status_texts) -1
    if last in status_texts:
        print("last status found")
        last_i = status_texts.index(last)
        del status_texts[last_i+1:]
    else:
        print("not found")

def cut_until_first_status(status_texts):
    first = input("What is the first status?: ")
    first_i = 0
    if first in status_texts:
        print("First status found")
        first_i = status_texts.index(first)
        del status_texts[:first_i]
    else:
        print("not found")

def get_tag():
    mode = input("Please select mode!\n[p] - paragraph tags\nli - list item tags\nany - costom tag e.g. h5, h4... \n  ")
    if mode == "":
        mode = "p"     
    print(f"Selected tag is {mode}")
    return mode

def get_emotion():
    emo = ["sad", "happy", "angry", "neutral", ""]
    while True:
        emotion = input("emotion? sad-0, happy-1, angry-2, neutral-3, not-applicable-4: ")
        if emotion in '0123':
            emotion = emo[int(emotion)]
            print(f"Emotion is {emotion}")
            break
        if emotion == '4':
            emotion = ""
            break
    return emotion

while True:
    get_page_content()
    answer = input("again? [y]|n \n")
    print(answer)
    print(answer.lower())
    if not answer.lower() in ["yes", "y", ""]:
        break
