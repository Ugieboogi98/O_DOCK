import json
from app.core.config import get_settings


def model():
    from langchain_openai import ChatOpenAI

    s = get_settings()
    if not s.llm_api_key:
        raise ValueError("LLM_KEY_MISSING")
    return ChatOpenAI(
        api_key=s.llm_api_key,
        base_url=s.llm_base_url,
        model=s.llm_model,
        temperature=0,
        timeout=45,
        max_retries=2,
    )


def call(prompt, payload, json_output=False):
    from langchain_core.messages import SystemMessage, HumanMessage

    s = get_settings()
    if s.llm_api_mode == "responses":
        from openai import OpenAI

        if not s.llm_api_key:
            raise ValueError("LLM_KEY_MISSING")
        client = OpenAI(
            api_key=s.llm_api_key, base_url=s.llm_base_url, timeout=45, max_retries=2
        )
        instruction = prompt + (
            "\nReturn only a valid JSON object, without Markdown fences."
            if json_output
            else ""
        )
        result = client.responses.create(
            model=s.llm_model,
            input=[
                {"role": "system", "content": instruction},
                {
                    "role": "user",
                    "content": json.dumps(payload, ensure_ascii=False, default=str),
                },
            ],
        )
        if result.status != "completed" or not result.output_text:
            raise ValueError("MODEL_FORMAT_ERROR")
        return json.loads(result.output_text) if json_output else result.output_text
    if s.llm_api_mode != "chat":
        raise ValueError("LLM_API_MODE_INVALID")
    llm = model()
    if json_output:
        llm = llm.bind(response_format={"type": "json_object"})
    result = llm.invoke(
        [
            SystemMessage(content=prompt),
            HumanMessage(content=json.dumps(payload, ensure_ascii=False, default=str)),
        ]
    )
    text = result.content
    if not isinstance(text, str):
        raise ValueError("MODEL_FORMAT_ERROR")
    return json.loads(text) if json_output else text
