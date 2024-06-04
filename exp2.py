# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import time
from types import TracebackType
from typing import Literal, cast

from typing_extensions import TypeAlias

from streamlit.cursor import Cursor
from streamlit.delta_generator import DeltaGenerator, _enqueue_message
from streamlit.errors import StreamlitAPIException
from streamlit.proto.Block_pb2 import Block as BlockProto
from streamlit.proto.ForwardMsg_pb2 import ForwardMsg

from streamlit import _main, type_util
from streamlit.components.types.base_custom_component import BaseCustomComponent
from streamlit.elements.form import current_form_id
from streamlit.elements.utils import check_cache_replay_rules
from streamlit.errors import StreamlitAPIException
from streamlit.proto.Components_pb2 import ArrowTable as ArrowTableProto
from streamlit.proto.Components_pb2 import SpecialArg
from streamlit.proto.Components_pb2 import ComponentInstance
from streamlit.proto.Element_pb2 import Element
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.state import NoValue, register_widget
from streamlit.runtime.state.common import compute_widget_id
from streamlit.type_util import to_bytes
from streamlit.delta_generator import DeltaGenerator
from typing import *
from streamlit_markdown import _markdown


class MarshallComponentException(StreamlitAPIException):
    """Class for exceptions generated during custom component marshalling."""

    pass


def marshall_component(
    self, dg: DeltaGenerator, element: Element, key, default, **kwargs
) -> ComponentInstance:
    all_args = dict(kwargs, **{"default": default, "key": key})

    json_args = {}
    special_args = []
    for arg_name, arg_val in all_args.items():
        json_args[arg_name] = arg_val

    try:
        serialized_json_args = json.dumps(json_args)
    except Exception as ex:
        raise MarshallComponentException("Could not convert component args to JSON", ex)
    element.component_instance.component_name = self.name
    element.component_instance.form_id = current_form_id(dg)
    if self.url is not None:
        element.component_instance.url = self.url

    # Normally, a widget's element_hash (which determines
    # its identity across multiple runs of an app) is computed
    # by hashing its arguments. This means that, if any of the arguments
    # to the widget are changed, Streamlit considers it a new widget
    # instance and it loses its previous state.
    #
    # However! If a *component* has a `key` argument, then the
    # component's hash identity is determined by entirely by
    # `component_name + url + key`. This means that, when `key`
    # exists, the component will maintain its identity even when its
    # other arguments change, and the component's iframe won't be
    # remounted on the frontend.

    def marshall_element_args():
        element.component_instance.json_args = serialized_json_args
        element.component_instance.special_args.extend(special_args)

    ctx = get_script_run_ctx()

    if key is None:
        marshall_element_args()
        computed_id = compute_widget_id(
            "component_instance",
            user_key=key,
            name=self.name,
            form_id=current_form_id(dg),
            url=self.url,
            key=key,
            json_args=serialized_json_args,
            special_args=special_args,
            page=ctx.page_script_hash if ctx else None,
        )
    else:
        computed_id = compute_widget_id(
            "component_instance",
            user_key=key,
            name=self.name,
            form_id=current_form_id(dg),
            url=self.url,
            key=key,
            page=ctx.page_script_hash if ctx else None,
        )
    element.component_instance.id = computed_id
    return element.component_instance


States: TypeAlias = Literal["running", "complete", "error"]


class MarkdownContainer(DeltaGenerator):
    @staticmethod
    def _create(
        parent: DeltaGenerator,
        content: str,
        state: States = "running",
        richContent: bool = True,
        theme_color: Literal["blue", "orange", "green"] = "green",
        key=None,
        default: Any = None,
        **kwargs,
    ) -> MarkdownContainer:
        element = Element()
        kwargs["content"] = content
        kwargs["state"] = state
        kwargs["richContent"] = richContent
        kwargs["theme_color"] = theme_color
        markdown_proto = marshall_component(
            _markdown, parent, element, key, default, **kwargs
        )

        delta_path: list[int] = (
            parent._active_dg._cursor.delta_path if parent._active_dg._cursor else []
        )

        markdown_container = cast(
            MarkdownContainer,
            parent._enqueue(
                "component_instance", markdown_proto, None
            ),
        )

        # Apply initial configuration
        markdown_container._delta_path = delta_path
        markdown_container._current_proto = markdown_proto
        markdown_container._current_state = state
        markdown_container._key = key

        # We need to sleep here for a very short time to prevent issues when
        # the status is updated too quickly. If an .update() directly follows the
        # the initialization, sometimes only the latest update is applied.
        # Adding a short timeout here allows the frontend to render the update before.
        time.sleep(0.05)

        return markdown_container

    def __init__(
        self,
        root_container: int | None,
        cursor: Cursor | None,
        parent: DeltaGenerator | None,
        block_type: str | None,
    ):
        super().__init__(root_container, cursor, parent, block_type)

        # Initialized in `_create()`:
        self._current_proto: BlockProto | None = None
        self._current_state: States | None = None
        self._key: str | None = None
        self._delta_path: list[int] | None = None

    def update(
        self,
        *,
        content: str | None = None,
        state: States | None = None,
    ) -> None:
        """Update the status container.

        Only specified arguments are updated. Container contents and unspecified
        arguments remain unchanged.

        Parameters
        ----------
        content : str or None
            A new label of the status container. If None, the label is not
            changed.

        state : "running", "complete", "error", or None
            The new state of the status container. This mainly changes the
            icon. If None, the state is not changed.
        """
        assert self._current_proto is not None, "Status not correctly initialized!"
        assert self._delta_path is not None, "Status not correctly initialized!"

        msg = ForwardMsg()
        msg.metadata.delta_path[:] = self._delta_path
        msg.delta.add_block.CopyFrom(self._current_proto)

        if content is not None:
            msg.delta.add_block.expandable.label = content

        if state is not None:
            if state == "running":
                msg.delta.add_block.expandable.icon = "spinner"
            elif state == "complete":
                msg.delta.add_block.expandable.icon = "check"
            elif state == "error":
                msg.delta.add_block.expandable.icon = "error"
            else:
                raise StreamlitAPIException(
                    f"Unknown state ({state}). Must be one of 'running', 'complete', or 'error'."
                )
            self._current_state = state

        self._current_proto = msg.delta.add_block
        _enqueue_message(msg)

        # We currently only support writing to st._main, but this will change
        # when we settle on an improved API in a post-layout world.
        dg = _main
        element = Element()
        return_value = marshall_component(_markdown, dg, element, self._key, )
        dg._enqueue(
            "component_instance", element.component_instance, return_value
        )

    def __enter__(self) -> MarkdownContainer:  # type: ignore[override]
        # This is a little dubious: we're returning a different type than
        # our superclass' `__enter__` function. Maybe DeltaGenerator.__enter__
        # should always return `self`?
        super().__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        # Only update if the current state is running
        if self._current_state == "running":
            # We need to sleep here for a very short time to prevent issues when
            # the status is updated too quickly. If an .update() is directly followed
            # by the exit of the context manager, sometimes only the last update
            # (to complete) is applied. Adding a short timeout here allows the frontend
            # to render the update before.
            time.sleep(0.05)
            if exc_type is not None:
                # If an exception was raised in the context,
                # we want to update the status to error.
                self.update(state="error")
            else:
                self.update(state="complete")
        return super().__exit__(exc_type, exc_val, exc_tb)
