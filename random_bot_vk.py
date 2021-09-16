token = ""
#id_txt = 'E:\\random skripts\\randomVK\\id.txt' #не юзабельно, оставленно на всякий, смотри закомментированное
#id_admin = 'E:\\random skripts\\randomVK\\id_adm.txt'
#name_txt = 'E:\\random skripts\\randomVK\\name.txt'


from threading import Thread
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3
from datetime import datetime

conn = sqlite3.connect("info.db")
c = conn.cursor()

vk_session = vk_api.VkApi(token='050b64a711fd36c5a0fe552e298cbee915030365f1f11c34160a91b24f28a537af445f55340402b7c5e58')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# значек #! будет обозначать что закомментирован отладочный вывод


cErr = 0

def ms_send(user_id, text1, attach):
        vk.messages.send(
                user_id=user_id,
                message=text1,
                attachment = attach,
                random_id=get_random_id()
                )
def sticker_send(user_id, st_id):
        #62821
        vk.messages.send(
                user_id=user_id,
                sticker_id=st_id,
                random_id=get_random_id()
                )
def get_name(us_id):
        user = vk.users.get(user_id=us_id)
        return user[0]['first_name'] + ' ' + user[0]['last_name']

def check_if_exists(us_id):
        c.execute("SELECT * FROM users WHERE user_id = %d" % us_id)
        result = c.fetchone()
        if result is None:
                return False
        return True

def register_new_user(us_id):
        c.execute("INSERT INTO users(user_id, admin) VALUES (%d, 0)" % us_id)
        conn.commit()
        date = datetime.now()
        c.execute("INSERT INTO users_info(user_id, user_name, entry_time) VALUES (%d, '%s', '%s')" % (us_id, get_name(us_id), str(date)))
        conn.commit()
        
'''
def Search(lys, val):  #супер сложный алгоритм сотрировки #упразднено в угоду sql
        
            fibM_minus_2 = 0
            fibM_minus_1 = 1
            fibM = fibM_minus_1 + fibM_minus_2
            while (fibM < len(lys)):
                fibM_minus_2 = fibM_minus_1
                fibM_minus_1 = fibM
                fibM = fibM_minus_1 + fibM_minus_2
            index = -1;
            while (fibM > 1):
                i = min(index + fibM_minus_2, (len(lys)-1))
                if (lys[i] < val):
                    fibM = fibM_minus_1
                    fibM_minus_1 = fibM_minus_2
                    fibM_minus_2 = fibM - fibM_minus_1
                    index = i
                elif (lys[i] > val):
                    fibM = fibM_minus_2
                    fibM_minus_1 = fibM_minus_1 - fibM_minus_2
                    fibM_minus_2 = fibM - fibM_minus_1
                else :
                    return i
            if(fibM_minus_1 and index < (len(lys)-1) and lys[index+1] == val):
                return index+1;
            return -1
        
'''
'''
#не актуально, хз почему не закомментировал
def id_to_bd(us_id):
        #try:                                    #чтение id.txt  далее можно заменить на sql
        mass_id = []
        f = open(id_txt, 'r+')
        lins = f.readlines()
        for line in lins:
                mass_id.append(int(line.strip()))
        print(mass_id)
        f.close()
        #except:
                #ms_send(us_id, 'Err 1 id_to_bd can not open id.txt')

        try:
                mass_id.sort()
                print(Search(mass_id, us_id))
                if Search(mass_id, us_id) != -1:
                        print('есть в бд')
                        ms_send(us_id, 'Вы уже авторизовались', None)
                else:
                        print('добавляю в бд')
                        try:
                                f = open(id_txt, 'a')
                                print(us_id)
                                f.write(str(us_id) + '\n')
                                f.close()
                                try:
                                        f = open(name_txt, 'a')
                                        f.write(get_name(us_id) + '\n')
                                        f.close()
                                        ms_send(us_id, 'Первичная авторизация пройдена', None)
                                except:
                                        ms_send(us_id, 'Err 4 id_to_bd name err', None)
                                
                        except:
                                ms_send(us_id, 'Err 2 id_to_bd can not open id.txt', None)
                        
        except:
                ms_send(us_id, 'Err 3 initial authorization', None)
'''
def adm_to_bd(us_id):
        
        conn = sqlite3.connect("info.db")
        c = conn.cursor()
        c.execute("SELECT admin FROM users WHERE user_id = %d" % int(us_id))
        result = c.fetchone()
        #!print(result[0])
        if(result[0] == 0):
                c.execute("UPDATE users SET admin = %d WHERE user_id = %d" % (1, int(us_id)))
                conn.commit()
                ms_send(us_id, 'Теперь вы стали администратором!', None)
                c.execute("SELECT user_id FROM users WHERE admin = %d" % 1)
                result = c.fetchall()
                #!print(result)
                text = 'Добавлен новый администратор https://vk.com/id' + us_id
                for i in range(0, len(result)):
                        #!print(result[i][0])
                        ms_send(str(result[i][0]), text, None)
                        sticker_send(str(result[i][0]), 62797)
                        
                
        else:
                ms_send(us_id, 'Вы уже являетесь администратором', None)
                c.execute("SELECT user_id FROM users WHERE admin = %d" % 1)
                result = c.fetchall()
                #!print(result)
        '''
        try:                                    #чтение id.txt  далее можно заменить на sql
                mass_id = []
                f = open(id_admin, 'r+')
                lins = f.readlines()
                for line in lins:
                        mass_id.append(int(line.strip()))
                print(mass_id)
                f.close()
        except:
                ms_send(us_id, 'Err 9 id_to_bd can not open id.txt', None)
        try:
                mass_id.sort()
                print(Search(mass_id, us_id))
                if Search(mass_id, int(us_id)) != -1:
                        print('есть в бд')
                        ms_send(us_id, 'Вы уже являетесь администратором', None)
                else:
                        print('добавляю в бд')
                        try:
                                f = open(id_admin, 'a')
                                print(us_id)
                                f.write(str(us_id) + '\n')
                                f.close() 
                                try:
                                        f = open(name_txt, 'a')
                                        f.write(get_name(us_id) + '\n')
                                        f.close()
                                        text = 'Добавлен новый администратор https://vk.com/id' + us_id
                                        ms_send(us_id, 'вы стали админисратором', None)
                                        for i in range(len(mass_id)):
                                                ms_send(str(mass_id[i]), text, None)
                                except:
                                        ms_send(us_id, 'Err 4 id_to_bd name err', None)
                                
                        except:
                                ms_send(us_id, 'Err 2 id_to_bd can not open id.txt', None)
                        
        except:
                ms_send(us_id, 'Err 3 initial authorization', None)
        '''                    
