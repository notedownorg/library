from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmbeddingsModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NVIDIA_EMBED_V2: _ClassVar[EmbeddingsModel]

class SpeechToTextModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPENAI_WHISPER_LARGE_V3: _ClassVar[SpeechToTextModel]

class Format(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ARTICLE: _ClassVar[Format]
    VIDEO: _ClassVar[Format]
    PODCAST: _ClassVar[Format]
    BOOK: _ClassVar[Format]
    COURSE: _ClassVar[Format]
NVIDIA_EMBED_V2: EmbeddingsModel
OPENAI_WHISPER_LARGE_V3: SpeechToTextModel
ARTICLE: Format
VIDEO: Format
PODCAST: Format
BOOK: Format
COURSE: Format

class ExtractArticleRequest(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class ExtractVideoRequest(_message.Message):
    __slots__ = ("url", "speech_to_text_model")
    URL_FIELD_NUMBER: _ClassVar[int]
    SPEECH_TO_TEXT_MODEL_FIELD_NUMBER: _ClassVar[int]
    url: str
    speech_to_text_model: SpeechToTextModel
    def __init__(self, url: _Optional[str] = ..., speech_to_text_model: _Optional[_Union[SpeechToTextModel, str]] = ...) -> None: ...

class ExtractRequest(_message.Message):
    __slots__ = ("article", "video")
    ARTICLE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    article: ExtractArticleRequest
    video: ExtractVideoRequest
    def __init__(self, article: _Optional[_Union[ExtractArticleRequest, _Mapping]] = ..., video: _Optional[_Union[ExtractVideoRequest, _Mapping]] = ...) -> None: ...

class ExtractResponse(_message.Message):
    __slots__ = ("title", "format", "content")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    title: str
    format: Format
    content: bytes
    def __init__(self, title: _Optional[str] = ..., format: _Optional[_Union[Format, str]] = ..., content: _Optional[bytes] = ...) -> None: ...
