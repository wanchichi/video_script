import streamlit as st  #引入Streamlit库，用于创建Web界面
from utils import generate_script
#从自定义的“utils”文件中导入generate_script函数，用于生成脚本


st.title("🎬 视频脚本生成器")   #设置网页的 主标题

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
    #创建一个侧边栏，用来输入用户的OpenAI API密钥，密钥输入框是密码类型（隐藏输入）
    #提供一个 获取API密钥的 超链接。

subject = st.text_input("💡 请输入视频的主题")
#创建一个文本输入框，用户输入视频主题
video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
#创建一个 数字输入框，用户输入视频时长（单位：分钟），最小为0.1.
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
#创建一个滑动条（0.0--0.1），用于控制生成脚本的“创造力”。默认值是0.2，数值越大，生成内容越多样

submit = st.button("生成脚本")
#创建一个按钮，用户点击后触发脚本生成

if submit and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")
    st.stop()
    #如果用户点击了按钮但没有填写API密钥，就显示提示并停止执行
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
    #如果点击了按钮但没有填入subject，提示并停止
if submit and not video_length >= 0.1:
    st.info("视频长度需要大于或等于0.1")
    st.stop()
    #检查视频时长是否合法，必须大于等0.1
#核心逻辑执行
if submit:
    with st.spinner("AI正在思考中，请稍等..."):
        search_result, title , script = generate_script(subject, video_length, creativity, openai_api_key, model_name = "gpt-4o")
    #用户提交了所有信息，显示加载动画
    #你定义的是参数 api_key，但传进去的是变量 openai_api_key，
    # _这完全没问题——只要这个变量 openai_api_key 在当前作用域里已经被定义并且是你想要传的值就行。
    #调用generate_script函数，传入用户的输入，生成wiki搜索结果，标题和脚本。
    st.success("视频脚本已生成！")#显示脚本生成成功的提示
    st.subheader("🔥 标题：")
    st.write(title) #显示生成的视频标题  st.write()是万能展示函数
    st.subheader("📝 视频脚本：")
    st.write(script) #显示生成的视频脚本
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)  #创建一个可展开的区域，显示维基百科的搜索内容，作为生成脚本的参考资料
