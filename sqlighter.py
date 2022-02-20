import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def get_suba(self, user_id, status = True):
        """Получаем нужного активного подписчика бота"""
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM `subscriptions` WHERE status = ? and user_id= ?", (status, user_id)).fetchall()
            

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET status=? WHERE user_id=?", (status, user_id))

    def add_user(self, user_id):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (user_id) VALUES(?)", (user_id,))        

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def add_city(self, user_id, city):
        """Добавляем город пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET city = ? WHERE user_id = ?", (city, user_id))
    
    def add_name(self, name, user_id):
        """Добавляем имя пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET name = ? WHERE user_id = ?", (name, user_id))
    
    def get_user_city(self, user_id):
        """Ищем город пользователя"""
        with self.connection:
            return self.cursor.execute("SELECT city FROM 'subscriptions' WHERE user_id = ?",(user_id,)).fetchall()

    def set_time(self, user_id, time):
        """Устанавливаем время рассылки"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET time = ? WHERE user_id = ?", (time, user_id))

    def get_time(self, user_id):
        """Берем время пользователя"""
        with self.connection:
            return self.cursor.execute("SELECT time FROM 'subscriptions' WHERE user_id = ? and status=True",(user_id,)).fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()