from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def initialize_driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)  # Ожидание загрузки элементов
    return driver


def search_wikipedia(driver, query):
    driver.get("https://www.wikipedia.org/")

    search_input = driver.find_element(By.NAME, "search")
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)

    links = driver.find_elements(By.XPATH, "//div[@class='mw-search-result-heading']/a")
    return links


def print_links(links):
    for i, link in enumerate(links):
        print(f"{i}: {link.text} - {link.get_attribute('href')}")


def choose_link(links):
    choice = int(input("Введите номер статьи, которую хотите открыть: "))
    return links[choice].get_attribute('href')


def print_sections(driver):
    sections = driver.find_elements(By.CSS_SELECTOR, ".mw-heading2")
    for section in sections:
        print(section.text)


def print_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    for paragraph in paragraphs:
        print(paragraph.text)


def print_article_links(driver):
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
    driver = initialize_driver()
    try:
        query = input("Введите строку поиска: ")
        links = search_wikipedia(driver, query)
        print_links(links)
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
        driver.quit()

if __name__ == "__main__":
    main()