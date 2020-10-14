import random, vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import info, data, keyboards, game
import os
import os.path

vk_session = vk_api.VkApi(token=info.token)
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
longpoll = VkBotLongPoll(vk_session, info.publicId)
vk = vk_session.get_api()
from vk_api.longpoll import VkLongPoll, VkEventType
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

try:
    os.mkdir('Game')
    os.mkdir('UsersInfo')
except:
    print('')
print('start')
for event in Lslongpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.from_user:
            #Смотрим статус пользователя
            userStatus = data.getUserStatus(event.user_id)
            #Если пользователь в меню
            if userStatus == '0':
                if event.text[:8] == 'Подписка':
                    SUBS = data.getUserSUBS(event.user_id)
                    mmessasge = ''
                    if event.text[9:] == 'на_что-то_там':
                        if SUBS[0] == '0':
                            data.setUserSUBS(event.user_id, '1' + SUBS[1:])
                            mmessage = 'Теперь ты подписан на_что-то_там'
                        else:
                            data.setUserSUBS(event.user_id, '0' + SUBS[1:])
                            mmessage = 'Ты отписался от на_что-то_там'
                        Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.subs(event.user_id).get_keyboard(),
                        message = mmessage
                        )

                var = ['Подписки']
                if event.text in var:
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.subs(event.user_id).get_keyboard(),
                        message = 'Тут находятся твои подписочки, все на что ты подписан выделено зеленым, на что не подписан красным, чтобы подписаться/отписаться нажми'
                        )
                var = ['Играть']
                if event.text in var:
                    data.setUserStatus(event.user_id, 'G0')
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                        message = 'Рад представить игру - Лабиринт Минотавра, правда Минотавр в отпуске, поэтому это почти обычный лабиринт.'
                                  'Его особенность в том, что он состоит из развилок похожих на Y, эти развилки связаны между собой абсолютно случайным образом. Тебе нужно выбраться из лабиринта.'
                                  'Ты можешь отметить путь на котором сейчас стоишь, отметка - 3 любых символа, можешь осмотреться в поисках отметок, а так же пойти назад, налево, вправо.'
                                  'Удачи!'
                        )
                var = ['Профиль']
                if event.text in var:
                    massage = ""
                    FIO = data.getUserFIO(event.user_id)
                    STUD = data.getUserSTUD(event.user_id)
                    if FIO != '0' and STUD != '0':
                        mmessage = ('Ты уже ввел свое ФИО и номер студака, можешь проверить \n'+
                                    'Номер студака:' + STUD + '\n' +
                                    'ФИО:' + FIO + '\n' +
                                    'Если есть ошибка, можешь исправить просто нажми на нужную кнопку')
                    elif FIO != '0' and STUD == '0':
                        mmessage = 'Введи номер своего студака, для ввода просто нажми кнопку студак'
                    elif FIO == '0' and STUD != '0':
                        mmessage = 'Введи свое ФИО, для ввода просто нажми кнопку ФИО'
                    else:
                        mmessage = 'Введи свое ФИО и номер студака, для ввода просто нажми на соответствующую кнопку'
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.profile(event.user_id).get_keyboard(),
                        message = mmessage
                        )
                var = ['ФИО']
                if event.text in var:
                    data.setUserStatus(event.user_id, '2')
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.back(event.user_id).get_keyboard(),
                        message = 'Теперь просто введи свое ФИО'
                        )
                var = ['Cтудак']
                if event.text in var:
                    data.setUserStatus(event.user_id, '1')
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.back(event.user_id).get_keyboard(),
                        message = 'Теперь просто введи номер студака'
                        )
                var = ['Назад']
                if event.text in var:
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.mainMenu(event.user_id).get_keyboard(),
                        message = 'Снова в меню.'
                    )
            elif userStatus[0] == 'G':
                if userStatus[1] == '0':
                    var = ['Новая игра']
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G1')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.back(event.user_id).get_keyboard(),
                            message = 'Введи сложность - число от 1 до 9'
                        )
                    var = ['Продолжить']
                    if event.text in var:
                        try:
                            a = game.getLine(event.user_id, 0)
                            if a[0][0] == '-1':
                                a /= 0
                            else:
                                data.setUserStatus(event.user_id, 'G2')
                                Lsvk.messages.send(
                                    user_id = event.user_id,
                                    random_id = get_random_id(),
                                    keyboard = keyboards.game(event.user_id).get_keyboard(),
                                    message = 'Сохранение загружено'
                                )
                        except:
                            data.setUserStatus(event.user_id, 'G1')
                            Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.back(event.user_id).get_keyboard(),
                                message = 'Ошибка, сохранение не найдено, создание новой игры...\nВведи сложность - число от 1 до 9'
                            )
                    var = ['Выход']
                    if event.text in var:
                        data.setUserStatus(event.user_id, '0')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.mainMenu(event.user_id).get_keyboard(),
                            message = 'Снова в меню.'
                        )
                if userStatus[1] == '1':
                    var = ['Отмена']
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G0')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                            message = 'Действие отменено.'
                        )
                    else:
                        try:
                            hard = int(event.text[0])
                            if hard>= 1 and hard<= 9:
                                game.newGame(event.user_id, hard*10)
                                data.setUserStatus(event.user_id, 'G2')
                                Lsvk.messages.send(
                                    user_id = event.user_id,
                                    random_id = get_random_id(),
                                    keyboard = keyboards.game(event.user_id).get_keyboard(),
                                    message = 'Ты в игре!'
                                )
                            else:
                                hard /= 0
                        except:
                            Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                message = 'Некоректный ввод, попробуй еще раз'
                                )
                if userStatus[1] == '2':
                    var = ['Назад', 'Налево' ,'Направо']
                    if event.text in var:
                        if game.move(event.user_id, var.index(event.text)):
                            data.setUserStatus(event.user_id, 'G0')
                            Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                                message = 'Поздравляем, ты вышел из лабиринта!'
                            )
                        else:
                            i = game.check(event.user_id)
                            Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                message = 'Ты пошел к следующей развилке и осмотрелся в поисках отметок\n' +
                                          'Слева:' + i[1] +
                                          '\nСправа:' + i[2] +
                                          '\nПод ногами:' + i[0]
                            )
                    var = ['Отметка']
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G3')
                        Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.back(event.user_id).get_keyboard(),
                                message = 'Введи отметку (3 символа)'
                            )
                    var = ['В меню']
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G0')
                        Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                                message = 'Игра сохранена.'
                            )

                if userStatus[1] == '3':
                    var = ['Отмена']
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G2')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.game(event.user_id).get_keyboard(),
                            message = 'Действие отменено.'
                        )
                    else:
                        text = event.text
                        if len(text) > 3:
                            text = text[:3]
                        else:
                            text.ljust(3, ' ')
                        game.addPrint(event.user_id, text)
                        data.setUserStatus(event.user_id, 'G2')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.game(event.user_id).get_keyboard(),
                            message = 'Ты оставил отметку:' + text
                            )


            #Если пользователь отсуцтвует в бд, добавляем в бд
            elif userStatus == '-1':
                data.addUser(event.user_id)
                Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.mainMenu(event.user_id).get_keyboard(),
                    message = 'Поздравляю, теперь ты с нами!'
                    )
            #Если пользователь вводит свой студак
            elif userStatus == '1':
                var = ['Отмена']
                if event.text in var:
                    data.setUserStatus(event.user_id, '0')
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.profile(event.user_id).get_keyboard(),
                        message = 'Отмена ввода данных.'
                    )
                else:
                    data.setUserSTUD(event.user_id, event.text.replace('\n', ''))
                    Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.profile(event.user_id).get_keyboard(),
                    message = 'Новый номер студака сохранен.'
                    )
            #Если пользователь вводит свое ФИО
            elif userStatus == '2':
                var = ['Отмена']
                if event.text in var:
                    data.setUserStatus(event.user_id, '0')
                    Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.profile(event.user_id).get_keyboard(),
                    message = 'Отмена ввода данных.'
                    )
                else:
                    data.setUserFIO(event.user_id, event.text.replace('\n', ''))
                    Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.profile(event.user_id).get_keyboard(),
                    message = 'ФИО изменено.'
                    )