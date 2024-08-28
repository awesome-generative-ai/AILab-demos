import streamlit as st
from constants import PRODUCT_DESCRIPTION_FEW_SHOT, DEFAULT_MODEL
from utils.studio_style import apply_studio_style
from constants import client
from ai21.models import Penalty

st.set_page_config(
    page_title="产品描述生成器",
)


def query(prompt):

    res = client.completion.create(
        model=DEFAULT_MODEL,
        prompt=prompt,
        num_results=1,
        max_tokens=240,
        temperature=1,
        top_k_return=0,
        top_p=0.98,
        count_penalty=Penalty(
            scale=0,
            apply_to_emojis=False,
            apply_to_numbers=False,
            apply_to_stopwords=False,
            apply_to_punctuation=False,
            apply_to_whitespaces=False,
        ),
        frequency_penalty=Penalty(
            scale=225,
            apply_to_emojis=False,
            apply_to_numbers=False,
            apply_to_stopwords=False,
            apply_to_punctuation=False,
            apply_to_whitespaces=False,
        ),
        presence_penalty=Penalty(
            scale=1.2,
            apply_to_emojis=False,
            apply_to_numbers=False,
            apply_to_stopwords=False,
            apply_to_punctuation=False,
            apply_to_whitespaces=False,
        )
    )

    return res.completions[0].data.text


if __name__ == '__main__':

    apply_studio_style()
    st.title("产品描述生成器")
    st.markdown("###### 几秒钟内为您的产品页面创建有价值的营销文案，描述您的产品及其优势！只需选择一个时尚配饰，几个关键特性，让我们的工具发挥魔力。")

    product_input = st.text_input("输入您的产品名称：", value="会说话的牛津平底鞋")
    features = st.text_area("在这里列出您的产品特性：", value="- 平底鞋\n- 惊人的栗色\n- 人造材料")

    prompt = PRODUCT_DESCRIPTION_FEW_SHOT + f"产品：{product_input}\n特性：\n{features}\n描述："

    if st.button(label="生成描述"):
        st.session_state["short-form-save_results_ind"] = []
        with st.spinner("加载中..."):
            st.session_state["short-form-result"] = {
                "completion": query(prompt),
            }

    if "short-form-result" in st.session_state:
        result = st.session_state["short-form-result"]["completion"]
        st.text("")
        st.text_area("生成的产品描述", result, height=200)
