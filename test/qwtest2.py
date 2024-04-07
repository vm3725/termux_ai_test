from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import dashscope
from airtest.core.api import connect_device
from airtest.core.api import G
from airtest.core.api import *
from uiautomation import AndroidUiautomationPoco
import json
dashscope.api_key="sk-5c80953a465545d29d1173b49d1fbbfc"
def multi_init(_messages):
    response = Generation.call("qwen-turbo",
                               
                               messages = _messages,
                               result_format='message',  # set the result to be "message" format.
                               )
    if response.status_code == HTTPStatus.OK:
        print(response.output.choices[0]['message']['content'])
        # append result assistant response to messages.
        _messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        # 如果失败，将最后一条user message从message列表里删除，确保user/assistant消息交替出现
        _messages = _messages[:-1]
        

def multi_send(_messages,str):
    _messages.append({'role': Role.USER, 'content': str})
    # make second round call
    response = Generation.call("qwen-turbo",
                               messages=_messages,
                               result_format='message',  # set the result to be "message" format.
                               )
    if response.status_code == HTTPStatus.OK:
        str = response.output.choices[0]['message']['content']
        _messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': str})
        return str
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        # 如果失败，将最后一条user message从message列表里删除，确保user/assistant消息交替出现
        messages = messages[:-1]

if __name__ == '__main__':
    #dev1 = connect_device("Android://127.0.0.1:5037/127.0.0.1:39955")
    dev1 = connect_device("Android:///")
    poco = AndroidUiautomationPoco(dev1)
    _messages = [{'role': Role.SYSTEM, 'content': '你现在是一个Android手机助手'},
             {'role': Role.USER, 'content': '你现在是一个Android手机助手，同时也是一个语言解析器，我为你增加了可以操控手机的组件，我需要你来为我拆分指令，比如，用户可能会说“打开微信”，我需要将这个指令解析成动作“打开”和目标“微信”，要以json形式展示，json值用中文标示，这样的话，我就能根据用户的指令执行相应的操作。在这期间你还要和我聊天，但是聊天内容和指令解析要分开展示'}]
    multi_init(_messages)
    while True:
        user_input = input("请输入你想要的内容：")
        strs = multi_send(_messages,user_input)
        if "```json" in strs:
            strsjson = strs[strs.rfind('{'):strs.rfind("}")]+"}"
            print(strsjson)
            print(strs)
            strdict = json.loads(strsjson)
            action = strdict["action"]
            if user_input == "/bye":
                print("再见！")
                break
            elif action == "打开":
                pocotest = poco(strdict["target"])
                pocotest.focus([0.5,0.2]).click()
            elif action == "点击":
                poco(text=strdict["target"]).click()
        else:
            print(strs)
       