def spam(text, us_id):
        conn = sqlite3.connect("info.db")
        c = conn.cursor()
        c.execute("SELECT user_id FROM users")
        result = c.fetchall()
        #!print(result)
        text = "Информация: \n\n" + text
        for i in range(0, len(result)):
                #!print(result[i][0])
                ms_send(str(result[i][0]), text, None)
                sticker_send(str(result[i][0]), 62821)
                        
        '''
        try:                                    #чтение id.txt  далее можно заменить на sql
                mass_id_adm = []
                f = open(id_admin, 'r+')
                lins = f.readlines()
                for line in lins:
                        mass_id_adm.append(int(line .strip()))
                print(mass_id_adm)
                f.close()
        except:
                ms_send(us_id, 'Err 9 id_to_bd can not open id.txt', None)
                
        #try:
                mass_id_adm.sort()
                #print(Search(mass_id_adm, us_id))
                if Search(mass_id_adm, int(us_id)) != -1:
                        print('есть в бд')
                
                try:                                    #чтение id.txt  далее можно заменить на sql
                        mass_id = []
                        f = open(id_txt, 'r+')
                        lins = f.readlines()
                        #count = 0
                        for line in lins:
                                mass_id.append(int(line.strip()))
                                #count+=1
                        print(mass_id)
                        f.close()
                except:
                        ms_send(us_id, 'Err 8 id_to_bd can not open id.txt', None)

                for i in range(len(mass_id_adm)):
                        ms_send(str(mass_id_adm[i]), 'рассылка начата', None)
                        
                text = 'Информация\n\n' + text
                try:
                        for i in range(len(mass_id)):
                                ms_send(str(mass_id[i]), text, None)
                                for i in range(len(mass_id_adm)):
                                        ms_send(str(mass_id_adm[i]), 'рассылка закончена', None)
                except:
                        ms_send(us_id, 'Err 7 spam', None)
        else:
                ms_send(us_id, 'У вас нет права доступа к данной команде', None)
               # except:
                             # ms_send(us_id, 'Global err 9 spam')
                '''
                             
def reply_or_fwd(i): #получение инфы о переслоннам сообщении
    return i['reply_message'] if 'reply_message' in i else i['fwd_messages'][0] if i['fwd_messages'] else None                

