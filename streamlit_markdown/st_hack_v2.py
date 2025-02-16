from __future__ import annotations

from streamlit.elements.form import current_form_id
from streamlit.proto.Element_pb2 import Element
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.state import register_widget
from streamlit.elements.lib.utils import compute_and_register_element_id, _compute_element_id
from streamlit.delta_generator import DeltaGenerator

import streamlit.components.v1 as v1
if hasattr(v1, "custom_component"):
    from streamlit.components.v1.custom_component import CustomComponent, MarshallComponentException
else:
    from streamlit.components.v1.components import CustomComponent, MarshallComponentException

from streamlit.runtime.scriptrunner_utils.script_run_context import ScriptRunContext
from streamlit.runtime.state.common import (
    WidgetCallback,
    user_key_from_element_id,
)
from typing import *
import json


def marshall_component(
    self: CustomComponent,
    dg: DeltaGenerator,
    element: Element,
    key,
    default,
    on_change: WidgetCallback | None = None,
    **kwargs,
):
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
        computed_id = compute_and_register_element_id(
            "component_instance",
            user_key=key,
            form_id=current_form_id(dg),
            name=self.name,
            url=self.url,
            json_args=serialized_json_args,
            special_args=special_args,
        )
    else:
        computed_id = compute_and_register_element_id(
            "component_instance",
            user_key=key,
            form_id=current_form_id(dg),
            name=self.name,
            url=self.url,
        )

    element.component_instance.id = computed_id

    def deserialize_component(ui_value, widget_id=""):
        # ui_value is an object from json, an ArrowTable proto, or a bytearray
        return ui_value

    component_state = register_widget(
        element.component_instance.id,
        deserializer=deserialize_component,
        serializer=lambda x: x,
        ctx=ctx,
        on_change_handler=on_change,
        value_type="json_value",
    )
    widget_value = component_state.value

    if key is not None:
        marshall_element_args()

    if widget_value is None:
        widget_value = default

    # widget_value will be either None or whatever the component's most
    # recent setWidgetValue value is. We coerce None -> NoValue,
    # because that's what DeltaGenerator._enqueue expects.
    value = widget_value
    return element.component_instance, value


def compute_and_register_element_id(
    element_type: str,
    *,
    user_key: str | None,
    form_id: str | None,
    **kwargs: SAFE_VALUES | Iterable[SAFE_VALUES],
) -> str:
    """Compute and register the ID for the given element.

    This ID is stable: a given set of inputs to this function will always produce
    the same ID output. Only stable, deterministic values should be used to compute
    element IDs. Using nondeterministic values as inputs can cause the resulting
    element ID to change between runs.

    The element ID includes the user_key so elements with identical arguments can
    use it to be distinct. The element ID includes an easily identified prefix, and the
    user_key as a suffix, to make it easy to identify it and know if a key maps to it.

    The element ID gets registered to make sure that only one ID and user-specified
    key exists at the same time. If there are duplicated IDs or keys, an error
    is raised.

    Parameters
    ----------
    element_type : str
        The type (command name) of the element to register.

    user_key : str | None
        The user-specified key for the element. `None` if no key is provided
        or if the element doesn't support a specifying a key.

    form_id : str | None
        The ID of the form that the element belongs to. `None` or empty string
        if the element doesn't belong to a form or doesn't support forms.

    kwargs : SAFE_VALUES | Iterable[SAFE_VALUES]
        The arguments to use to compute the element ID.
        The arguments must be stable, deterministic values.
        Some common parameters like key, disabled,
        format_func, label_visibility, args, kwargs, on_change, and
        the active_script_hash are not supposed to be added here
    """
    ctx = get_script_run_ctx()

    # If form_id is provided, add it to the kwargs.
    kwargs_to_use = {"form_id": form_id, **kwargs} if form_id else kwargs

    if ctx:
        # Add the active script hash to give elements on different
        # pages unique IDs.
        kwargs_to_use["active_script_hash"] = ctx.active_script_hash

    element_id = _compute_element_id(
        element_type,
        user_key,
        **kwargs_to_use,
    )

    if ctx:
        _register_element_id(ctx, element_type, element_id)
    return element_id


def _register_element_id(
    ctx: ScriptRunContext, element_type: str, element_id: str
) -> None:

    if not element_id:
        return

    if user_key := user_key_from_element_id(element_id):
        if user_key not in ctx.widget_user_keys_this_run:
            ctx.widget_user_keys_this_run.add(user_key)
        # else:
        #     raise StreamlitDuplicateElementKey(user_key)

    if element_id not in ctx.widget_ids_this_run:
        ctx.widget_ids_this_run.add(element_id)
    # else:
    #     raise StreamlitDuplicateElementId(element_type)
