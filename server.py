import json
import random
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from transformers import AutoTokenizer, TextIteratorStreamer
from threading import Thread

app = FastAPI()


def simulated_token_stream(content):
    import random

    length = 0
    while length < len(content):
        n_chars = random.randint(5, 15)
        yield content[length : length + n_chars]
        length += n_chars
        time.sleep(0.05)


@app.get("/simulated_token_stream")
async def main(text):
    return StreamingResponse(simulated_token_stream(text))

# from transformers import AutoModel
# tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
# model = AutoModel.from_pretrained("openai-community/gpt2")
# async def generate(instruction):
#     inputs = tokenizer([instruction], return_tensors="pt")
#     streamer = TextIteratorStreamer(tokenizer)
#     generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=20)
#     thread = Thread(target=model.generate, kwargs=generation_kwargs)
#     thread.start()
#     for new_text in streamer:
#         yield new_text
#
# @app.get("/simulated_with_local_model")
# async def simulated_with_local_model(instruction):
#     return StreamingResponse(generate(instruction))


def fake_generation(inputs, streamer: TextIteratorStreamer):
    ids = inputs.input_ids[0]
    length = 0
    while length < len(ids):
        token_id = ids[length: length + random.randint(5, 20)]
        length += len(token_id)
        streamer.put(token_id)
        time.sleep(0.3)
    streamer.end()


async def generate_fake_markdown(text):
    tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
    inputs = tokenizer([text], return_tensors="pt")
    streamer = TextIteratorStreamer(tokenizer)
    generation_kwargs = dict(inputs=inputs, streamer=streamer)
    thread = Thread(target=fake_generation, kwargs=generation_kwargs)
    thread.start()
    for new_text in streamer:
        yield new_text


@app.get("/simulated_with_tokenizer")
async def simulated_with_tokenizer(text: str):
    return StreamingResponse(generate_fake_markdown(text))


if __name__ == "__main__":
    import uvicorn

    # usage:
    # curl -N localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
