import re
from datetime import timedelta, datetime
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import random
random.seed()

login = input("Введите логин: ")
passwd = input("Введите пароль: ")
browser = webdriver.Chrome("/home/viktor_/PycharmProjects/MyProjects/instabot/chromedriver")


# ПАРАМЕТРЫ
like_time = 10  # время между каждым лайком
all_likes = 1000  # за сутки
all_subscriptions = 500  # за сутки
hour_like = 50  # максимальное число лайков за час
hour_sub = 25  # максимальное число подписок за час


# в этом часу уже есть
likes = 0
subsciptions = 0


# функция проверки существования элемента на странице
def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


# вход в аккаунт
browser.get("https://www.instagram.com/accounts/login/")
time.sleep(2)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(login)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(passwd)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[4]').click()
time.sleep(3)
# input("Подтвердите код и нажмите любую клавишу")

# считывание файла отфильтрованных пользователей
with open("filtered_persons_list.txt", "r") as f:
    file_list = []
    for line in f:
        file_list.append(line)

# считывание листа с моими подписками
subscriptions_list = []
with open("my_subscriptions.txt", "r") as f1:
    for line in f1:
        subscriptions_list.append(line)

j = 0  # номер вывода в терминале
n = 0  # пропущенное число пользователей из=за совпадения в subscriptions_list
next_person = 0  # если true - следующий пользователь по циклу
start_time = time.time()  # время начала цикла


# ЦИКЛ
for person in file_list:

    # Условие для паузы цикла
    if likes >= all_likes:
        print("Предел числа лайков за сутки")
        break
    if subsciptions >= all_subscriptions:
        print("Предел числа подписок за сутки")
        break
    # максимальное число подписок в час
    if ((time.time() - start_time) <= 60*60) and (hour_sub <= subsciptions):
        print("Предел числа подписок в час")
        print("Подождите", int(60*60 - (time.time() - start_time)/60), "мин.")

        # удаление из отфильтрованных пользователей тех, на которых уже произвелись подписка
        with open("filtered_persons_list.txt", "w") as f:
            for i in range(j, len(file_list)):
                f.write(file_list[i])

        time.sleep(60*60 - (time.time() - start_time))
        start_time = time.time()
        subsciptions = 0
        likes = 0

    # максимальное число лайков в час
    if ((time.time() - start_time) <= 60*60) and (hour_like <= likes):
        print("Предел числа лайков в час")
        print("Подождите", int((60*60 - (time.time() - start_time))/60), "мин.")

        # удаление из отфильтрованных пользователей тех, на которых уже произвелись подписка
        with open("filtered_persons_list.txt", "w") as f:
            for i in range(j, len(file_list)):
                f.write(file_list[i])

        time.sleep(60*60 - (time.time() - start_time))
        start_time = time.time()
        subsciptions = 0
        likes = 0

    # обнуление часа
    if time.time() - start_time >= 60*60:
        start_time = time.time()
        subsciptions = 0
        likes = 0

    # сравнение с массивом подписок
    for line in subscriptions_list:
        next_person = 0
        if person == line:
            next_person = 1
            print(j + 1, "\tПодписка от этого человека уже есть")
            j += 1
            n +=1
            break
    if next_person == 1:
        continue

    # вывод в терминал номера
    j += 1
    print("\n" + str(j - n) + ": ")

    # открытие страницы пользователя
    browser.get(person)
    time.sleep(1.5)

    # 1) открытие публикаций и лайки

    # проверка есть ли уже подписка на этого пользователя
    element = "//section/main/div/header/section/div[1]/div[1]/span/span[1]/button"
    if xpath_existence(element) == 1:
        try:
            follow_status = browser.find_element_by_xpath(element).text
        except StaleElementReferenceException:
            print("Ошибка, код ошибки: 1.0")
            continue
        if (follow_status == "Following") or (follow_status == "Подписки"):
            print("Вы уже подписаны на этого пользователя\n")
            continue

    # поиск публикаций и открытие двух случайных, лайки
    element = "//a[contains(@href, '/p/')]"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 1.1")
        continue
    posts = browser.find_elements_by_xpath(element)
    i = 0
    for post in posts:
        posts[i] = post.get_attribute("href")
        i += 1
    rand_post = random.randint(0, 5)  # случайный 1-5 пост
    for i in range(2):
        browser.get(posts[rand_post + i])
        time.sleep(0.3)
        browser.find_element_by_xpath("//section/main/div/div/article/div[2]/section[1]/span[1]/button").click()
        likes += 1
        print("+1 лайк")
        time.sleep(like_time)

    # 2) Подписка на пользователя
    try:
        element = "//section/main/div/div/article/header/div[2]/div[1]/div[2]/button"
        if xpath_existence(element) == 0:
            print(j, "Ошибка, код ошибки: 2.0")
        try:
            browser.find_element_by_xpath(element).click()
        except StaleElementReferenceException:
            print(j, "Ошибка, код ошибки: 2.1")
            continue
    except ElementClickInterceptedException:
        print(j, "Ошибка, код ошибки: 2.2")
        continue

    subsciptions += 1
    print("+1 Подписка", person[0:len(person)-1])
    time.sleep(0.5)

    # запись новой подписки в файл подписок
    with open("my_subscriptions.txt", "a") as f:
        f.write(person)

# конец цикла


# with open("filtered_persons_list.txt", "w") as f:
#     for i in range(j, len(file_list)):
#         f.write(file_list[i])


# завершение работы
browser.quit()
