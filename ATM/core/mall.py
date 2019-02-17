# Author:ZhuYuLiang
import json
import os
from core import atm

commodity=[
    ('iphone6',3500),
    ('iphone6s',3888),
    ('iphone7',4500),
    ('iphone7s',4888),
    ('iphoneWatch',1888),
    ('iphoneMac',14888)
]

shopping_trolley=[]

def print_commodity():
    print('现有商品，如下'.center(50, '-'))
    for index,merchandise in enumerate(commodity):
        print(index, end=' ')
        for i in merchandise:
            print(i, end=' ')
        print()
    print('\033[31;1m或者按q键退出！\033[0m')



def main():
    money = 0
    while True:
        print_commodity()
        use_choice=input("选择要购买的商品编号: ")
        if use_choice.isdigit():
            use_choice=int(use_choice)
            if use_choice >= 0 and use_choice <= len(commodity) - 1:
                shopping_trolley.append(commodity[use_choice][0])
                money += commodity[use_choice][1]
                del commodity[use_choice]
                print('加入购物车成功')
            else:
                print('\033[31;1m选择的商品不存在\033[0m')
        elif use_choice == 'q':
            if shopping_trolley:
                balance = atm.shopping_consumption(money)
                if balance[0]:
                    print('信用卡余额为: {}，商品为：{}。'.format(balance[1], shopping_trolley[:]))
                    break
                else:
                    print('\033[31;1m余额不足,现余额为：{}\033[0m'.format(balance[1]))
                    continue
            else:
                break
        else:
            print('\033[41;1m输入错误，重新选择\033[0m')
            continue

if __name__ == '__main__':
    main()


