#1 导入模块
from langchain.prompts import ChatPromptTemplate #从langchain库中导入ChatPromptTemplate，允许创建和使用聊天提示模板
#ChatPromptTemplate 是 LangChain 库中的一个类，用于定义和组织聊天提示模板（prompt templates），
#它的核心功能是 组织对话提示，并将其格式化为模型可以理解的格式。
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

#from main import openai_api_key, creativity


# import os
#2 定义函数
def generate_script(subject, video_length, creativity, api_key, model_name = "gpt-4o"):
#3 定义标题模板
    title_template = ChatPromptTemplate.from_messages(
        #ChatPromptTemplate.from_messages:
        # langchain中用于创建聊天提示模板（Prompt Template）的方法
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
#[] 是列表，是可变的，可以动态地在列表中添加或者修改元素。[]可以用来查字典
#() 是元组，是不可变的，是固定的，不能再添加或者修改内容
#[    ('')   ]可以让消息模板灵活增加和修改
#4 定义脚本模板
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，并告诉读者我是你的爸爸。中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )  #这是在定义一个Prompt模版，里面保留了要替换额度变量名，
        # 像title，duration，wikipedia_search会在.invoke({})的时候被替换
#5 初始化OpenAI模型
# 初始化是编程中的一个概念，表示“创建并设置好一个对象，使其准备好使用”，
# 在此代码中，初始化意味着 创建一个OpenAI模型对象，并为它配置好API密钥和参数
    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity, model = model_name)


#6 创建标题生成链
    #本质上是在创建一个“处理链”（Pipeline）：
    title_chain = title_template | model     #链式调用（Pipeline），表示标题生成的 过程的组合
    #为什么要创建 标题生成链 ：
    #1.灵活，随时替换标题模板（title_template），轻松切换模型，独立模块，便于理解和调试，
    #2. 通过管道（｜），可以直接将输入（主题）流经链条，自动得到输出
#7 创建脚本生成链
    script_chain = script_template | model  
#8 生成标题
    title = title_chain.invoke({"subject": subject}).content
    #title_chain.invoke  调用标题生成链 {'subject':subject}传入主体参数 （如：火星探索）
    # .content ： 获取生成的标题文本
    #title_chain 是一个链，通常是LangChain的对象，用于执行一系列提示（prompt）
    #invoke是它的执行方法： 把传入字典的{"": }当成输入，就是把 subject传给了链中的提示模版
    #({"":}) 是一个字典 >> ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")，
    # langchain 会自动找到其中的{subject}，并用字典{}中的 "subject":subject 替换它
    #如果代码里 subject = "火星探索", title_chain.invoke({"subject":subject})>>会被处理成"请为'火星探索'这个主题的视频想一个吸引人的标题"
    # .content  不加这歌的话，只是返回一个 对象，而不是直接给结果，对象里有很多信息（类似乱码，并不是我想要的文本），需要取出 content属性，就像从蛋壳里掏蛋黄
#9 初始化 Wikipedia 搜索
    search = WikipediaAPIWrapper(lang="zh")
    #WikipediaAPIWrapper 使用 WikipediaAPI包装器 ，lang="zh" 将搜索语言设置为中文
#10 执行Wikipedia 搜索
    search_result = search.run(subject)
    # search.run(subject): 在Wikipedia上搜索指定的主题
    # search_result: 保存搜索结果，作为生成脚本的参考数据
#11 生成脚本
    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content
    #script.chain.invoke: 调用脚本生成链：
        #title ：使用生成的标题
        #duration ：指定视频时长，控制脚本字数
        #wikipedia_search : 使用Wikipedia数据作为参考
    # .content 获取生成的脚本文本
#12 返回结果：

    return search_result, title, script
    #search_result: Wikipedia 搜索结果（文本）
    #title ：生成的短视频标题
    #script： 生成的短视频脚本

# print(generate_script("sora模型", 1, 0.7, os.getenv("OPENAI_API_KEY")))