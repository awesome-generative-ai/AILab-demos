import streamlit as st
import numpy as np
import asyncio
from constants import DEFAULT_MODEL
from utils.studio_style import apply_studio_style
import argparse
from utils.completion import async_complete
from utils.completion import paraphrase_req
from constants import client

st.set_page_config(
    page_title="博客文章生成器",
)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        type=int,
                        default=8888)

    parser.add_argument('--num_results',
                        type=int,
                        default=5)

    args = parser.parse_args()
    return args


def build_prompt(title, sections, section_heading):
    sections_text = '\n'.join(sections)
    prompt = f"根据以下细节编写博客文章的描述性部分。\n\n博客标题：\n{title}\n\n博客内容：\n{sections_text}\n\n当前部分标题：\n{section_heading}\n\n当前部分文本："
    return prompt


def generate_sections_content(num_results, sections, title):
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = {
        "numResults": num_results,
        "maxTokens": 256,
        "minTokens": 10,
        "temperature": 0.7,
        "topKReturn": 0,
        "topP": 1,
        "stopSequences": []
    }
    group = asyncio.gather(*[async_complete(DEFAULT_MODEL, build_prompt(title, sections, s), config) for s in sections])
    results = loop.run_until_complete(group)
    loop.close()
    return results


def build_generate_outline(title):
    return lambda: generate_outline(title)


def generate_outline(title):
    st.session_state['show_outline'] = True
    st.session_state['show_sections'] = False

    res = _generate_outline(title)

    st.session_state["outline"] = res.completions[0].data.text.strip()


def _generate_outline(title):
    prompt = f"为以下标题编写博客文章的各个部分。\n博客标题：如何开始个人博客 \n博客内容：\n1. 选择个人博客模板\n2. 打造你的品牌\n3. 选择托管计划和域名\n4. 创建内容日历 \n5. 优化你的内容以适应搜索引擎优化\n6. 建立电子邮件列表\n7. 传播消息\n\n##\n\n为以下标题编写博客文章的各个部分。\n博客标题：提高JavaScript性能的现实世界示例\n博客内容：\n1. 我为什么需要提高我的JavaScript性能\n2. 寻找JavaScript性能问题的三种常见方法\n3. 我是如何使用console.time找到JavaScript性能问题的\n4. lodash.cloneDeep是如何工作的？\n5. lodash.cloneDeep的替代品是什么？\n6. 结论\n\n##\n\n为以下标题编写博客文章的各个部分。\n博客标题：幸福生活与有意义的生活有何不同？\n博客内容：\n1. 幸福生活与有意义的生活的五个不同点\n2. 幸福到底是什么？\n3. 没有愉悦的幸福吗？\n4. 你可以拥有一切吗？\n\n##\n\n为以下标题编写博客文章的各个部分。\n博客标题：{title}\n博客内容："

    res = client.completion.create(
        model=DEFAULT_MODEL,
        prompt=prompt,
        num_results=1,
        max_tokens=296,
        temperature=0.84,
        top_k_return=0,
        top_p=1,
        stop_sequences=["##"]
    )
    return res


def generate_sections():
    st.session_state['show_sections'] = True


def build_on_next_click(section_heading, section_index, completions, arg_sorted_by_length):
    return lambda: on_next_click(section_heading, section_index, completions, arg_sorted_by_length)


def on_next_click(section_heading, section_index, completions, arg_sorted_by_length):
    st.session_state['show_paraphrase'][section_heading] = False
    new_comp_index = (st.session_state['generated_sections_data'][section_heading]["text_area_index"] + 1) % 5
    section_i_text = completions[arg_sorted_by_length[new_comp_index]]["data"]["text"]
    st.session_state['generated_sections_data'][section_heading]["text_area_index"] = new_comp_index
    st.session_state['generated_sections_data'][section_heading]["text_area_data"].text_area(label=section_heading,
                                                                                             height=300,
                                                                                             value=section_i_text,
                                                                                             key=section_index)


def build_on_prev_click(section_heading, section_index, completions, arg_sorted_by_length):
    return lambda: on_prev_click(section_heading, section_index, completions, arg_sorted_by_length)


def on_prev_click(section_heading, section_index, completions, arg_sorted_by_length):
    st.session_state['show_paraphrase'][section_heading] = False

    new_comp_index = (st.session_state['generated_sections_data'][section_heading]["text_area_index"] - 1) % 5
    section_i_text = completions[arg_sorted_by_length[new_comp_index]]["data"]["text"]
    st.session_state['generated_sections_data'][section_heading]["text_area_index"] = new_comp_index
    st.session_state['generated_sections_data'][section_heading]["text_area_data"].text_area(label=section_heading,
                                                                                             height=300,
                                                                                             value=section_i_text,
                                                                                             key=section_index)


def get_event_loop(title, sections, num_results):
    st.session_state['show_sections'] = True

    for s in sections:
        st.session_state['generated_sections_data'][s] = {}
        st.session_state['show_paraphrase'][s] = False

    # 执行请求，实际生成部分
    results = generate_sections_content(num_results, sections, title)

    # 将这些行移动到这里，以将st代码与逻辑分离
    for i, s in enumerate(sections):
        response_json = results[i]
        section_completions = response_json["completions"]  # 获取当前完成的生成候选项
        st.session_state['generated_sections_data'][s]["completions"] = section_completions

    # 排名/过滤
    for i, s in enumerate(sections):
        response_json = results[i]
        section_completions = response_json["completions"]
        st.session_state['generated_sections_data'][s]["completions"] = section_completions

        lengths = []
        for c in range(len(section_completions)):
            l = len(section_completions[c]["data"]["text"])
            lengths.append(l)

        arg_sort = np.argsort(lengths)
        index = 2
        st.session_state['generated_sections_data'][s]["text_area_index"] = index
        st.session_state['generated_sections_data'][s]["arg_sort"] = arg_sort

        st.session_state['generated_sections_data'][s]["rewrites"] = ["" for c in range(len(section_completions))]


