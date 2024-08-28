# AILab Studio 演示

这个仓库展示了以下AI21大型语言模型（LLM）的用例示例，使用Streamlit应用程序实现：
- 博客文章生成器（Blog Post Generator）
- 产品描述生成器（Product Description Generator）
- 带有文章摘要的推销邮件和社交媒体生成器（Pitch Email and Social Media Generator with Article Summerization）
- 主题分类器（Topic Classifier）
- 同义替换与重写工具（Paraphrases & Rewrites Tool）
- 文档和网站摘要器（Document and Website Summarizer）
- 上下文答案（Contextual Answers）
- 多文档问答（Multiple Document Q&A）

[Streamlit演示应用程序](https://ai21-studio-demos.streamlit.app/)

# 使用你的AI21账户设置应用程序
- 在`.streamlit`文件夹中创建`secrets.toml`，并添加你的凭证（将`<YOUR_API_KEY>`替换为你的AI21 API密钥）：
```
[api-keys]
ai21-api-key = "<YOUR_API_KEY>"
```
- 运行`Welcome.py`

## 请求AI21账户和API密钥
- [创建](https://studio.ai21.com/login) 你的AI21账户
- 定位你的[AI21 API密钥](https://studio.ai21.com/account/api-key)
