import streamlit as st
from audio_recorder_streamlit import audio_recorder
import time
import requests
import json

# Deepseek API 配置
DEEPSEEK_API_KEY = "sk-f0db277b72cc4f96b82aafc81a61b12b"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # 请根据实际的API地址调整

def call_deepseek_api(prompt, temperature=0.7):
    """调用 Deepseek API 获取响应"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",  # 请根据实际的模型名称调整
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"API 调用失败: {str(e)}")
        return None

def get_teaching_materials(subject):
    """获取教学素材"""
    prompt = f"请为《{subject}》课程提供合适的教学导入素材，包括生活实例和历史案例。"
    return call_deepseek_api(prompt)

def get_language_optimization(text):
    """获取语言优化建议"""
    prompt = f"请分析以下教学语言，并提供优化建议：\n{text}"
    return call_deepseek_api(prompt)

def generate_question_chain(text):
    """生成问题链"""
    prompt = f"请基于以下教学内容，生成一个循序渐进的问题链：\n{text}"
    return call_deepseek_api(prompt)

def get_experiment_materials(subject):
    """获取实验素材"""
    prompt = f"请为《{subject}》课程提供适合的实验素材和演示方案。"
    return call_deepseek_api(prompt)

def main():
    st.set_page_config(page_title="师范生教学技能个性化提升平台", layout="wide")
    
    st.title("师范生教学技能个性化提升平台")
    
    tab1, tab2, tab3 = st.tabs(["导入语言优化", "讲授语言优化", "实验板块优化"])
    
    # 导入语言优化标签页
    with tab1:
        st.subheader("素材查询")
        search_input = st.text_input(
            "请输入查询内容",
            placeholder="例如：我要试讲《自由落体运动》，有没有合适的导入素材"
        )
        if st.button("查询素材", key="search_material"):
            with st.spinner("正在查询中..."):
                if search_input:
                    # 从输入中提取课程名称
                    subject = search_input.split("《")[1].split("》")[0]
                    materials = get_teaching_materials(subject)
                    if materials:
                        st.success("已找到相关素材")
                        st.write(materials)
        
        st.divider()
        
        st.subheader("语言优化")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("方式一：实时录音")
            audio_bytes = audio_recorder()
            if audio_bytes:
                st.audio(audio_bytes, format="audio/wav")
        
        with col2:
            st.write("方式二：上传音频文件")
            audio_file = st.file_uploader(
                "选择音频文件", 
                type=['wav', 'mp3', 'm4a'],
                key="audio_upload1"
            )
            if audio_file:
                st.audio(audio_file)
        
        if audio_bytes or audio_file:
            text_input = st.text_area(
                "语音转文字结果",
                value="这里将显示语音转换的文字...",
                height=150
            )
            if st.button("获取优化建议"):
                with st.spinner("正在分析..."):
                    optimization = get_language_optimization(text_input)
                    if optimization:
                        st.success("优化建议已生成")
                        st.write(optimization)
    
    # 讲授语言优化标签页
    with tab2:
        st.subheader("提问环节优化")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("方式一：实时录音")
            audio_bytes2 = audio_recorder(key="recorder2")
            if audio_bytes2:
                st.audio(audio_bytes2, format="audio/wav")
        
        with col2:
            st.write("方式二：上传音频文件")
            audio_file2 = st.file_uploader(
                "选择音频文件", 
                type=['wav', 'mp3', 'm4a'],
                key="audio_upload2"
            )
            if audio_file2:
                st.audio(audio_file2)
        
        if audio_bytes2 or audio_file2:
            text_input2 = st.text_area(
                "语音转文字结果",
                value="这里将显示语音转换的文字...",
                height=150,
                key="text_area2"
            )
            if st.button("生成问题链"):
                with st.spinner("正在生成问题链..."):
                    question_chain = generate_question_chain(text_input2)
                    if question_chain:
                        st.success("问题链已生成")
                        st.write(question_chain)
    
    # 实验板块优化标签页
    with tab3:
        st.subheader("实验素材查询")
        exp_search = st.text_input(
            "请输入查询内容",
            placeholder="例如：我要试讲《自由落体运动》，有没有合适的常见可实现的实验素材",
            key="exp_search"
        )
        if st.button("查询实验素材"):
            with st.spinner("正在查询中..."):
                if exp_search:
                    # 从输入中提取课程名称
                    subject = exp_search.split("《")[1].split("》")[0]
                    experiments = get_experiment_materials(subject)
                    if experiments:
                        st.success("已找到相关实验素材")
                        st.write(experiments)

if __name__ == "__main__":
    main() 