def build_event_loop(title, section_heading, num_results):
    return lambda: get_event_loop(title, section_heading, num_results)


def build_event_loop_one_section(title, section, num_results):
    return lambda: get_event_loop(title, [section], num_results)


def on_outline_change():
    st.session_state['show_sections'] = False


def paraphrase(text, tone, times):
    len_text = len(text)
    entire_text = text
    for i in range(times):
        if len_text > 500:
            sentences = text.split(".")
        else:
            sentences = [text]

        filtered_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            len_sent = len(sentence)
            if len_sent > 1:
                filtered_sentences.append(sentence)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        group = asyncio.gather(*[paraphrase_req(sentence, tone) for sentence in filtered_sentences])

        results = loop.run_until_complete(group)
        loop.close()

        final_text = []
        for r in results:
            sugg = r["suggestions"][0]["text"]
            final_text.append(sugg)

        entire_text = ". ".join(final_text)
        entire_text = (entire_text + ".").replace(",.", ".").replace("?.", ".").replace("..", ".")

        text = entire_text
        len_text = len(entire_text)

    return entire_text


def on_paraphrase_click(s, tone, times):

    all_sections_data = st.session_state['generated_sections_data']

    index = st.session_state['generated_sections_data'][s]["text_area_index"]
    section_completions = all_sections_data[s]["completions"]

    sec_text = section_completions[index]["data"]["text"]
    paraphrased_section = paraphrase(sec_text, tone, times)

    st.session_state['generated_sections_data'][s]["rewrites"][index] = paraphrased_section
    st.session_state['show_paraphrase'][s] = True


def build_paraphrase(s, tone, times):
    return lambda: on_paraphrase_click(s, tone, times)


def on_heading_change():
    st.session_state['show_sections'] = False


def on_title_change():
    st.session_state['show_sections'] = False


if __name__ == '__main__':
    args = get_args()
    apply_studio_style()
    num_results = args.num_results

    # 初始化
    if 'show_outline' not in st.session_state:
        st.session_state['show_outline'] = False

    if 'show_sections' not in st.session_state:
        st.session_state['show_sections'] = False

    if 'show_paraphrase' not in st.session_state:
        st.session_state['show_paraphrase'] = {}

    if 'generated_sections_data' not in st.session_state:
        st.session_state['generated_sections_data'] = {}

    st.title("博客文章生成器")
    st.markdown("只需一个标题，您就可以立即生成整篇文章！只需选择您的主题，这个工具将为您从头到尾创建一篇引人入胜的文章。")
    st.markdown("#### 博客标题")
    title = st.text_input(label="在这里写下您文章的标题：", placeholder="",
                        value="5种克服写作障碍的策略").strip()
    st.markdown("#### 博客大纲")
    st.text("点击按钮生成博客大纲")
    st.button(label="生成大纲", on_click=build_generate_outline(title))

    sections = []
    if st.session_state['show_outline']:
        text_area_outline = st.text_area(label=" ", height=250, value=st.session_state["outline"],
                                         on_change=on_outline_change)
        sections = text_area_outline.split("\n")
        st.text("对生成的大纲不满意？再次点击'生成大纲'按钮重新生成它，或在线编辑它。")

        st.markdown("#### 博客内容")
        st.text("点击按钮轻松为您的博客文章生成大纲：")
        st.button(label="生成部分", on_click=build_event_loop(title, sections, num_results))

    if st.session_state['show_sections']:
        st.markdown(f"**{title}**")
        for s in sections:
            st.session_state['generated_sections_data'][s]["text_area_data"] = st.empty()
            st.session_state['generated_sections_data'][s]["cols"] = st.empty()

        all_sections_data = st.session_state['generated_sections_data']
        for i, s in enumerate(st.session_state['generated_sections_data'].keys()):
            index = st.session_state['generated_sections_data'][s]["text_area_index"]
            section_completions = all_sections_data[s]["completions"]
            arg_sort = st.session_state['generated_sections_data'][s]["arg_sort"]

            section_text_area_value = st.session_state['generated_sections_data'][s]["rewrites"][index] if st.session_state['show_paraphrase'][s] == True else section_completions[
                                                                                                            index]["data"]["text"]
            section_i_text = st.session_state['generated_sections_data'][s]["text_area_data"].text_area(label=s,
                                                                                                        height=300,
                                                                                                        value=section_text_area_value,
                                                                                                        key="generated-section"+s)
            st.session_state['generated_sections_data'][s]["completions"][index]["data"]["text"] = section_i_text
            col1, col2, col3, col4, col5, col6 = st.session_state['generated_sections_data'][s]["cols"].columns(
                [0.2, 0.2, 0.06, 0.047, 0.05, 0.4])

            with col1:
                st.button("重新生成", on_click=build_event_loop_one_section(title, s, num_results),
                          key="generate-again-" + s)

            with col2:
                st.button("释义", on_click=build_paraphrase(s, tone="general", times=1),
                          key="paraphrase-button-" + s)

            with col3:
                st.button("<", on_click=build_on_prev_click(s, i, section_completions, arg_sort), key="<" + s)

            with col4:
                st.text(f"{index+1}/{num_results}")

            with col5:
                st.button(">", on_click=build_on_next_click(s, i, section_completions, arg_sort), key=">" + s)
