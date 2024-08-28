import streamlit as st
from utils.studio_style import apply_studio_style
from constants import CLASSIFICATION_FEWSHOT, CLASSIFICATION_PROMPT, CLASSIFICATION_TITLE, CLASSIFICATION_DESCRIPTION, \
    DEFAULT_MODEL
from constants import client


st.set_page_config(
    page_title="主题分类器",
)


def query(prompt):

    res = client.completion.create(
        model=st.session_state['classification_model'],
        prompt=prompt,
        num_results=1,
        max_tokens=5,
        temperature=0,
        stop_sequences=["##"]
    )
    return res.completions[0].data.text


if __name__ == '__main__':

    apply_studio_style()
    st.title("主题分类器")
    st.write("最近阅读了什么有趣的新闻吗？让我们看看我们的主题分类器是否能快速浏览它，并识别它的类别是体育、商业、世界新闻还是科学技术。")
    st.session_state['classification_model'] = DEFAULT_MODEL

    st.text(CLASSIFICATION_PROMPT)
    classification_title = st.text_input(label="标题：", value=CLASSIFICATION_TITLE)
    classification_description = st.text_area(label="描述：", value=CLASSIFICATION_DESCRIPTION, height=100)

    if st.button(label="分类"):
        with st.spinner("加载中..."):
            classification_prompt = f"{CLASSIFICATION_PROMPT}\n标题：\n{classification_title}" \
                                    f"描述：\n{classification_description}这篇文章的主题是：\n"
            st.session_state["classification_result"] = query(CLASSIFICATION_FEWSHOT + classification_prompt)

    if "classification_result" in st.session_state:
        st.subheader(f"主题：{st.session_state['classification_result']}")
