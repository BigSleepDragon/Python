# Author:ZhuYuLiang
from core import atm
from core import mall

menu='''\033[32;1m
    1.购物商场
    2.ATM
    \033[0m'''

def run():
    '''
    The program runs the main function
    :return:
    '''
    while True:
        print(menu)
        choice=input('请选择: ').strip()
        if choice == '1':
            mall.main()
        elif choice == '2':
            atm.main()
        else:
            print('输入错误，请重新选择')
            continue


if __name__ == '__main__':
    run()