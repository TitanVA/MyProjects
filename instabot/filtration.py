import re
from datetime import timedelta, datetime
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# параметры
days = 30  # количество допустимых дней с момента публикации
acc_subscriptions = 55500  # количество допустимых подписок у аккаунта
publications = 10  # необходимый минимум публикаций
today = datetime.now()
site = 'OFF'  # 'ON' - если есть сайт не добавляет, 'OFF' - добавляет

# функция проверки существования элемента на странице
def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


browser = webdriver.Chrome("/home/viktor_/PycharmProjects/MyProjects/instabot/chromedriver")

# считываение из файла всех ссылок на пользователей
with open('persons_list.txt', 'r') as f:
    file_list = []
    for line in f:
        file_list.append(line)

# ОБРАБОТКА ССЫЛОК

# 1) аккаунт должен быть публичным
# 2) у аккаунта не должно быть более указанного числа подписок
# 3) не должно быть ссылки на сайт
# 4) необходимо фото профиля
# 5) необходимо не менее 10 публикаций в профиле
# 6) последняя публикация не менее days дней назад


filtered_list = []
i = 0  # количество подходящий пользователей
j = 0  # номер вывода в терминале

for person in file_list:
    j += 1
    browser.get(person)
    time.sleep(0.4)

    # 1) проверка на закрытость аккаунта
    element = "//section/main/div/div/article/div[1]/div/h2"
    if xpath_existence(element) == 1:
        try:
            if browser.find_element_by_xpath(element).text == "This Account is Private" \
                    or "Это закрытый аккаунт":
                print(j, "Приватный аккаунт")
                continue
        except StaleElementReferenceException:
            print("Ошибка, код ошибки: 1")

    # 2) Проверка на допустимое число подписок
    element = "//section/main/div/header/section/ul/li[3]/a/span"
    if xpath_existence(element) == 0:
        print("Ошибка, код ошибки: 2")
        continue
    status = browser.find_element_by_xpath(element).text
    status = re.sub(r'\s', '', status)  # удаление пробелов из числа подписок
    if int(status) > acc_subscriptions:
        print(j, "У аккаунта слишком много подписок")
        continue

    # 3) Не должно быть ссылки на сайт
    if site == 'ON':
        element = "//section/main/div/header/section/div[2]/a"
        if xpath_existence(element) == 1:
            print(j, "Есть ссылка на сайт")
            continue

    # 4) Проверка на наличие как минимум заданного кол-ва публикаций
    element = "//section/main/div/header/section/ul/li[1]/a/span"

    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 4")
        continue
    status = browser.find_element_by_xpath(element).text
    status = re.sub(r'\s', '', status)  # удаление пробелов из числа подписок
    if int(status) < publications:
        print(j, "У аккаунта слишком мало публикаций")
        continue

    # 5) проверка на наличие аватарки
    element = "//section/main/div/header/div/div/span/img"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 5")
        continue
    status = browser.find_element_by_xpath(element).get_attribute("src")
    if status.find("s150x150") == -1:
        print(j, "Профиль без аватарки")
        continue

    # 6) Проверка на дату последней публикации
    element = "//a[contains(@href, '/p/')]"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 6")
        continue
    status = browser.find_element_by_xpath(element).get_attribute("href")
    browser.get(status)
    post_date = browser.find_element_by_xpath("//time").get_attribute("datetime")
    year = int(post_date[0:4])
    month = int(post_date[5:7])
    day = int(post_date[8:10])
    post_date = datetime(year, month, day)
    period = today - post_date
    if period.days > days:
        print(j, "Последняя публикация была очень давно")
        continue

    # ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В ОТФИЛЬТРОВАННЫЙ ФАЙЛ
    filtered_list.append(person)
    print(j, "Добавлен новый пользователь", person)
    i += 1
    #
    # if i > 3:
    #     break

# ВЫХОД ИЗ ЦИКЛА

# Запись в файл
with open("filtered_persons_list.txt", 'w') as f:
    for line in filtered_list:
        f.write(line)
print("\nДобавлено", i, "пользователей")
browser.quit()