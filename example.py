import random
import time
import streamlit as st

from streamlit_markdown import streamlit_markdown


markdown_text = """
This is a table:

| Vegetable | Description |
|-----------|-------------|
| Carrot    | A crunchy, orange root vegetable that is rich in vitamins and minerals. It is commonly used in soups, salads, and as a snack. |
| Broccoli  | A green vegetable with tightly packed florets that is high in fiber, vitamins, and antioxidants. It can be steamed, boiled, stir-fried, or roasted. |
| Spinach   | A leafy green vegetable that is dense in nutrients like iron, calcium, and vitamins. It can be eaten raw in salads or cooked in various dishes. |
| Bell Pepper | A colorful, sweet vegetable available in different colors such as red, yellow, and green. It is often used in stir-fries, salads, or stuffed recipes. |
| Tomato    | A juicy fruit often used as a vegetable in culinary preparations. It comes in various shapes, sizes, and colors and is used in salads, sauces, and sandwiches. |
| Cucumber   | A cool and refreshing vegetable with a high water content. It is commonly used in salads, sandwiches, or as a crunchy snack. |
| Zucchini | A summer squash with a mild flavor and tender texture. It can be sautéed, grilled, roasted, or used in baking recipes. |
| Cauliflower | A versatile vegetable that can be roasted, steamed, mashed, or used to make gluten-free alternatives like cauliflower rice or pizza crust. |
| Green Beans | Long, slender pods that are low in calories and rich in vitamins. They can be steamed, stir-fried, or used in casseroles and salads. |
| Potato | A starchy vegetable available in various varieties. It can be boiled, baked, mashed, or used in soups, fries, and many other dishes. |

This is a mermaid diagram:

```mermaid
gitGraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    commit
```

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
\\[F(x) = \\int_{a}^{b} f(x) \\, dx\\]
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

content = st.text_area("Markdown", markdown_text, height=250)
a, b, c, d = st.columns(4)
streaming = d.checkbox("Streaming", False)
partial = a.checkbox("Partial", False)
richContent = b.checkbox("Rich Content", True)
background_color = c.selectbox("Background Color", ["blue", "orange", "green"])

if not streaming:
    streamlit_markdown(
        content,
        partial=partial,
        richContent=richContent,
        background_color=background_color,
        key="content",
    )
else:
    if "n_chars" not in st.session_state:
        st.session_state.n_chars = 1

    streamlit_markdown(
        content[: st.session_state.n_chars],
        partial=st.session_state.n_chars < len(content),
        richContent=richContent,
        background_color=background_color,
        key="content",
    )

    # Simulate streaming
    if st.session_state.n_chars < len(content):
        st.session_state.n_chars += random.randint(1, 5)
        time.sleep(0.05)
        st.rerun()
    else:
        st.session_state.n_chars = 1
        st.rerun()
