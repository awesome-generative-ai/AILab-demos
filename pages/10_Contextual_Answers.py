import streamlit as st
from utils.completion import tokenize
from utils.studio_style import apply_studio_style
from constants import OBQA_CONTEXT, OBQA_QUESTION, client

st.set_page_config(
    page_title="上下文相关回答",
)

max_tokens = 2048 - 200


if __name__ == '__main__':

    apply_studio_style()
    st.title("上下文相关回答")

    st.write("在给定的上下文中提出问题。")

    context = st.text_area(label="上下文：", value=OBQA_CONTEXT, height=300)
    question = st.text_input(label="问题：", value=OBQA_QUESTION)

    if st.button(label="回答"):
        with st.spinner("加载中..."):
            num_tokens = tokenize(context + question)
            if num_tokens > max_tokens:
                st.write("文本太长。输入限制为2048个令牌以内。请尝试使用更短的文本。")
                if 'answer' in st.session_state:
                    del st.session_state['completions']
            else:
                response = client.answer.create(context=context, question=question)
                st.session_state["answer"] = response.answer

    if "answer" in st.session_state:
        st.write(st.session_state['answer'])
