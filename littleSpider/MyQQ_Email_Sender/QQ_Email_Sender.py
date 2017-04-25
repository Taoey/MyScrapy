import getpass
from tools import MyEmail,Mydb,MyWeb
from models import QQ_group




if __name__ == '__main__':

    # run =True
    # while run :
    #     try:
    #         获取用户数据
    #         qq_num=input("兄台,请输入你的QQ号:")
    #         #qq_password=getpass.getpass('然后,你的密码(密码不显示哦):')
    #         qq_password=input('password:')
    #
    #         run=False
    #     except Exception as e:
    #         print("不正确输入账号密码是不行滴,重来一遍吧")
    #         print(e)


        # 获取qq_group数据
        qq_num = '741494582'
        qq_password = '754154954582qwer'
        my_web = MyWeb()
        my_web.get_qq_group(qq_num, qq_password)


