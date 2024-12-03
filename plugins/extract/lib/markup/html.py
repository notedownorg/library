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

import mdformat, requests 
from typing import Optional
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer
from bs4 import BeautifulSoup

def extract_article(url: str) -> bytes:
    docs = AsyncHtmlLoader([url]).load()
    md = MarkdownifyTransformer()
    converted = md.transform_documents(docs)
    formatted = mdformat.text(converted[0].page_content)
    return formatted.encode("utf-8")

def get_webpage_title(url: str) -> Optional[str]:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.title:
        return soup.title.string
    return None