def zakrep_check(text, attach): #проверка на повторения при добавлении
        conn = sqlite3.connect("info.db")
        c = conn.cursor()
        c.execute("SELECT text FROM zakrep WHERE text = '%s'" % text)
        result = c.fetchone()
        #!print('----------')
        #!print(result)
        
        #print(result[0])
        #if attach == None: #костыль
        #        c.execute("SELECT attach FROM zakrep WHERE attach = '%s'" % 'None')
        c.execute("SELECT attachment FROM zakrep WHERE attachment = '%s'" % attach)
        result_attach = c.fetchone()
        #!print(result_attach)
        if(result == None or result[0] == '' and result_attach[0] == 'None'): #хз, какой-то трабл с result, если текста в бд нет возвращает только None, без массива. нужно править 
                #print('pyk')                                                                #ок, походу это происходит только с сообщениями без аттача
                                                                                                      #пофиг, костыль работает
                return 0 #можно записывать
                
        else:
                #print('kak')
                return 1 #нельзя записывать

def notification():
        conn = sqlite3.connect("info.db")
        c = conn.cursor()
        c.execute("SELECT entry_time FROM zakrep")
        result_zak = c.fetchall()
        c.execute("SELECT entry_time FROM users_info")
        result_us = c.fetchall()
        c.execute("SELECT user_id FROM users_info")
        result_id = c.fetchall()
        
        #!print(result_zak)
        #!print("-=-")
        #!print(result_us)
        #!print('-----------------') #не самый оптимальный вариант, первое что в голову пришло
                                                #чет я подумал что это как-то супер сложно для простого отправления уведомления о непрочтенных записях, но да ладно
        new = [''] * 50
        txt = ''
        for i in range(0, len(result_us)):
                for j in range(0, len(result_zak)):
                        print('User ', i, ' ', result_us[i] < result_zak[j])
                        if result_us[i] < result_zak[j]:
                                txt = txt + str(j) + ' '
                new[i] = txt
                txt = ''
        #!print(new)
        for i in range(0, len(new)):
                if new[i] != '':
                        zap = new[i].split()
                        text = "Появилась новая инфа в количестве " + str(len(zap)) + " шт"
                        ms_send(result_id[i], text, None)
                        sticker_send(result_id[i], 62826)
                        
                        
def zakrep_new(us_id):
        conn = sqlite3.connect("info.db")
        c = conn.cursor()
        c.execute("SELECT entry_time FROM users_info WHERE user_id = %d" % us_id)
        result_LtimeMass = c.fetchone()
        result_Ltime = ''.join(result_LtimeMass)
        #!print(result_Ltime)
        date = datetime.now()
        c.execute("UPDATE users_info SET entry_time='%s' WHERE user_id = %d" % (str(date), us_id))
        conn.commit()
        c.execute("SELECT * FROM zakrep")
        result_zak = c.fetchall()
        #!print(len(result_zak))
        #!print(result_zak[0])
        k=0
        for i in range(0, len(result_zak)):
                if result_Ltime < result_zak[i][3]:
                        k = k+1
                        text = 'https://vk.com/id' + str(result_zak[i][0]) + ' засейвил: \n' + result_zak[i][1]
                        #!print(text)
                        #!print(result_zak[i])
                        if result_zak[i][2] != 'None':
                                attach = result_zak[i][2].split()
                                #!print(attach)
                                ms_send(us_id, text, attach)
                        else:
                                ms_send(us_id, text, None)
        if k == 0:
                ms_send(us_id, 'Для тебя пока нет новых закрепов', None)
                sticker_send(us_id, 62814)

