# Copyright 2024 Notedown Authors
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

import tempfile
from typing import Callable, Optional
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import YoutubeAudioLoader
from langchain_community.document_loaders.parsers.audio import (OpenAIWhisperParserLocal)
from lib.transcribing.models import SpeechToTextModels

class VideoTranscriber():
    def __init__(self, model: SpeechToTextModels):
        self.model = model

    def extract_video_transcription(self, url: str, splitter: Optional[Callable[[bytes], bytes]]) -> Optional[bytes]:
        transcription = None
        if "youtube.com" in url or "youtu.be" in url:
            transcription = self._extract_youtube_transcription(url)

        if transcription is None:
            return None

        if splitter is None:
            return transcription

        return splitter(transcription)


    def _extract_youtube_transcription(self, url: str) -> bytes:
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = GenericLoader(
                YoutubeAudioLoader([url], tmpdir),
                OpenAIWhisperParserLocal(lang_model=self.model)
            )
            return loader.load()[0].page_content.encode("utf-8")


