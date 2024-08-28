from ai21 import AI21Client
import streamlit as st

client = AI21Client(api_key=st.secrets['api-keys']['ai21-api-key'])

DEFAULT_MODEL = 'j2-ultra'

SUMMARIZATION_URL = "https://www.5loi.com/blog/technology-strategy-thoughts"
SUMMARIZATION_TEXT = '''
或许没有其他现代历史危机像 COVID-19 这样对日常生活产生了如此巨大的影响。也没有任何危机像这样迫使全球企业加速演变，因为它们的领导者在应对和恢复的过程中努力适应后疫情时代的繁荣环境。

德勤私人公司对私人企业的最新全球调查显示，各地区的高管都利用这场危机作为催化剂，加速了我们工作和生活方式几乎所有方面的变革。他们通过增加科技投资和部署，加快了数字化转型。正在进行的计划被推向完成，而那些还停留在构想阶段的计划则被付诸实践。他们寻找新的合作伙伴关系和联盟。他们寻求新的机会来加强他们的供应链网络并扩大市场。他们加大了努力去理解他们的目的不仅仅是盈利，寻找新的可持续增长的方式，并与员工、客户和其他关键利益相关者加强信任。他们也接受了关于工作方式和地点的新可能性。
'''

CLASSIFICATION_FEWSHOT="""将以下新闻文章分类到以下主题之一：
1. 世界
2. 体育
3. 商业
4. 科学和技术
标题：
天文学家观测到星系碰撞，形成更大的星系
摘要：
一个国际天文学家团队获得了两个遥远星系团合并的最清晰图像，称之为有史以来见证的最强大的宇宙事件之一。
这篇文章的主题是：
科学和技术

---

将以下新闻文章分类到以下主题之一：
1. 世界
2. 体育
3. 商业
4. 科学和技术
标题：
美国军事车队附近发生爆炸 (美联社)
摘要：
美联社 - 伊拉克警方表示，一枚汽车炸弹在周日清晨在美国军事车队前往巴格达机场的路上爆炸，据目击者称两辆悍马车被摧毁。
这篇文章的主题是：
世界

---

将以下新闻文章分类到以下主题之一：
1. 世界
2. 体育
3. 商业
4. 科学和技术
标题：
马拉多纳前往古巴
摘要：
前阿根廷足球明星迭戈·阿曼多·马拉多纳于周一前往古巴继续治疗他的药物成瘾问题。
这篇文章的主题是：
体育

---

将以下新闻文章分类到以下主题之一：
1. 世界
2. 体育
3. 商业
4. 科学和技术
标题：
杜克第三季度收益激增
摘要：
杜克能源公司公布第三季度净收入为3.89亿美元，或每股摊薄收益41美分，远高于去年同期的净收入4900万美元，或每股摊薄收益5美分。
这篇文章的主题是：
商业

"""

CLASSIFICATION_PROMPT="""将以下新闻文章分类到以下主题之一：
1. 世界
2. 体育
3. 商业
4. 科学和技术"""

CLASSIFICATION_TITLE = "华盛顿特区公布体育场计划"

CLASSIFICATION_DESCRIPTION = "有传言称，美国职业棒球大联盟（Major League Baseball）越来越接近将博览会队（Expos，现已不存在）迁移到华盛顿，与此同时华盛顿特区的官员宣布了在阿纳科斯提亚河滨地区建造一座体育场的计划。"

PRODUCT_DESCRIPTION_FEW_SHOT = '''根据特性列表为时尚电子商务网站撰写产品描述。
产品：全光谱合身A字裙
特性：
- 由 Retrolicious 设计
- 弹力棉质面料
- 侧口袋
- 彩虹条纹印花
描述：这款来自 Retrolicious 的杰出滑板裙，采用了大胆的彩虹条纹印花，由特别鲜艳的色彩组成，它在复古风格中独树一帜。由弹力棉质面料制成，拥有圆领、无袖合身上身，以及带有便利侧口袋的蓬蓬A字裙，这款可爱的合身A字裙确实独一无二，复古而时尚。

##

根据特性列表为时尚电子商务网站撰写产品描述。
产品：营地总监斜挎包
特性：
- 黑色帆布手提包
- 彩虹太空印花
- 皮革饰边
- 两个安全拉链隔层
描述：带上这款黑色帆布手提包，无论走到哪里都带上一些营地的魅力吧！这款手提包装饰有彩虹太空图案印花、黑色仿皮革饰边、两个安全拉链隔层和可调节的斜挎带，这款 ModCloth 专属包包确保你无论在何处漫步都能吸引微笑。

##

根据特性列表为时尚电子商务网站撰写产品描述。'''

