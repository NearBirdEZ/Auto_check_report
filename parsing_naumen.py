from API_Naumen import API_Naumen
from selenium.common.exceptions import NoSuchElementException


class Parsing_naumen:
    driver = API_Naumen.driver
    email = []

    def take_senders(self):
        self.driver.find_element_by_xpath(
            '//*[@id="ServiceCall.Container.Column_1.ServiceCallProps.responsible"]/a').click()
        try:
            self.email.append(
                self.driver.find_element_by_xpath('//*[@id="Parameters.EmployeeParameters.Email"]').text)
            if "" in self.email:
                self.email.clear()
                self.driver.back()
                self.driver.find_element_by_xpath(
                    '//*[@id="ServiceCall.Container.Column_1.ServiceCallProps.responsible"]/a[2]').click()
                self.group_emails()
        except NoSuchElementException:
            self.group_emails()

    def group_emails(self):
        xpath_emails = '//*[@id="OU.EmployeesList.EmployeesListActionContainer.ObjectListReport.tableListAndButtons' + \
                       '.EmployeesListemployeesList"]/tbody'
        text = self.driver.find_element_by_xpath(xpath_emails).text

        for word in " ".join(text.split('\n')).split():
            if "@" in word:
                self.email.append(word)
        self.driver.back()

    def time_out(self):
        link = self.driver.find_element_by_xpath('//*[@id="SCTiming"]').get_attribute('href')
        self.driver.get(link)
        return self.driver.find_element_by_xpath('//*[@id="SCTiming.TimeProps.remaining_time"]').text
