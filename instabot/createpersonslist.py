from selenium import webdriver
import time

login = input("Введите логин: ")
passwd = input("Введите пароль: ")
target_group = "https://www.instagram.com/smkventilyatcia/"
all = 500

browser = webdriver.Chrome(r"/home/viktor_/PycharmProjects/MyProjects/instabot/chromedriver")
browser.get("https://www.instagram.com/")

# вход в аккаунт
browser.get("https://www.instagram.com/accounts/login/")
time.sleep(3)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(login)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(passwd)
browser.find_element_by_xpath('//section/main/div/article/div/div[1]/div/form/div[4]').click()
time.sleep(3)
# input("Подтвердите код и нажмите любую клавишу")

# действия на сайте
browser.get(target_group)
time.sleep(1)
but_folowwers = '//section/main/div/header/section/ul/li[2]/a'
browser.find_element_by_xpath(but_folowwers).click()  # открытие списка подписчиков
time.sleep(2)
element = browser.find_element_by_xpath("/html/body/div[4]/div/div[2]")  # прокручиваемый элемент

# начальная плавная прокрутка
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 6, element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 4, element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 3, element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 2, element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 1.4, element)
time.sleep(0.8)

pers = []  # массив ссылок на пользователей
t = 0.7  # ожидание после каждой прокрутки
num_scroll = 0  # количество совершенных прокруток
p = 0  # коэфф для ожидания при 2000, 4000... пользователей


while len(pers) < all:
    num_scroll += 1
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
    if num_scroll % 10 == 0:
        print("!")
        # сохранение пользователей в массив
        persons = browser.find_elements_by_xpath("//div[@role='dialog']/div[2]/ul/div/li/div/div/div/div/a[@title]")
        for i in range(len(persons)):
            if str(persons[i].get_attribute("href")) not in pers:
                pers.append(str(persons[i].get_attribute("href")))
    time.sleep(t)

    # ожидание
    if len(pers) > (2000 + 1000 * p):
        print("\nОжидание 10 мин.")
        time.sleep(60 * 10)
        p += 1

with open('persons_list.txt', 'w') as f:
    for person in pers:
        f.write(person)
        f.write("\n")

# закрытие браузера
browser.quit()
