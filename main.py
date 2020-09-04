import config
import send_message
import parsing_naumen
import API_Naumen
import time


def main():
    pars = parsing_naumen.Parsing_naumen()
    api = API_Naumen.API_Naumen(config.log_n, config.pas_n)
    flag = True
    with open("request.txt", "r") as file:
        total_line = sum(1 for _ in file)

    with open("request.txt", "r") as file:
        count = 0
        for request in file:
            count += 1
            request = request.strip()
            shop = api.shop_request(request)
            sm = input(f'Введите, пожалуйста, сервисного менеджера (фамилию) магазина {shop}\n')
            pars.take_senders()
            description = api.description_body(request).replace('\n\n', '\n')
            api.send_comments(request, 'Направлен запрос исполнителю')
            time.sleep(1)
            time_limit = pars.time_out()
            print(pars.email, '\n', description, '\nВремени осталось ', time_limit)
            time.sleep(1)
            if flag:
                send = send_message.Send_message(config.log_m, config.pas_m)
                flag = False
            else:
                API_Naumen.API_Naumen.driver.get('https://mail.pilot.ru')

            text = f'''Добрый день!
Коллеги, информирую Вас, что до регламентного времени завершения работ по запросу {request} осталось менее 15 часов (текущий запас нормативного времени: {time_limit}).
  
{description}
 
С уважением,
Желваков Егор
Специалист службы поддержки пользователей
Тел.: +7 (495) 564-87-97/96 доб. 616
Факс.: +7(495) 564-83-69
Email: Egor.Zhelvakov@pilot.ru'''

            send.create_mail(request, pars.email, text, 'a', sm)

            pars.email.clear()
            print('Письмо направлено, клик =)')
            print(f'{count} заявок выполнено из {total_line} \n\n')
            time.sleep(3)
            API_Naumen.API_Naumen.driver.get(
                'http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?uuid=corebofs000080000ikhm8pnur5l85oc')


if __name__ == '__main__':
    main()
