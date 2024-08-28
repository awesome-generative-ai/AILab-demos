import streamlit as st
from utils.studio_style import apply_studio_style

if __name__ == '__main__':
    st.set_page_config(
        page_title="欢迎"
    )
    apply_studio_style()
    st.title("欢迎来到 5Loi AILab")
    st.markdown("亲身体验大型语言模型的惊人能力。通过这些演示，您可以探索各种独特的用例，展示我们尖端技术真正能够做到的事情。从即时内容生成到可以重写任何文本的释义器，AI文本生成的世界将在您的指尖。")
    st.markdown("点击这里查看背后的大脑：[5Loi 关于页面](https://www.5loi.com/about_loi)")
    st.markdown("请注意，这是5Loi AILab能力的有限演示。如果您对了解更多感兴趣，请通过 [AIPM社区](https://roadmaps.feishu.cn/wiki/RykrwFxPiiU4T7kZ63bc7Lqdnch) 与我们联系。")
