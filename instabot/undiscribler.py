from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# время между отписками
unsub_time = 3
# количество отписок
max = 20

login = input("Введите логин: ")
passwd = input("Введите пароль: ")
browser = webdriver.Chrome("/home/viktor_/PycharmProjects/MyProjects/instabot/chromedriver")


# Функция проверки сууществования элемента на странице
def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


# Вход в аккаунт
browser.get("https://www.instagram.com/accounts/login/")
time.sleep(2)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(login)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(passwd)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[4]').click()
time.sleep(3)
# input("Подтвердите код и нажмите любую клавишу")


# чтение файла с подписками и сохранение данных данных в массив
file_list = []
with open("my_subscriptions.txt", "r") as f:
    for line in f:
        file_list.append(line)

# процесс отписки
i = 0
for line in file_list:
    i += 1
    if i == max + 1:
        break
    browser.get(line)
    element = "//section/main/div/header/section/div[1]/div[1]/span/span[1]/button"
    if xpath_existence(element) == 0:
        print("Ошибка 1 поиска кнопки отписки")
        continue
    try:
        button = browser.find_element_by_xpath(element)
    except StaleElementReferenceException:
        print("Ошибка 2 поиска кнопки отписки")
        continue

    if button.text == "Подписки":
        try:
            button.click()
        except StaleElementReferenceException:
            print("Ошибка 3 нажатия кнопки отписки")
            continue

    time.sleep(0.5)
    element = "/html/body/div[4]/div/div/div[3]/button[1]"
    if xpath_existence(element) == 0:
        print("Ошибка 4 поиска кнопки отписки")
        continue
    button = browser.find_element_by_xpath(element)
    try:
        button.click()
    except StaleElementReferenceException:
        print("Ошибка 5 нажатия кнопки")
        continue
    print("Произвелась отписка от", line)
    time.sleep(unsub_time)

# очистка списка моих подписок
with open("my_subscriptions.txt", "w") as f:
    i = 0
    for i in range(max, len(file_list)):
        f.write(file_list[i])
        i += 1

# завершение работы
browser.quit()