OBQA_CONTEXT = """大型语言模型
我们产品核心的介绍

自从引入大型语言模型（LLMs）以来，自然语言处理（NLP）在过去几年中取得了飞速发展。这些庞大的模型基于 Transformer 架构，这使得训练更大、更强大的语言模型成为可能。
我们将 LLMs 分为两大类：自回归和掩蔽语言模型（Masked LM）。在本页面中，我们将专注于自回归 LLMs，因为我们的语言模型 Jurassic-1 系列属于这一类。

⚡ 任务：预测下一个词
自回归 LLM 是一个由数十亿参数组成的神经网络模型。它经过大量文本的训练，目标只有一个：基于给定的文本预测下一个词。通过多次重复这一动作，每次都将预测的词添加到提供的文本中，你最终会得到一个完整的文本（例如完整的句子、段落、文章、书籍等）。在术语上，文本输出（完整的文本）称为补全，而输入（给定的、原始的文本）称为提示。

🎓 附加价值：知识获取
想象一下，如果你不得不反复阅读莎士比亚的所有作品来学习一门语言。最终，你不仅能够记住他所有的戏剧和诗歌，还能够模仿他的写作风格。
以类似的方式，我们通过提供许多文本来源来训练 LLMs。这使它们能够深入理解英语以及一般知识。

🗣️ 与大型语言模型交互
LLMs 使用自然语言进行查询，也称为提示工程。
与编写代码行和加载模型不同，你编写自然语言提示并将其作为输入传递给模型。

⚙️ 资源密集型
训练和部署大型语言模型需要数据、计算和工程资源。例如我们的 Jurassic-1 模型这样的 LLMs 在这里发挥重要作用，为学术研究人员和开发人员提供这种技术类型的访问。

分词器和分词

现在你知道了什么是大型语言模型，你一定想知道：“神经网络如何使用文本作为输入和输出？”

答案是：分词 🧩
任何语言都可以分解成基本的部分（在我们的情况下，是分词）。每个部分都被转换成它自己的向量表示，最终输入到模型中。例如：
每个模型都有自己的分词字典，这决定了它“说”的语言。输入中的每段文本都将分解为这些分词，模型生成的每段文本都将由它们组成。
但是我们如何分解一种语言呢？我们选择哪些部分作为我们的分词呢？有几种方法可以解决这个问题：

🔡 字符级分词
作为一种简单的解决方案，每个字符可以被视为自己的分词。通过这样做，我们可以用仅仅 26 个字符来表示整个英语语言（好吧，为大写字母翻倍并添加一些标点符号）。这将给我们一个小型的分词字典，从而减少这些向量所需的宽度，并为我们节省一些宝贵的内存。然而，这些分词没有任何固有的意义 - 我们都知道“Cat”的意思是什么，但是“C”的意思是什么？理解语言的关键是上下文。尽管对于我们读者来说，“Cat”和“Cradle”有不同的意思很清楚，但对于使用这种分词器的语言模型来说 - “C”是相同的。

🆒 单词级分词
我们可以尝试的另一种方法是将我们的文本分解成单词，就像上面的例子（"I want to break free"）。
现在，每个分词都有模型可以学习并使用的含义。我们获得了意义，但这需要一个更大的字典。此外，它引发了另一个问题：像 “helped”，“helping” 和 “helpful” 这样来自同一个根词的单词呢？在这种方法中，这些单词中的每一个都会得到一个不同的分词，它们之间没有固有的联系，尽管对于我们读者来说，它们都有类似的意思。
此外，单词在组合在一起时可能具有根本不同的含义 - 例如，我的破旧汽车没有在任何地方行驶。如果我们进一步发展呢？

💬 句子级分词
在这种方法中，我们将文本分解成句子。这将捕获有意义的短语！然而，这将导致一个荒谬的大字典，其中一些分词非常罕见，我们将需要大量的数据来教模型每个分词的含义。

🏅 哪个最好？
每种方法都有优点和缺点，像任何现实生活问题一样，最好的解决方案涉及一定程度的妥协。5Loi AILab 使用一个大型分词字典（250K），其中包含每种方法的一些：单独的字符、单词、单词部分如前缀和后缀，以及许多多词分词。"""

OBQA_QUESTION = "有哪些分词方法？"

DOC_QA = "您想知道些什么？"
