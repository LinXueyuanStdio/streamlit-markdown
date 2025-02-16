from __future__ import annotations
from typing import *

from streamlit import __version__
from streamlit.proto.Element_pb2 import Element
from streamlit.delta_generator import DeltaGenerator

import streamlit.components.v1 as v1
if hasattr(v1, "custom_component"):
    from streamlit.components.v1.custom_component import CustomComponent
else:
    from streamlit.components.v1.components import CustomComponent

try:
    from streamlit_markdown.st_hack_v1 import marshall_component
except:
    from streamlit_markdown.st_hack_v2 import marshall_component



def st_hack_component(
    parent: DeltaGenerator,
    component: CustomComponent,
    key=None,
    default: Any = None,
    **kwargs,
):
    element = Element()
    component_proto, return_value = marshall_component(
        component,
        parent,
        element,
        key,
        default,
        **kwargs,
    )

    return parent._enqueue("component_instance", component_proto, return_value)

