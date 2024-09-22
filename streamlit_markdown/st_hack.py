from __future__ import annotations

from streamlit.elements.form import current_form_id
from streamlit.proto.Element_pb2 import Element
from streamlit.runtime.scriptrunner import get_script_run_ctx, ScriptRunContext
from streamlit.runtime.state import NoValue, register_widget
from streamlit.runtime.state.widgets import ElementType, ELEMENT_TYPE_TO_VALUE_TYPE
from streamlit.runtime.state.common import compute_widget_id
from streamlit.delta_generator import DeltaGenerator
from streamlit.components.v1.custom_component import (
    CustomComponent,
    MarshallComponentException,
)

from streamlit.runtime.state.common import (
    RegisterWidgetResult,
    T,
    WidgetArgs,
    WidgetCallback,
    WidgetDeserializer,
    WidgetKwargs,
    WidgetMetadata,
    WidgetProto,
    WidgetSerializer,
    user_key_from_widget_id,
)
from typing import *
import json


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


def marshall_component(
    self: CustomComponent,
    dg: DeltaGenerator,
    element: Element,
    key,
    default,
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

    def deserialize_component(ui_value, widget_id=""):
        # ui_value is an object from json, an ArrowTable proto, or a bytearray
        return ui_value

    component_state = register_widget(
        element_type="component_instance",
        element_proto=element.component_instance,
        user_key=key,
        widget_func_name=self.name,
        deserializer=deserialize_component,
        serializer=lambda x: x,
        ctx=ctx,
    )
    widget_value = component_state.value

    if key is not None:
        marshall_element_args()

    if widget_value is None:
        widget_value = default

    # widget_value will be either None or whatever the component's most
    # recent setWidgetValue value is. We coerce None -> NoValue,
    # because that's what DeltaGenerator._enqueue expects.
    value = widget_value if widget_value is not None else NoValue
    return element.component_instance, value


def register_widget(
    element_type: ElementType,
    element_proto: WidgetProto,
    deserializer: WidgetDeserializer[T],
    serializer: WidgetSerializer[T],
    ctx: ScriptRunContext | None,
    user_key: str | None = None,
    widget_func_name: str | None = None,
    on_change_handler: WidgetCallback | None = None,
    args: WidgetArgs | None = None,
    kwargs: WidgetKwargs | None = None,
) -> RegisterWidgetResult[T]:
    metadata = WidgetMetadata(
        element_proto.id,
        deserializer,
        serializer,
        value_type=ELEMENT_TYPE_TO_VALUE_TYPE[element_type],
        callback=on_change_handler,
        callback_args=args,
        callback_kwargs=kwargs,
        fragment_id=ctx.current_fragment_id if ctx else None,
    )
    return register_widget_from_metadata(metadata, ctx, widget_func_name, element_type)


def register_widget_from_metadata(
    metadata: WidgetMetadata[T],
    ctx: ScriptRunContext | None,
    widget_func_name: str | None,
    element_type: ElementType,
) -> RegisterWidgetResult[T]:
    """Register a widget and return its value, using an already constructed
    `WidgetMetadata`.

    This is split out from `register_widget` to allow caching code to replay
    widgets by saving and reusing the completed metadata.

    See `register_widget` for details on what this returns.
    """
    # Local import to avoid import cycle
    import streamlit.runtime.caching as caching

    if ctx is None:
        # Early-out if we don't have a script run context (which probably means
        # we're running as a "bare" Python script, and not via `streamlit run`).
        return RegisterWidgetResult.failure(deserializer=metadata.deserializer)

    widget_id = metadata.id
    user_key = user_key_from_widget_id(widget_id)

    # Ensure another widget with the same user key hasn't already been registered.
    if user_key is not None:
        if user_key not in ctx.widget_user_keys_this_run:
            ctx.widget_user_keys_this_run.add(user_key)

    # Ensure another widget with the same id hasn't already been registered.
    new_widget = widget_id not in ctx.widget_ids_this_run
    if new_widget:
        ctx.widget_ids_this_run.add(widget_id)

    # Save the widget metadata for cached result replay
    if hasattr(caching, "save_widget_metadata"):
        caching.save_widget_metadata(metadata)
    return ctx.session_state.register_widget(metadata, user_key)