def zakrep_add(us_id, for_reply_or_fwd):
        t = reply_or_fwd(for_reply_or_fwd)
        conn = sqlite3.connect("info.db")
        c = conn.cursor()
        if len(t.get('attachments')) != 0:
                #print(t)
                type1 = t.get('attachments')[0]['type']
                #!print(t.get('attachments'))
                if type1 == 'photo':
                        
                        #!print(type1)
                        #!print(len(t.get('attachments')))
                        #!print(t.get('text'))
                        attach = []
                        for i in range(0, len(t.get('attachments'))):
                                photo = t.get('attachments')[i]['photo']
                                attach.append("photo{}_{}_{}".format(photo['owner_id'], photo['id'], photo['access_key']))
                        ##############
                        #!print(" ".join(attach))
                        attach_str = " ".join(attach)
                        if zakrep_check(str(t.get('text')), None) == 0:
                                date = datetime.now()
                                c.execute("INSERT INTO zakrep(user_id, text, attachment, entry_time) VALUES (%d, '%s', '%s', '%s')" % (us_id, str(t.get('text')), attach_str, str(date)))
                                conn.commit()
                                ms_send(us_id, 'Успешно добавлено', None)
                                sticker_send(us_id, 62823)
                        else:
                                ms_send(us_id, 'это уже добавлено в закреп', None)
                                sticker_send(us_id, 62815)
                        
                else:
                        print('нет аттача photo')
                if type1 == 'wall':
                        print(len(t.get('attachments')))
                        #!print(t.get('text'))
                        attach = []
                        for i in range(0, len(t.get('attachments'))):
                                wall = t.get('attachments')[i]['wall']
                                #wall2 = wall.get('attachments')
                                #print(wall)
                                attach.append("wall{}_{}".format(wall['from_id'], wall['id']))
                                #print(attach)
                        #!print(attach)
                        attach_str = " ".join(attach)
                        #!print(attach_str)
                        if zakrep_check(str(t.get('text')), None) == 0:
                                date = datetime.now()
                                c.execute("INSERT INTO zakrep(user_id, text, attachment, entry_time) VALUES (%d, '%s', '%s', '%s')" % (us_id, str(t.get('text')), attach_str, str(date)))
                                conn.commit()
                                ms_send(us_id, 'Успешно добавлено', None)
                                sticker_send(us_id, 62823)
                                notification()
                        else:
                                ms_send(us_id, 'это уже добавлено в закреп', None)
                                sticker_send(us_id, 62815)
                
                                
                if type1 == 'video':
                        #!print(t.get('attachments'))
                        #!print(len(t.get('attachments')))
                        #!print(t.get('text'))
                        attach = []
                        for i in range(0, len(t.get('attachments'))):
                                video = t.get('attachments')[i]['video']
                                attach.append("video{}_{}".format(video['owner_id'], video['id']))
                        #!print(attach)
                        attach_str = " ".join(attach)
                        #!print(attach_str)
                        if zakrep_check(str(t.get('text')), None) == 0:
                                date = datetime.now()
                                c.execute("INSERT INTO zakrep(user_id, text, attachment, entry_time) VALUES (%d, '%s', '%s', '%s')" % (us_id, str(t.get('text')), attach_str, str(date)))
                                conn.commit()
                                ms_send(us_id, 'Успешно добавлено', None)
                                sticker_send(us_id, 62823)
                                notification()
                        else:
                                ms_send(us_id, 'это уже добавлено в закреп', None)
                                sticker_send(us_id, 62815)
                if type1 == 'doc':
                        #!print('fds')
                        attach = []
                        for i in range(0, len(t.get('attachments'))):
                                doc = t.get('attachments')[i]['doc']
                                attach.append("doc{}_{}_{}".format(doc['owner_id'], doc['id'], doc['access_key']))
                        ##############
                        #!print(" ".join(attach))
                        attach_str = " ".join(attach)
                        if zakrep_check(str(t.get('text')), None) == 0:
                                date = datetime.now()
                                c.execute("INSERT INTO zakrep(user_id, text, attachment, entry_time) VALUES (%d, '%s', '%s', '%s')" % (us_id, str(t.get('text')), attach_str, str(date)))
                                conn.commit()
                                ms_send(us_id, 'Успешно добавлено', None)
                                sticker_send(us_id, 62823)
                        else:
                                ms_send(us_id, 'это уже добавлено в закреп', None)
                                sticker_send(us_id, 62815)
        else:
                if len(t.get('text')) != 0:
                        #!print(t.get('text'))
                        if zakrep_check(str(t.get('text')), None) == 0:
                                date = datetime.now()
                                c.execute("INSERT INTO zakrep(user_id, text, attachment, entry_time) VALUES (%d, '%s', '%s', '%s')" % (us_id, str(t.get('text')), attach_str, str(date)))
                                conn.commit()
                                ms_send(us_id, 'Успешно добавлено', None)
                                sticker_send(us_id, 62823)
                                notification()
                        else:
                                ms_send(us_id, 'это уже добавлено в закреп', None)
                                sticker_send(us_id, 62815)
        

def zakrep_read(us_id):
        conn = sqlite3.connect("info.db")
        c = conn.cursor()
        c.execute("SELECT user_id, text, attachment FROM zakrep")
        result = c.fetchall()
        print(len(result))
        for i in range(0, len(result)):
                text = 'https://vk.com/id' + str(result[i][0]) + ' засейвил: \n' + result[i][1]
                print(text)
                if result[i][2] != 'None':
                        attach = result[i][2].split()
                        print(attach)
                        ms_send(us_id, text, attach)
                else:
                        ms_send(us_id, text, None)

