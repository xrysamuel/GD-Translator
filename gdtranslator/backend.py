from openai import OpenAI

from .cache import cached_generator
from .config import ServerConfig

def get_context(source_text):
    context = []
    system_prompt = "你是一位精通简体中文的专业翻译，尤其擅长英译中翻译，你不仅会注意翻译时的准确性，并且你的翻译结果总是符合中文的表达习惯。\n在翻译时，不要作出任何额外的解释，你只需要翻译用户给出的文本。\n保留特定的英文术语、数字或名字，并在其前后加上空格，例如：“生成式 AI 产品”，“不超过 10 秒”。"
    example_source_text = "From protein sequencing to electron microscopy, and from archaeology to astronomy, here are seven technologies that are likely to shake up science in the year ahead."
    example_target_text = "从蛋白质测序到电子显微镜，从考古学到天文学，这七项技术可能会在未来一年震动科学界的技术。"
    context.append({"role": "system", "content": system_prompt})
    context.append(
        {
            "role": "user",
            "content": f"{example_source_text}",
        }
    )
    context.append(
        {
            "role": "assistant",
            "content": f"{example_target_text}",
        }
    )
    context.append(
        {
            "role": "user",
            "content": f"{source_text}",
        }
    )
    return context


@cached_generator(capacity=1000)
def generate_translate(source_text: str, server_config: ServerConfig):
    chunks = []
    client = OpenAI(api_key=server_config.api_key, base_url=server_config.base_url)
    response = client.chat.completions.create(
        model=server_config.model,
        messages=get_context(source_text),
        stream=True,
        temperature=1.0,
        stream_options={"include_usage": True},
    )
    for chunk in response:
        chunks.append(chunk)
        chunk_message = chunk.choices[0].delta.content
        if chunk.usage is not None:
            total_price = (
                chunk.usage.prompt_tokens * server_config.price["input"]
                + chunk.usage.completion_tokens * server_config.price["output"]
            )
            chunk_message += f" （{total_price}￥）"
        yield chunk_message