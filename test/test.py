from airtest.core.api import connect_device
from airtest.core.api import G
from airtest.core.api import *
from uiautomation import AndroidUiautomationPoco

#dev1 = connect_device("Android://127.0.0.1:5037/127.0.0.1:39955")
dev2 = connect_device("Android:///")
poco = AndroidUiautomationPoco(dev2)
while True:
    user_input = input("请输入你想要的内容：")
    if user_input == "/bye":
        print("再见！")
        break
    elif "打开" in user_input:
        new_input = user_input.replace("打开", "")
        print("除去'打开'后的内容是：", new_input)
        poco(text=new_input).click()
        
    else:
        print("你输入的内容是：", user_input)

       

