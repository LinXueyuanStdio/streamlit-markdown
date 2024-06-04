import os
import streamlit.components.v1 as components
from streamlit.runtime.scriptrunner import get_script_run_ctx
from typing import (
    List,
    Any,
    Dict,
    Optional,
    Union,
    Sequence,
    Callable,
    Tuple,
    TYPE_CHECKING,
)
from typing_extensions import Literal
from streamlit.runtime.uploaded_file_manager import UploadedFileRec
from streamlit import session_state
from typing import Optional

import re
from typing import Dict, Union, Sequence
from streamlit import util
import io
from typing import Optional
from dataclasses import dataclass
from streamlit.runtime.uploaded_file_manager import UploadedFileRec

from streamlit.runtime.memory_uploaded_file_manager import MemoryUploadedFileManager

class UploadedFile(io.BytesIO):
    """A mutable uploaded file.

    This class extends BytesIO, which has copy-on-write semantics when
    initialized with `bytes`.
    """

    def __init__(self, record: UploadedFileRec):
        # BytesIO's copy-on-write semantics doesn't seem to be mentioned in
        # the Python docs - possibly because it's a CPython-only optimization
        # and not guaranteed to be in other Python runtimes. But it's detailed
        # here: https://hg.python.org/cpython/rev/79a5fbe2c78f
        super().__init__(record.data)
        self.file_id = record.file_id
        self.name = record.name
        self.type = record.type
        self.size = len(record.data)
        # self._file_urls = file_urls

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UploadedFile):
            return NotImplemented
        return self.file_id == other.file_id

    def __repr__(self) -> str:
        return util.repr_(self)


@dataclass
class ChunkUploaderReturnValue:
    file_id: str
    file_name: str
    file_size: int
    file_type: str
    total_chunks: Optional[int] = None

    @staticmethod
    def from_component_value(conponent_value: dict):
        try:
            return ChunkUploaderReturnValue(
                **convert_keys_to_snake_case(conponent_value)
            )
        except:
            return None

def convert_keys_to_snake_case(data: Dict[str, any]) -> dict:
    """Convert dictionary keys to snake case

    Args:
        data (Dict[str, any]): dictionary

    Returns:
        dict: dictionary with snake case keys

    """
    return {
        re.sub("([a-z0-9])([A-Z])", r"\1_\2", key).lower(): value
        for key, value in data.items()
    }


def generate_accept_string(extensions: Union[str, Sequence[str], None]) -> str:
    """Generate accept string for file uploader

    Args:
        extensions (Union[str, Sequence[str], None]): extensions to accept

    Returns:
        str: accept string
    """

    if extensions is None:
        return "*.*"
    elif isinstance(extensions, str):
        # Check if it's a MIME type
        if "/" in extensions:
            return extensions
        extensions = [f".{extensions.strip().lstrip('.')}"]
    else:
        # If it's a sequence, handle each extension accordingly
        ext_list = []
        for ext_item in extensions:
            if isinstance(ext_item, str):
                # Check if it's a MIME type
                if "/" in ext_item:
                    ext_list.append(ext_item)
                else:
                    ext_list.append(f".{ext_item.strip().lstrip('.')}")
            else:
                raise TypeError("Each extension must be a string.")
        extensions = ext_list

    return ",".join([ext for ext in extensions])


def __get_files_from_file_storage(
    rv: ChunkUploaderReturnValue,
) -> Optional[UploadedFile]:
    if rv is None:
        return None
    # Do not proceed if there is no file id
    if rv.file_id is None:
        return None
    # Get the context
    ctx = get_script_run_ctx()
    session_id = ctx.session_id
    # Get the streamlit upload manager
    uploaded_file_mgr: "MemoryUploadedFileManager" = ctx.uploaded_file_mgr
    # Get the file data associated with the session_id
    file_storage: Dict[str, UploadedFileRec] = uploaded_file_mgr.file_storage.get(session_id, {})
    # In the case of multipart, the format will be {uuid}.{chunk_id}, so we need to retrieve it
    file_ids = [k for k in file_storage.keys() if k.startswith(rv.file_id)]
    if len(file_ids) > 1:
        # Raise an exception if the number of files doesn't match
        if rv.total_chunks != len(file_ids):
            raise Exception("Upload failed!!")
        sorted_file_ids = list(sorted(file_ids, key=lambda x: int(x.split(".")[1])))
        combined_bytes = b""
        for file_id in sorted_file_ids:
            record = uploaded_file_mgr.get_files(session_id, file_ids=[file_id])[0]
            combined_bytes += record.data
            uploaded_file_mgr.remove_file(session_id, file_id)
        if len(combined_bytes) != rv.file_size:
            raise Exception("File sizes do not match!!!")
        # Register
        combined_file = UploadedFileRec(
            rv.file_id, rv.file_name, rv.file_type, combined_bytes
        )
        uploaded_file_mgr.add_file(session_id, combined_file)
        del combined_bytes, combined_file
    # Get the file
    record = uploaded_file_mgr.get_files(session_id, [rv.file_id])[0]
    return UploadedFile(record)

def stream_markdown(
    richContent: bool = True,
    background_color: Literal["blue", "orange", "green"] = "green",
    on_change: Optional[Callable] = None,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    key=None,
):
    _CV_KEY = f"_{key}_cv"
    _CV_PREV_KEY = f"{_CV_KEY}_prev"

    ctx = get_script_run_ctx()
    session_id = ctx.session_id
    uploaded_file_mgr: MemoryUploadedFileManager = ctx.uploaded_file_mgr
    endpoint = uploaded_file_mgr.endpoint

    component_value = st_markdown(
        richContent,
        background_color,
        key=_CV_KEY,
        session_id=session_id,
        endpoint=endpoint,
    )
    rv = ChunkUploaderReturnValue.from_component_value(component_value)
    content = __get_files_from_file_storage(rv)
    # Get the previous state
    prev_cv: Optional[dict] = session_state.get(_CV_PREV_KEY)
    # Rewrite file and execute on_change if the state is different
    if prev_cv != component_value:
        session_state[key] = content
        session_state[_CV_PREV_KEY] = component_value
        if on_change is not None:
            on_change(
                *(args if args is not None else ()),
                **(kwargs if kwargs is not None else {}),
            )

    return content