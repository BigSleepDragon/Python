# Author:ZhuYuLiang
import json,os
import time

menu1 = '''\033[32;1m
    1.用户接口
    \033[0m'''

menu2 = '''\033[32;1m
    1.用户接口
    2.管理接口
    \033[0m'''
menu_user='''\033[32;1m
     1.提现(需支付5%的手续费)
     2.转账
     3.还款
     4.查看日常消费流水
     \033[0m'''
menu_Admin='''\033[32;1m
    1.添加用户
    2.修改用户额度
    3.冻结用户
    4.查看ATM记录日志
    \033[0m'''
timeinfo=time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
def Auth_type(type):
    def login(func):
        def Authentication(*args,**kwargs):
            while True:
                user_info=read_file()
                name=input('输入账户名: ')
                passwd=input('密码: ')
                print(user_info)
                if user_info:
                    if passwd == user_info[name][0] and user_info[name][3]:
                        print('\033[1;36;1m登陆成功\033[0m')
                        atm_log('{} {}用户登录成功\n'.format(timeinfo,name))
                        if type == 'atm':
                            info=func((name,user_info[name]))
                            return info
                        else:
                            info=func(args[0],(name,user_info[name]))
                            return info
                    else:
                        print('登陆失败,请重试')
                        continue
                else:
                    print('用户不存在')
        return Authentication
    return login

def stream_log(name,money):
    info='{}\t{}用户通过购物商城消费{}元'.format(timeinfo,name,money)
    try:
        with open('../logs/stream_log','r') as f:
            if not f.read():
                user_info={name:[]}
            else:
                f.seek(0)
                user_info=json.loads(f.read())
    except Exception:
        f=open('../logs/stream_log','w')
        f.close()
        stream_log(name,money)
    else:
        with open('../logs/stream_log','w') as f:
            try:
                user_info[name].append(info)
            except KeyError:
                user_info[name]=[info]         ##
            finally:
                f.write(json.dumps(user_info))

def atm_log(info):
    try:
        with open('../logs/atm.log','a') as f:
            f.write(info)
    except Exception:
        f=open('../logs/stream_log','w')
        f.close()
        atm_log(info)

def get_atm_log():
    with open('../logs/atm.log', 'r') as f:
        if not f.read():
            print('ATM没有历史操作数据')
        else:
            f.seek(0)
            for i in f:
                print(i.strip())

def get_stream_log(name):
    with open('../logs/stream_log', 'r') as f:
        if not f.read():
            print('没有历史购物数据')
        else:
            f.seek(0)
            user_info = json.loads(f.read())
            try:
                for i in user_info[name]:
                    print(i)
                    atm_log('{} {} 用户查看了消费流水\n'.format(timeinfo, name))
            except Exception:
                print('没有历史购物数据')

def modify_money(info):
    name,limit= info[0], info[1][4]
    print('{}用户,你现信用卡额度为: {}'.format(name,limit))
    limit=input('提升额度为: ')
    if limit.isdigit():
        limit=int(limit)
        user_info = read_file()
        user_info[name][4]=limit
        with open('../db/user','w') as f:
            f.write(json.dumps(user_info))
    else:
        print('输入错误')

def read_file():
    '''
    读取文件，新用户返回所有内容，老用户只返回自己的内容
    :param args:
    :return:
    '''
    try:
        f=open('../db/user', 'r')
        if not f.read():
            f.close()
            if add_user('Admin'):
                return read_file()
        else:
            f.seek(0)
            info=json.loads(f.read())
            f.close()
            return info
    except FileNotFoundError:
        fobj=open('../db/user', 'w')
        fobj.close()
        return read_file()
    except Exception:
        return False

@Auth_type('shopping')
def shopping_consumption(*args):
    menoy=args[0]
    login_info=args[1]
    db_info = read_file()
    print(login_info[1][1],menoy)
    if login_info[1][1] >= int(menoy):
        db_info[login_info[0]][1] -= int(menoy)
        db_info[login_info[0]][2] += int(menoy)
        with open('../db/user', 'w') as f:
            f.write(json.dumps(db_info))
            stream_log(login_info[0],int(menoy))
            print(login_info[0],int(menoy))
        return True,db_info[login_info[0]][1]
    else:
        print('余额不足')
        return False,db_info[login_info[0]][1]



def get_money(info):
    name, balance = info[0], info[1][1]
    print('{}用户,你现余额为: {}'.format(name, balance))
    while True:
        money=input('你要取多少钱?: ').strip()
        if money.isdigit():
            money=int(money)
            money=money+money*0.05
            break
        else:
            print('输入非数字')
            continue

    user_info=read_file()
    if user_info[name][1] >= money:
        user_info[name][1] -= money
        user_info[name][2] += money
        with open('../db/user', 'w') as f:
            f.write(json.dumps(user_info))
            print('提现成功，余额为:{}'.format(user_info[name][1]))
            atm_log('{} {}用户提取了{}元\n'.format(timeinfo,name,money))
    else:
        print('金额不足')

