import json
import random
import time
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
tokenizer = AutoTokenizer.from_pretrained("/cpfs/29583eqvgtdvw5cvegg/data/shared/AIME-COMMON/runs/240528/llama3_base_cn_business_16k")

app = FastAPI()


# async def generate():
#     inputs = tokenizer(["An increasing sequence: one,"], return_tensors="pt")
#     streamer = TextIteratorStreamer(tokenizer)
#     generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=20)
#     thread = Thread(target=model.generate, kwargs=generation_kwargs)
#     thread.start()
#     for new_text in streamer:
#         yield new_text


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
    inputs = tokenizer([text], return_tensors="pt")
    streamer = TextIteratorStreamer(tokenizer)
    generation_kwargs = dict(inputs=inputs, streamer=streamer)
    thread = Thread(target=fake_generation, kwargs=generation_kwargs)
    thread.start()
    for new_text in streamer:
        yield new_text


@app.get("/")
async def main():
    text = """
This is a table:

| Title | Description |
|-----------|-------------|
| text    | hello world |
| math  | $y=f(x)$ |
| reference  | cite[^1][^2] |

This is a mermaid diagram:

```mermaid
sequenceDiagram
   autonumber
   participant 归档标准数据v1
   participant 归档配置planning
   actor 算法侧数据处理
   participant 预标注模型
   participant 工具执行
   participant 归档标准数据v2
   归档标准数据v1 ->> 算法侧数据处理: query, time, nlu
   归档配置planning ->> 算法侧数据处理: tools[develop], time_format
   归档配置planning ->> 算法侧数据处理: planning_prompt[develop]
   算法侧数据处理 ->>+ 预标注模型: planning_instruction[develop]
   loop 直到 ActionList==<Finished>
      预标注模型 ->>+ 工具执行:   Thought, ActionList
      工具执行   ->>- 预标注模型: Action, ActionInput, Observation, ObservationObejct
   end
   预标注模型 ->>- 算法侧数据处理: steps
   算法侧数据处理 ->> 归档标准数据v2: query, time, nlu, steps
```

```latex
F(x) = \int_{a}^{b} f(x) \, dx
```

行内数学公式 $y=f(x)$ 自变量为 $x$，因变量为 $y$。

$$y=f(x)$$

# Heading level 1

This is the first paragraph.

This is the second paragraph.

This is the third paragraph.

## Heading level 2

This is an [anchor](https://github.com).

### Heading level 3

This is **bold** and _italics_.

#### Heading level 4

This is `inline` code.

This is a code block:

```tsx
const Message = () => {
  return <div>hi</div>;
};
```

##### Heading level 5

This is an unordered list:

- One
- Two
- Three, and **bold**

This is an ordered list:

1. One
1. Two
1. Three

This is a complex list:

1. **Bold**: One
    - One
    - Two
    - Three

2. **Bold**: Three
    - One
    - Two
    - Three

3. **Bold**: Four
    - One
    - Two
    - Three

###### Heading level 6

> This is a blockquote.

"""
    return StreamingResponse(generate_fake_markdown(text))


@app.get("/query")
async def query(instruction: str):
    text = """
This is a table:

| Title | Description |
|-----------|-------------|
| text    | hello world |
| math  | $y=f(x)$ |
| reference  | cite[^1][^2] |

This is a mermaid diagram:

```mermaid
sequenceDiagram
   autonumber
   participant 归档标准数据v1
   participant 归档配置planning
   actor 算法侧数据处理
   participant 预标注模型
   participant 工具执行
   participant 归档标准数据v2
   归档标准数据v1 ->> 算法侧数据处理: query, time, nlu
   归档配置planning ->> 算法侧数据处理: tools[develop], time_format
   归档配置planning ->> 算法侧数据处理: planning_prompt[develop]
   算法侧数据处理 ->>+ 预标注模型: planning_instruction[develop]
   loop 直到 ActionList==<Finished>
      预标注模型 ->>+ 工具执行:   Thought, ActionList
      工具执行   ->>- 预标注模型: Action, ActionInput, Observation, ObservationObejct
   end
   预标注模型 ->>- 算法侧数据处理: steps
   算法侧数据处理 ->> 归档标准数据v2: query, time, nlu, steps
```

```latex
F(x) = \int_{a}^{b} f(x) \, dx
```

行内数学公式 $y=f(x)$ 自变量为 $x$，因变量为 $y$。

$$y=f(x)$$

# Heading level 1

This is the first paragraph.

This is the second paragraph.

This is the third paragraph.

## Heading level 2

This is an [anchor](https://github.com).

### Heading level 3

This is **bold** and _italics_.

#### Heading level 4

This is `inline` code.

This is a code block:

```tsx
const Message = () => {
  return <div>hi</div>;
};
```

##### Heading level 5

This is an unordered list:

- One
- Two
- Three, and **bold**

This is an ordered list:

1. One
1. Two
1. Three

This is a complex list:

1. **Bold**: One
    - One
    - Two
    - Three

2. **Bold**: Three
    - One
    - Two
    - Three

3. **Bold**: Four
    - One
    - Two
    - Three

###### Heading level 6

> This is a blockquote.

"""
    return StreamingResponse(generate_fake_markdown(text))


send_index = {}
recv_memory = {}

@app.websocket("/content")
async def websocket_endpoint(id: str, server: int, websocket: WebSocket):
    await websocket.accept()
    while True:
        if server == 1:
            if id not in recv_memory:
                recv_memory[id] = ""
            print(f"Server {server} waiting message from {id}")
            while data := await websocket.receive_text():
                recv_memory[id] += data
                print(f"Server {server} received message from {id}: {data}")
            await websocket.close()
            break
        else:
            if id not in recv_memory:
                time.sleep(1)
                # 等待接收端准备好
                continue
            if id not in send_index:
                send_index[id] = 0
            while send_index[id] < len(recv_memory[id]):
                data = recv_memory[id][send_index[id]: send_index[id] + 10]
                send_index[id] += 10
                print(f"Server {server} send message to {id}: {data}  | {len(recv_memory[id])}")
                await websocket.send_text(data)
                time.sleep(0.1)
            await websocket.close()
            break


if __name__ == "__main__":
    import uvicorn

    # usage:
    # curl -N localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
