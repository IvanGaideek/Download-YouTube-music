# pip install selenium pytube fake-useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pytube import YouTube
from random import choices
import time
import re
import os

site_url = "https://www.youtube.com/watch?v=NiR_EJhRteU&list=PLfQAe5M2BkwBHqCIuLr0d-zqUZ49pBeKt"
prefix = "https://www.youtube.com"
directory = "music"

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")
# options.add_argument("--headless")
browser = webdriver.Chrome(options=options)


def slugify(docname,
               slash_replace='-',  # слэш: заменять на минус; используется в идентификаторах документов: типа № 1/2
               quote_replace='',  # кавычки: замены нет - удаляем
               multispaces_replace='\x20',  # множественные пробелы на один пробел
               quotes="""“”«»'\""""  # какие кавычки будут удаляться
               ):
    docname = re.sub(r'[' + quotes + ']', quote_replace, docname)
    docname = re.sub(r'[/]', slash_replace, docname)
    docname = re.sub(r'[|*?<>:\\\n\r\t\v]', '', docname)  # запрещенные символы в windows
    docname = re.sub(r'\s{2,}', multispaces_replace, docname)
    docname = docname.strip()
    docname = docname.rstrip('-')  # на всякий случай
    docname = docname.rstrip('.')  # точка в конце не разрешена в windows
    docname = docname.strip()  # не разрешен пробел в конце в windows
    return docname


def download_music(url):
    yt = YouTube(url, use_oauth=True)
    try:
        stream = yt.streams.get_by_itag(251)
        stream.download(output_path=directory, filename=slugify(yt.title) + ".mp3")
        # os.rename(directory + "/" + yt.video_id + ".webm", directory + "/" + yt.title + ".mp3")
        print("Трек скачан!")
    except Exception as ex:
        print("Этот трек не получается загрузить. " + str(ex))


def finds_url_videos():
    try:
        videos = browser.find_elements(By.ID, "wc-endpoint")
        selection = choices(videos, k=30)
        print("Загрузка треков...")
        for video in selection:
            download_music(prefix + video.get_attribute("href"))
        return "Треки загружены!"
    except Exception as ex:
        return "Упс! Что-то пошло не так." + "\n" + str(ex)


def main():
    browser.get(site_url)
    browser.maximize_window()
    time.sleep(3)
    print(finds_url_videos())
    browser.quit()


if __name__ == "__main__":
    main()
