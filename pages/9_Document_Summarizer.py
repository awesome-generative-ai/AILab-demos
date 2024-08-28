import streamlit as st
from ai21.errors import UnprocessableEntity

from utils.studio_style import apply_studio_style
from constants import client, SUMMARIZATION_URL, SUMMARIZATION_TEXT

st.set_page_config(
    page_title="文档摘要生成器",
)

if __name__ == '__main__':
    apply_studio_style()

    st.title("文档摘要生成器")
    st.write("轻松将长篇材料转化为精炼的摘要。无论是文章、研究论文还是您自己的笔记 - 这个工具都能总结出关键点！")
    sourceType = st.radio(label="资源类型", options=['Text', 'URL'])
    if sourceType == 'Text':
        source = st.text_area(label="在此处粘贴您的文本：",
                              height=400,
                              value=SUMMARIZATION_TEXT).strip()
    else:
        source = st.text_input(label="在此处粘贴您的网址：",
                               value=SUMMARIZATION_URL).strip()

    if st.button(label="生成摘要"):
        with st.spinner("加载中..."):
            try:
                response = client.summarize.create(source=source, source_type=sourceType.upper())
                st.text_area(label="摘要", height=250, value=response.summary)
            except UnprocessableEntity:
                 st.write('文本对于文档摘要生成器来说太长了，请尝试使用分段摘要生成器。')