print('пока всё норм')

#id_to_bd(7)
for event in longpoll.listen():
        
        #print(123)
        #print(event)
        #message = event.obj['message']
        #peer_id = message['peer_id']
        #text = message['text']
        #print(text[0])
        #print(text)

        if event.type == VkEventType.MESSAGE_NEW and event.from_user and event.to_me:
                
                try:
                        text = event.text.lower()
                        full_inf_user = get_name(event.user_id)
                        full_inf_user+= ' id: '
                        full_inf_user+=str(event.user_id)
                        full_inf_user+=' message: '
                        full_inf_user+=text
                        print(full_inf_user)
                        #ms_send('395491169', full_inf_user)
                        
                except:
                        print('Err 5 event.text or full_name def')
                        cErr = 1
                
                
                
                
                if cErr == 0:
                        if text == 'начать' or text == 'start':

                                if not check_if_exists(event.user_id):
                                        register_new_user(event.user_id)
                                        ms_send(event.user_id, 'Вы успешно авторизовались', None)
                                else:
                                        ms_send(event.user_id, 'Вы уже авторизовались', None)
                                        
                                #th = Thread(target = id_to_bd, args = (event.user_id,))
                                #th.start()
                                #for i in text
                                #       if not i.isalpha() and i != ' ':
                                #               text = text.replace(i, '')
                                
                                ms_send(event.user_id, 'Привет. Доборо пожаловать в этот супер пупер бот! напиши помощь или help', None)
                        if text == 'залупа' or text == 'pfkegf':
                                ms_send(event.user_id, 'pon prin', None)
                        if text == 'помощь' or text == 'help':
                                ms_send(event.user_id, 'BETA 1.1.28 \n Добро пожаловать в этого прекрасного бота!\n Пока что он не обкатан на большом код-ве людей и возможно будет падать и всё такое (кстати баг репорт вы можете отправить мне в лс, буду благодарен)\n',  None)
                                ms_send(event.user_id, 'Фунционал: \n &#128511; Закреп(для получения дополнительной информации напиши помощь закреп) \n &#128511; Рассылка(для получения дополнительной информации напиши помощь рассылка) \n &#128511; Кнопки(в разработке) \n &#128511; Голосования(в разработке на последней стадии)', None)

                        if text == 'помощь закреп':
                                attach = []
                                attach.append("video395491169_456239787")
                                #print(attach)
                                ms_send(event.user_id, '&#9881; Итак, у закрепа есть 3 функции: \n\n закреп+ - заархивировать запись. Необходимо чтобы это было единожды пересланное сообщение, так же нельзя отправлять 2 записи со стены в одном сообщении(баг, пралю). Чтобы избежать большинства вопросов смотрите видео.\n\n закреп -  просмотреть све кода-либо закрепленные записи \n\n new или новое или читать - когда кто-то будет добавлять новую запись в закреп, вам будет приходить уведомление и с помощью этих триггеров можно посмотреть то, что вы еще не видели', attach)

                        if text == 'закреп+' or text == 'pfrhtg+':
                                th = Thread(target = zakrep_add, args = (event.user_id,vk.messages.getById(message_ids=event.message_id)['items'][0],))
                                th.start()
                        if text == 'закреп' or text == 'pfrhtg':
                                #zakrep_read(event.user_id)
                                th = Thread(target = zakrep_read, args = (event.user_id, ))
                                th.start()
                        if text == 'new' or text == 'новое' or text == 'читать':
                                zakrep_new(event.user_id)
                        #админ команды
                        if text.find('admin')  != -1 and str(event.user_id) == '395491169':
                                print('adding new admin starting')
                                text1 = text[6:]
                                #дописать потом
                                th = Thread(target = adm_to_bd, args=(text1,))
                                th.start()
                                
                        if text.find('спам')  != -1  or text.find('spam')  != -1:
                                
                                text2 = text[5:]
                                print(text2)
                                print('==++++++++++++====')
                                try:
                                        th = Thread(target = spam, args=(text2, event.user_id, ))
                                        th.start()
                                except:
                                        ms_send(event.user_id, 'Err 6 spam', None)
                          
                #print('Running ' + str(threading.active_count()) + ' threads')        
                                
                                
                               
                                
                
                
        
                                







#if __name__ == '__main__':
#    main()

