from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def initialize_driver():
    # Инициализация драйвера Chrome
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)  # Ожидание загрузки элементов
    return driver


def search_wikipedia(driver, query):
    # Открытие сайта Википедии
    driver.get("https://www.wikipedia.org/")

    # Поиск строки поиска и ввод запроса
    search_input = driver.find_element(By.NAME, "search")
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)

    time.sleep(2)  # Ожидание загрузки результатов поиска

    # Получение списка найденных ссылок
    #links = driver.find_elements(By.CSS_SELECTOR, "ul.mw-search-results li a")
    links = driver.find_elements(By.XPATH, "//div[@class='mw-search-result-heading']/a")
    #links = browser.find_elements(By.XPATH, "//div[@class='mw-search-result-heading']/a")
    return links


def print_links(links):
    # Вывод списка ссылок
    for i, link in enumerate(links):
        print(f"{i}: {link.text} - {link.get_attribute('href')}")


def choose_link(links):
    # Запрос у пользователя выбора ссылки
    choice = int(input("Введите номер статьи, которую хотите открыть: "))
    return links[choice].get_attribute('href')


def print_sections(driver):
    # Получение и вывод списка разделов
    #sections = driver.find_elements(By.CSS_SELECTOR, "h2 .mw-headline")
    sections = driver.find_elements(By.CSS_SELECTOR, ".mw-heading2")
    for section in sections:
        print(section.text)


def print_paragraphs(driver):
    # Получение и вывод абзацев статьи
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    for paragraph in paragraphs:
        print(paragraph.text)


def print_article_links(driver):
    # Получение и вывод ссылок в статье
    article_links = driver.find_elements(By.CSS_SELECTOR, "a:not(.mw-jump-link)")
    for link in article_links:
        href = link.get_attribute('href')
        if href and 'http' in href:
            print(href)

def print_ext_url(driver):
    ext_urls = driver.find_elements(By.CSS_SELECTOR, "a.external")
    for ext_url in ext_urls:
        href = ext_url.get_attribute('href')
        if (href and 'http' in href) and (ext_url.get_attribute('text')!='Архивировано') and (ext_url.get_attribute('text')!='арх.'):
            print(f"{ext_url.get_attribute('text')} {href}")

def main():
    # Инициализация драйвера
    driver = initialize_driver()

    try:
        # Запрос у пользователя строки поиска
        query = input("Введите строку поиска: ")

        # Поиск и вывод ссылок
        links = search_wikipedia(driver, query)
        print_links(links)

        # Выбор ссылки и переход по ней
        article_url = choose_link(links)
        driver.get(article_url)

        while True:
            print("\nВыберите действие:")
            print("1: Показать список разделов")
            print("2: Показать список ссылок")
            print("3: Показать статью по абзацам")
            print("4: Показать ссылки на источники")
            print("9: Новый поиск")
            print("0: Выйти")
            action = input("Введите номер действия: ")

            if action == "1":
                print_sections(driver)
            elif action == "2":
                print_article_links(driver)
            elif action == "3":
                print_paragraphs(driver)
            elif action == "4":
                print_ext_url(driver)
            elif action == "9":
                query = input("Введите строку поиска: ")
                links = search_wikipedia(driver, query)
                print_links(links)
                article_url = choose_link(links)
                driver.get(article_url)
            elif action == "0":
                break
            else:
                print("Неверный ввод. Пожалуйста, попробуйте снова.")
    finally:
        # Закрытие драйвера
        driver.quit()

if __name__ == "__main__":
    main()