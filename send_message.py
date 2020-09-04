from API_Naumen import API_Naumen
import config
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class Send_message:
    driver = API_Naumen.driver

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.__auth()

    """Переопределить функцию с помощью наследования!!!!!!"""

    def enter_words(self, id_xpath_area, words, id_xpath_button=None, t=0.5):
        """Функция для заполнения полей по ID или XPATH
           При необходимости нажатие на кнопку. По-умолчанию без нажатия"""
        try:
            if id_xpath_area.startswith('//*[@'):
                self.driver.find_element_by_xpath(id_xpath_area).clear()
                self.driver.find_element_by_xpath(id_xpath_area).send_keys(words)
            else:
                self.driver.find_element_by_id(id_xpath_area).clear()
                self.driver.find_element_by_id(id_xpath_area).send_keys(words)
            time.sleep(t)

            if id_xpath_button:
                if id_xpath_button.startswith('//*[@'):
                    self.driver.find_element_by_xpath(id_xpath_button).click()
                else:
                    self.driver.find_element_by_id(id_xpath_button).click()
            time.sleep(t)
        except NoSuchElementException:
            raise NoSuchElementException('Вы находитесь в специфическом окне, где нельзя что либо вставить или нажать'
                                         'кнопку, может быть ошибка в пути')

    def __auth(self):
        self.driver.get('https://mail.pilot.ru')
        time.sleep(0.5)
        self.enter_words('//*[@id="username"]', self.login)
        self.enter_words('//*[@id="password"]', self.password, '//*[@id="lgnDiv"]/div[9]/div')

    def add_senders(self, xpath, email):
        self.driver.find_element_by_xpath(xpath).send_keys(email)
        time.sleep(2)
        self.driver.find_element_by_xpath(xpath).send_keys(Keys.TAB)

    def create_mail(self, request, email_cto, text, report, sm):

        self.driver.find_element_by_xpath('//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[1]/div/'
                                          'div[1]/div/div/div[1]/div/button[1]/span[1]').click()
        """Заполнение поля "Кому" электронными адресами ЦТО"""

        while True:
            try:
                self.add_senders('//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div'
                                 '[5]/div[1]/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]'
                                 '/div[2]/div[1]/div/div/div/span/div[1]/form/input', email_cto[0])
                break
            except NoSuchElementException:
                print(time.time())
                time.sleep(0.5)

        for email in email_cto[1:]:
            self.add_senders('//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div'
                             '[5]/div[1]/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]'
                             '/div[2]/div[1]/div/div/div/span/div[1]/form/input', email)
        time.sleep(1)
        copy_senders = ['SD_Administrators', 'service_orr']

        disc_sm = {'глебов': 'Pavel.Glebov@pilot.ru',
                   'лесовой': 'Dmitriy.Lesovoy@pilot.ru'}

        copy_senders.append(disc_sm[sm.lower()])
        for email in copy_senders:
            self.add_senders('//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/'
                             'div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div/div/div/'
                             'span/div[1]/form/input', email)
            time.sleep(0.3)

        if report == 'a':
            report = f'А.01.14 Запросы на ремонт ККТ с РВЗ менее 15 часов {request}'
        elif report == 'd':
            report = f'D 01 {request}'

        self.driver.find_element_by_xpath(
            '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]'
            '/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[6]/div[2]'
            '/input').clear()
        self.driver.find_element_by_xpath(
            '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]'
            '/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[6]/div[2]'
            '/input').send_keys(report)

        """Наполнение письма текстом"""
        self.enter_words('//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div'
                         '[1]/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div[1]/'
                         'div[3]/div', text)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/'
                                          'div[5]/div[1]/div/div[3]/div[5]/div/div[2]/div[1]/button[1]').click()


def main():
    """testing"""
    mail = Send_message(config.log_m, config.pas_m)
    mail.create_mail('920920', ['Maksim.Timofeev@pilot.ru', 'artem.moiseev@pilot.ru'], 'test mail\nHello world', 'a')


if __name__ == '__main__':
    main()