def Frozen_user(info):
    name=info[0]
    user_info = read_file()
    user_info[name][3]=False
    with open('../db/user', 'w') as f:
        f.write(json.dumps(user_info))
        print('冻结成功')

def transfer(info):
    name,balance=info[0],info[1][1]
    print('{}用户,你现余额为: {}'.format(name,balance))
    judge=True
    while judge:
        transfer_object=input('要转给哪位用户?: ')
        if read_file(transfer_object):
            while judge:
                money=input('转账金额: ')
                if money.isdigit():
                    if int(money) < balance:
                        user_info=read_file()
                        user_info[name][1]-=int(money)
                        user_info[name][2]+=int(money)
                        user_info[transfer_object][1]+=int(money)
                        with open('../db/user','w') as f:
                            f.write(json.dumps(user_info))
                            print('\033[36;1m转账成功，{}用户,你现余额为: {}\033[1m'.format(name,user_info[name][1]))
                            atm_log('{} {}用户转账给{}用户{}元\n'.format(timeinfo,name,transfer_object,money))
                            judge=False
                    else:
                        print('余额不足')
                        continue
                else:
                    print('输入非数字')
                    continue
        elif transfer_object == 'q':
            break
        else:
            print('目标用户不存在')

def Repay_money(info):
    name,Arrears=info[0],info[1][2]
    if Arrears < 1:
        print('{}用户，你现在不欠款,无须还款'.format(name))
        return
    else:
        print('{}用户,你现欠款为: \033[36;1m{}\033[0m'.format(name,Arrears))

    while True:
        money=input('请输入你要还款金额: ')
        if money.isdigit():
            if int(money) >0:
                user_info = read_file()
                user_info[name][2]-=int(money)
                with open('../db/user', 'w') as f:
                    f.write(json.dumps(user_info))
                    print('{}用户,你现欠款为: \033[36;1m{}\033[0m'.format(name, user_info[name][2]))
                    atm_log('{} {}用户还款{}元\n'.format(timeinfo,user_info[name],money))
                    break
            else:
                print('金额输入错误')
        elif money == 'q':
            break
        else:
            print('输入非数字')

def add_user(*args):
    if bool(args):
        print('管理员用户名为Admin')
        name='Admin'
    else:
        while True:
            name=input('输入信用卡账户名: ')
            if name == 'Admin':
                print('不能与管理员名称相同')
                continue
            else:
                break
    while True:
        passwd1=input('请输入6位数字密码: ')
        passwd2=input('请再次输入密码: ')
        if passwd1 != passwd2 or len(passwd1) >6 or not passwd1.isdigit():
            print('密码输入错误,请重试')
            continue
        else:
            break
    limit=input('输入你想要的额度，不输入的话默认为15000: ')
    if not limit:limit=15000

    if name == 'Admin':
        user_info = {name: [passwd1, int(limit), 0, True, int(limit)]}
    elif read_file():
        user_info=read_file()
        user_info[name]=[passwd1,int(limit),0,True,int(limit)]

    with open('../db/user','w') as f:
        f.write(json.dumps(user_info))
        print('创建{}用户成功，初始额度为:{}'.format(name,limit))
        atm_log('{} 管理员用户创建了{}用户\n'.format(timeinfo,name))
        return True

@Auth_type('atm')
def main(*args):
    info=args[0]
    while True:
        if info[0] == 'Admin':
            print(menu2)
        else:
            print(menu1)
        choice = input('请选择序号: ').strip()
        if choice == '1':
            while True:
                print(menu_user)
                choice=input('请选择序号: ').strip()
                if choice == '1':
                    get_money(info)
                elif choice == '2':
                    transfer(info)
                elif choice == '3':
                    Repay_money(info)
                elif choice == '4':
                    get_stream_log(info[0])
                elif choice == 'q':
                    break
                else:
                    print('\033[31;1m输入错误，请重新输入\033[0m')
                    continue
        elif choice == '2' and info[0] == 'Admin':
            while True:
                if info:
                    print(menu_Admin)
                    choice=input('请选择序号: ')
                    if choice == '1':
                        add_user()
                    elif choice == '2':
                        print(info,type(info))
                        modify_money(info)
                    elif choice == '3':
                        Frozen_user(info)
                    elif choice == '4':
                        get_atm_log()
                    elif choice == 'q':
                        break
                    else:
                        print('\033[31;1m输入错误，请重新输入\033[0m')
                        continue
        elif choice == 'q':
            break
        else:
            print('\033[31;1m输入错误，请重新输入\033[0m')

if __name__ == '__main__':
    main()
