import time
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(max_retries=5)

schema={
    "type": "object",
        "properties": {
            "results":{
                "type":"array",
                "items":{
                    "type":"object",
                    "properties": {
                        "genre": {"type":"string","enum":["PROFANITY", "ROMANTIC/EXPLICIT CONTENT", "DARK/HEAVY THEMES", "VIOLENCE/SCARINESS", "ALCOHOL/SUBSTANCE USE"]},
                        "analysis":{"type":"string","description":"The summarized description of how the content displays inappropriate content of the specified genre."},
                        "quotes":{"type":"array","items": {"type":"string","description":"An exact quote pulled from the given text that displays the use of the specified genre of inappropriate content in the text."}},
                        "severity_score":{"type":"integer","description":"An integer from 1 to 10."}
            },
            "required":["genre", "analysis", "quotes", "severity_score"],
            "additionalProperties": False
            },
        }
    },
    "required":['results'],
    "additionalProperties": False
}
with open("rubric.txt") as rubric_file:
    rubric=rubric_file.read()
def api_request(wait, prompt, text, rubric=rubric):
    sys_prompt = f'''You are analyzing and evaluating text for inappropriate content (specified in the prompt). For a part of your JSON output,
    called the severity score in the user prompt, you are to grade the text based on the specified genre using a rubric. This is the rubric you will use:
    {rubric}'''
    try:
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=16000,
            system=sys_prompt,
            messages=[{"role": "user", "content": f"{prompt}\nText:{text}"}],
            output_config={"format": {"type": "json_schema", "schema": schema}},
        )
        if response.stop_reason == "max_tokens":
            raise ValueError("Response was cut off before finishing")
        return next(b.text for b in response.content if b.type == "text")
    except anthropic.RateLimitError as e:
        print(f"Rate limit hit (after automatic retries): {e}")
        raise
    except anthropic.BadRequestError as e:
        if "credit balance" in str(e).lower():
            raise RuntimeError("API credits used up") from e
        raise
def title_request(wait, prompt, text):
    sys_prompt = '''You are given the task of generating a title for a given text. When given this task, you will solely
    output the generated title, with zero prose or extra characters before or after the output.'''
    try:
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1000,
            system=sys_prompt,
            messages=[{"role": "user", "content": f"{prompt}\nText:{text}"}],
        )
        if response.stop_reason == "max_tokens":
            raise ValueError("Response was cut off before finishing")
        return next(b.text for b in response.content if b.type == "text")
    except anthropic.RateLimitError as e:
        print(f"Rate limit hit (after automatic retries): {e}")
        raise
    except anthropic.BadRequestError as e:
        if "credit balance" in str(e).lower():
            raise RuntimeError("API credits used up") from e
        raise