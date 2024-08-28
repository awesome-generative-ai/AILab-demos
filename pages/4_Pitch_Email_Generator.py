import streamlit as st
from constants import DEFAULT_MODEL
from utils.completion import tokenize
from utils.studio_style import apply_studio_style
import re
from constants import client


st.set_page_config(
    page_title="推介邮件生成器",
)

max_tokens = 2048 - 200

WORDS_LIMIT = {
    "pitch": (150, 200),
}

title_placeholder = "PetSmart Charities® 承诺投入1亿美元改善获取兽医护理的途径"
article_placeholder = """许多家庭无法获得兽医护理是一个迫切的全国性动物福利问题。为了应对这一问题，PetSmart Charities宣布在未来五年内承诺投入1亿美元，帮助打破地理、文化、语言和财务障碍，这些障碍阻止了宠物获得它们需要的兽医护理以茁壮成长。
Zora是一只可爱的哈巴狗，它的主人知道它呼吸有问题，但难以找到能以低成本提供非例行护理的兽医。尽管主人自己从无家可归到住院面临种种挑战，他还是找到了人带Zora去PetSmart Charities资助的Ruthless Kindness提供的免费诊所。得益于她接受的护理，Zora和她的主人现在一起茁壮成长。
兽医护理的获取影响着全国每个社区的动物福利行业和各个家庭。现在美国超过70%的家庭都养有宠物，但有5000万只宠物在美国甚至缺乏基本的兽医护理，包括绝育/去势手术、年度检查和疫苗接种。没有定期的兽医护理，小的宠物健康问题常常变成更大的、更昂贵的问题；可以预防的疾病可能会传播给人类和其他动物。宠物父母可能被迫放弃他们心爱的毛茸茸家庭成员给已经拥挤的动物收容所，或者在他们无法获得治疗时被迫看着它们受苦。鉴于宠物被普遍认为是心爱的家庭成员，无法获得兽医护理所带来的挑战可能产生深远的影响。
PetSmart Charities估计每年需要超过200亿美元才能以标准兽医价格弥补需要兽医护理的宠物的缺口。需要做更多的工作来扩大低成本服务的可用性，确保偏远和双语社区的获取，并确保有足够的兽医能够通过诊所和紧急护理中心提供各种服务。为了帮助引领这一行动，这家非营利组织正在发挥领导作用，联合合作伙伴和利益相关者开发和执行解决兽医护理获取差距的解决方案。
"兽医护理系统面临的挑战是巨大和多样的，没有单一的组织可以单独解决它们，"PetSmart Charities的总裁Aimee Gilbreath说。"通过PetSmart Charities的承诺，我们计划进一步投资于我们的合作伙伴并建立新的联盟，以在整个系统中创新解决方案 - 同时资助已经实施的长期解决方案，如低成本兽医诊所和兽医学生奖学金。我们相信这种方法将在兽医护理行业中产生可持续的变化。我们最好的朋友像任何家庭成员一样，应该能够获得适当的医疗保健。"
"""

def anonymize(text):
    """
    将文本中的URL和电子邮件地址替换为相应的占位符。

    参数:
    text (str): 要进行匿名化的原始文本。

    返回:
    str: 包含匿名化信息的文本。
    """
    text = re.sub(r'https?:\/\/.*', '[URL]', text)
    return re.sub(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', '[EMAIL]', text)


def generate(prompt, category, max_retries=2):
    min_length, max_length = WORDS_LIMIT[category]
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
                                if comp.finish_reason.reason == "endoftext"
                                and min_length <= len(comp.data.text.split()) <= max_length]
        try_count += 1
    st.session_state["completions"] = [anonymize(i) for i in completions_filtered]


def on_next():
    st.session_state['index'] = (st.session_state['index'] + 1) % len(st.session_state['completions'])


def on_prev():
    st.session_state['index'] = (st.session_state['index'] - 1) % len(st.session_state['completions'])


def toolbar():
    cols = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])
    with cols[1]:
        if st.button(label='<', key='prev'):
            on_prev()
    with cols[2]:
        st.text(f"{st.session_state['index'] + 1}/{len(st.session_state['completions'])}")
    with cols[3]:
        if st.button(label='\>', key='next'):
            on_next()


if __name__ == '__main__':
    apply_studio_style()
    st.title("营销生成器")

    st.session_state['title'] = st.text_input(label="标题", value=title_placeholder).strip()
    st.session_state['article'] = st.text_area(label="文章", value=article_placeholder, height=500).strip()

    domain = st.radio(
        "选择报道领域的记者 👉",
        options=['Technology', 'Healthcare', 'Venture Funding', 'Other'],
    )

    if domain == 'Other':
        instruction = "撰写给记者的推介，说服他们为什么应该为他们的出版物报道这个内容。"
    else:
        instruction = f"撰写给报道 {domain} 新闻的记者的推介，说服他们为什么应该为他们的出版物报道这个内容。"
    suffix = "电子邮件介绍"
    prompt = f"{instruction}\n标题：{st.session_state['title']}\n新闻稿：\n{st.session_state['article']}\n\n{suffix}:\n"
    category = 'pitch'

    if st.button(label="撰写"):
        with st.spinner("加载中..."):
            num_tokens = tokenize(prompt)
            if num_tokens > max_tokens:
                st.write("文本太长。输入限制为2048个token以内。尝试使用更短的文本。")
                if 'completions' in st.session_state:
                    del st.session_state['completions']
            else:
                generate(prompt, category=category)
                st.session_state['index'] = 0

    if 'completions' in st.session_state:
        if len(st.session_state['completions']) == 0:
            st.write("请再试一次 😔")

        else:
            curr_text = st.session_state['completions'][st.session_state['index']]
            st.subheader(f'生成的电子邮件')
            st.text_area(label=" ", value=curr_text.strip(), height=400)
            st.write(f"字数：{len(curr_text.split())}")
            if len(st.session_state['completions']) > 1:
                toolbar()
