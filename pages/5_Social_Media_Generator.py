from constants import *
from utils.filters import *
from utils.studio_style import apply_studio_style
from constants import client


def create_prompt(media, article):
    post_type = "tweet" if media == "Twitter" else "领英帖子"
    instruction = f"撰写一条{post_type}，宣传以下新闻稿。"
    return f"{instruction}\n文章：\n{article}\n\n{post_type}:\n"


def generate(article, media, max_retries=2, top=3):
    prompt = create_prompt(media, article)
    completions_filtered = []
    try_count = 0
    while not len(completions_filtered) and try_count < max_retries:
        res = client.completion.create(
            model=DEFAULT_MODEL,
            prompt=prompt,
            max_tokens=200,
            temperature=0.8,
            num_results=16
        )
        completions_filtered = [comp.data.text for comp in res.completions
                                if apply_filters(comp, article, media)]
        try_count += 1
    res = filter_duplicates(completions_filtered)[:top]
    return [remove_utf_emojis(anonymize(i)) for i in res]


def on_next():
    st.session_state['index'] = (st.session_state['index'] + 1) % len(st.session_state['completions'])


def on_prev():
    st.session_state['index'] = (st.session_state['index'] - 1) % len(st.session_state['completions'])


def toolbar():
    cols = st.columns([0.35, 0.1, 0.1, 0.1, 0.35])
    with cols[1]:
        st.button(label='<', key='prev', on_click=on_prev)
    with cols[2]:
        st.text(f"{st.session_state['index'] + 1}/{len(st.session_state['completions'])}")
    with cols[3]:
        st.button(label="\>", key='next', on_click=on_next)
    with cols[4]:
        st.button(label="🔄", on_click=lambda: compose())


def extract():
    with st.spinner("文章总结中..."):
        try:
            st.session_state['article'] = client.summarize.create(source=st.session_state['url'], source_type='URL').summary
        except:
            st.session_state['article'] = False


def compose():
    with st.spinner("生成帖子中..."):
        st.session_state["completions"] = generate(st.session_state['article'], media=st.session_state['media'])
        st.session_state['index'] = 0


if __name__ == '__main__':
    apply_studio_style()
    st.title("社交媒体内容生成器")

    st.session_state['url'] = st.text_input(label="输入你的文章 URL",
                                            value=st.session_state.get('url', 'https://www.5loi.com/blog/technology-strategy-thoughts')).strip()

    if st.button(label='摘要'):
        extract()

    if 'article' in st.session_state:
        if not st.session_state['article']:
            st.write("这篇文章不支持，请尝试另一个")

        else:
            st.text_area(label='Summary', value=st.session_state['article'], height=200)

            st.session_state['media'] = st.radio(
                "为这篇文章撰写帖子 👉",
                options=['Twitter', 'Linkedin'],
                horizontal=True
            )

            st.button(label="撰写", on_click=lambda: compose())

    if 'completions' in st.session_state:
        if len(st.session_state['completions']) == 0:
            st.write("请再试一次 😔")

        else:
            curr_text = st.session_state['completions'][st.session_state['index']]
            st.text_area(label="你生成的绝妙帖子", value=curr_text.strip(), height=200)
            if len(st.session_state['completions']) > 1:
                toolbar()
