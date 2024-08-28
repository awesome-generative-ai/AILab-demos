import streamlit as st
from utils.studio_style import apply_studio_style
from constants import client
from ai21.models import ParaphraseStyleType

st.set_page_config(
    page_title="改写工具",
)


def get_suggestions(text, intent=ParaphraseStyleType.GENERAL, span_start=0, span_end=None):
    rewrite_resp = client.paraphrase.create(
        text=text,
        style=intent,
        start_index=span_start,
        end_index=span_end or len(text))
    rewritten_texts = [sug.text for sug in rewrite_resp.suggestions]
    st.session_state["rewrite_rewritten_texts"] = rewritten_texts


def show_next(cycle_length):
    # From streamlit docs: "When updating Session state in response to events, a callback function gets executed first, and then the app is executed from top to bottom."
    # This means this function just needs to update the current index. The text itself would be shown since the entire app is executed again
    curr_index = st.session_state["rewrite_curr_index"]
    next_index = (curr_index + 1) % cycle_length
    st.session_state["rewrite_curr_index"] = next_index


def show_prev(cycle_length):
    curr_index = st.session_state["rewrite_curr_index"]
    prev_index = (curr_index - 1) % cycle_length
    st.session_state["rewrite_curr_index"] = prev_index


if __name__ == '__main__':
    apply_studio_style()

    st.title("改写工具")
    st.write("轻松改写！使用这个AI写作伴侣，为您的句子找到全新的表述方式，它能够释义和重写任何文本。选择能够清晰传达您想法的改写建议，有多种不同的语调可供选择。")
    text = st.text_area(label="在这里写下您的文本，看看改写工具能做什么：",
                        max_chars=500,
                        placeholder="5Loi AILab 是一个为开发者和企业提供顶级自然语言处理（NLP）解决方案的平台，由 AI21 Labs 的尖端语言模型驱动。",
                        value="5Loi AILab 是一个为开发者和企业提供顶级自然语言处理（NLP）解决方案的平台，由 AI21 Labs 的尖端语言模型驱动。").strip()

    intent = st.radio(
        "设置您的语调 👉",
        key="intent",
        options=["general", "formal", "casual", "long", "short"],
        horizontal=True
    )

    st.button(label="改写 ✍️", on_click=lambda: get_suggestions(text, intent=intent))
    if "rewrite_rewritten_texts" in st.session_state:
        suggestions = st.session_state["rewrite_rewritten_texts"]

        ph = st.empty()
        if "rewrite_curr_index" not in st.session_state:
            st.session_state["rewrite_curr_index"] = 0
        curr_index = st.session_state["rewrite_curr_index"]
        ph.text_area(label="建议", value=suggestions[curr_index])

        col1, col2, col3, *_ = st.columns([1, 1, 1, 10])
        with col1:
            st.button("<", on_click=show_prev, args=(len(suggestions),))
        with col2:
            st.markdown(f"{curr_index+1}/{len(suggestions)}")
        with col3:
            st.button("\>", on_click=show_next, args=(len(suggestions),))
