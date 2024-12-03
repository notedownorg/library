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

import grpc, sys, time, json, logging
from pathlib import Path
from concurrent import futures
from typing import Dict
from lib.transcribing.video import VideoTranscriber
from lib.transcribing.splitting import sat
from lib.transcribing import models
from lib.markup.html import extract_article
from .grpc.extract_pb2_grpc import ExtractServicer, add_ExtractServicer_to_server
from .grpc.extract_pb2 import ExtractRequest, ExtractResponse, EmbeddingsModel, SpeechToTextModel

logging.basicConfig(
    level=logging.DEBUG,
    filename=f"{Path.home()}/.notedown/logs/library-plugin-extractor.log",
)

stt_map: Dict[SpeechToTextModel, models.SpeechToTextModels]  = {
    SpeechToTextModel.OPENAI_WHISPER_LARGE_V3: "openai/whisper-large-v3",
}

embed_map: Dict[EmbeddingsModel, models.EmbeddingModels] = {
    EmbeddingsModel.NVIDIA_EMBED_V2: "nvidia/NV-Embed-v2",
}

class ExtractService(ExtractServicer):
    def __init__(self):
        pass

    def Extract(self, request: ExtractRequest, context: grpc.ServicerContext) -> ExtractResponse:
        if request.video:
            transcriber = VideoTranscriber(stt_map[request.video.speech_to_text_model])
            transcription = transcriber.extract_video_transcription(
                request.video.url,
                sat(),
            )
            if transcription is None:
                context.abort(grpc.StatusCode.INTERNAL, "unable to process transcription")
            return ExtractResponse(content=transcription)

        if request.article:
            content = extract_article(request.article.url)
            if content is None:
                context.abort(grpc.StatusCode.INTERNAL, "unable to process article")
            return ExtractResponse(content=content)

        context.abort(grpc.StatusCode.UNIMPLEMENTED, "unrecognized request type")
        return ExtractResponse(content=b"") # wont be reached, here for types
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ExtractServicer_to_server(ExtractService(), server)
    port = server.add_insecure_port('127.0.0.1:0')
    server.start()
    
    print(json.dumps({"address": f"127.0.0.1:{port}"}), end="\n") 

    sys.stdout.flush()

    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
