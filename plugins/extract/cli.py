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

from typing import Optional
from lib.transcribing import models
from lib.transcribing.splitting import sat
from lib.transcribing.video import VideoTranscriber
from lib.markup.html import extract_article

def video(stt_model: models.SpeechToTextModels, url: str) -> Optional[bytes]:
    return VideoTranscriber(stt_model).extract_video_transcription(url, sat())

def article(url: str) -> Optional[bytes]:
    return extract_article(url)

def run():
    content = video("openai/whisper-large-v3", "https://youtu.be/KuLUd1UIvVA")
    # content = article("https://brooker.co.za/blog/2024/08/14/gc-metastable.html")
    if content:
        print(content.decode("utf-8"))
    else:
        print("unable to process video")

