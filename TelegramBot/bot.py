import sys
import telebot
import mysql.connector
from mysql.connector import errorcode
import os


token = ''
bot = telebot.TeleBot(token)


group_id = '-1001279036503'
# print(bot.get_chat('@testviktorsgroup').id)


try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='123Titan',
        port='3306',
        database='youtube'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Wrong with user name or psswd')
        sys.exit()
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database does not exist')
        sys.exit()
    else:
        print(err)
        sys.exit()

cursor = db.cursor()
user_data = {}
#
# # cursor.execute("CREATE DATABASE dbbot")
# cursor.execute("CREATE TABLE regs (id INT AUTO_INCREMENT PRIMARY KEY, \
#                 first_name VARCHAR(255), last_name VARCHAR(255),\
#                 description VARCHAR(255),\
#                 user_id INT(11))")
# cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, \
#                 first_name VARCHAR(255), last_name VARCHAR(255),\
#                 telegram_user_id INT(11) UNIQUE)")


class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.description = ''


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Введите имя: ')
    bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Введите фамилию: ')
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        msg = bot.send_message(message.chat.id, 'Напишите описание: ')
        bot.register_next_step_handler(msg, process_description_step)
    except Exception as e:
        bot.reply_to(message, 'ooooops')


def process_description_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.description = message.text

        # Проверка есть ли пользователь в БД
        sql = 'SELECT * FROM users WHERE telegram_user_id = {0}'.format(user_id)
        cursor.execute(sql)
        existuser = cursor.fetchone()
        print(existuser)
        # Если нету то добавить
        if existuser == None:
            sql = 'INSERT INTO users (first_name, last_name, telegram_user_id) \
                                      VALUES (%s, %s, %s)'
            val = (message.from_user.first_name,
                   message.from_user.last_name, user_id)
            cursor.execute(sql, val)
        # Регистрация заявки
        sql = 'INSERT INTO regs (first_name, last_name, description, user_id) \
                                          VALUES (%s, %s, %s, %s)'
        val = (user.first_name, user.last_name, user.description, user_id)
        cursor.execute(sql, val)
        db.commit()
        bot.send_message(message.chat.id, 'вы успешно зарегистрированы!')
        bot.send_message(group_id, user.first_name + ' ' + user.last_name)
        with open(os.path.join(os.getcwd(), 'data', 'cats.jpg'), 'rb') as photo:
            bot.send_photo(group_id, photo)

    except Exception as e:
        bot.reply_to(message, 'ooooops')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()


if __name__ == '__main__':
    bot.polling(none_stop=True)
