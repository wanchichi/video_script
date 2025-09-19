import streamlit as st
from utils import generate_script

st.title("视频脚本🤖生成器")

with st.sidebar:
    openai_api_key = st.text_input("要输入OpenAI API密钥：", type="password")
    st.markdown("[点击获取OpenAI API密钥嗷](https://platform.openai.com/account/api-keys)")

subject = st.text_input("你的视频主题是什么嘞?")
video_length = st.number_input("视频的大致有多少分钟呢?（单位：分钟）", min_value=0.1, step=0.1)
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更贴合主题，数字大放飞自我创造）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
submit = st.button("生成!!\(≧▽≦)/")

if submit and not openai_api_key:
    st.info("要先输入OpenAI API密钥~")
    st.stop()
if submit and not subject:
    st.info("要先输入视频的主题嗷😡")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("视频长度需要大于或等于0.1😡")
    st.stop()
if submit:
    with st.spinner("我正在思考🤔，请稍等..."):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
    st.success("视频脚本已生成！")
    st.subheader("🔥 标题：")
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)
