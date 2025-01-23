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

from typing import Callable
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.splitters import RollingWindowSplitter
from lib.transcribing.models import EmbeddingModels
from wtpsplit import SaT
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_huggingface.embeddings.huggingface import HuggingFaceEmbeddings

# Transcripts produce one long string, so we need to split it into paragraphs based on semantic meaning

# @deprecated, use sat instead.
# TODO: Agentic splitting? https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb
def semantic_split(model: EmbeddingModels) -> Callable[[bytes], bytes]:
    def split(text: bytes) -> bytes:
        # TODO: Fix pure langchain implementation
        # hf = HuggingFaceEmbeddings(
        #     model_name="nvidia/NV-Embed-v2",
        #     model_kwargs={"trust_remote_code": True},
        #     # model_kwargs={"max_seq_length": 32768},
        #     # tokenizer_kwargs={"padding_side": "right"},
        # )
        # splitter = SemanticChunker(
        #         hf,
        #         # HuggingFaceEmbeddings(
        #         #     model_name="nvidia/NV-Embed-v2",
        #         #     model_kwargs={"trust_remote_code": True},
        #         #     # model_kwargs={"max_seq_length": 32768},
        #         #     tokenizer_kwargs={"padding_side": "right"},
        #         # ),
        #         # chunks are very likely to be highly correlated so we use gradient threshold
        #         breakpoint_threshold_type="gradient",
        # )
        # chunks = splitter.split_text(text)
        # for chunk in chunks:
        #     print(chunk)
        encoder = HuggingFaceEncoder()
        encoder.name = model
        encoder.model_kwargs = {"max_seq_length": 32768}
        encoder.tokenizer_kwargs = {"padding_side": "right"}
        splitter = RollingWindowSplitter(
            encoder=encoder,
            dynamic_threshold=True,
            min_split_tokens=100,
            max_split_tokens=500,
            window_size=5,
            # plot_splits=True,  # set this to true to visualize chunking
            # enable_statistics=True  # to print chunking stats
        )
        paragraphs = []
        for split in splitter([text.decode("utf-8")]):
            paragraphs.append(' '.join(split.docs))
        return '\n\n'.join(paragraphs).encode("utf-8")
    return split

def sat() -> Callable[[bytes], bytes]:
    def split(text: bytes) -> bytes:
        sat = SaT("sat-12l-sm")
        paragraphs = []
        for paragraph in sat.split(text.decode("utf-8"), do_paragraph_segmentation=True):
            paragraphs.append(''.join(paragraph))
        return '\n\n'.join(paragraphs).encode("utf-8")
    return split

    

    
