# Library

`library` is a command-line tool for extracting the content of different formats from the web and storing them as Markdown. It is designed to be used as part of a Notedown workspace but commands can be overidden to work in many different setups.

## How does it work?

Library works differently depending on the format being extracted. 

For text-based sources it leverages [Markdownify](https://github.com/matthewwithanm/python-markdownify) for deterministic results.

For audio and video sources it leverages local AI models, specifically [OpenAI's `whisper-large-v3-turbo`](https://huggingface.co/openai/whisper-large-v3-turbo) to transcribe and then [Segment Any Text `sat-12l-sm`](https://huggingface.co/segment-any-text/sat-12l-sm) to chunk the result into a best effort attempt of paragraphs. As these models are relatively small this should work on most modern machines. If you are having problems please raise an issue!

## Supported Sources

If you would like support added for additional formats/sources please create a discussion thread!

| Format | Source | Link Type |
| ------ | ------ | ---- |
| Text | Any | Any HTML should work (https://daringfireball.net/projects/markdown/) |
| Video | YouTube | Any YouTube video link (e.g. https://youtu.be/TQn2hJeHQbM?si=h6daSXm1le5opihU) |


## Usage outside of Notedown

The `extract` command extracts Markdown from sources and output them to stdout.

```sh
library extract https://daringfireball.net/projects/markdown/
```

## Usage with Notedown

The `add` command creates a new Markdown file in your selected Notedown workspace with the required metadata. If your url contains special characters e.g. `?` you need to put it in quotes.

```sh
library add 'https://youtu.be/TQn2hJeHQbM?si=h6daSXm1le5opihU'
2025/01/23 04:07:35 INFO detected YouTube video url="https://youtu.be/TQn2hJeHQbM?si=h6daSXm1le5opihU"
2025/01/23 04:08:13 INFO Added new source title="Advent of Neovim: Why Neovim? - YouTube" format=video url="https://youtu.be/TQn2hJeHQbM?si=h6daSXm1le5opihU"
```

Then the `process` command scans the workspace for any unprocessed entries and appends the content to the entry.

```sh 
library process
Entry some_note.md already has already been processed, skipping.
Entry new_note.md has no content, extracting.
```

The `process` command can also be used to override an existing extraction. You might want to do this in the scenario where library adds support for a new model. If you have made any additional notes in the file this will override them.

```sh
library process --force some_note.md
Entry new_note.md has be re-processed.
```

## Configuration

Library uses per-workspace configuration located at `${WORKSPACE_ROOT}/.config/library.yaml`. If there is no configuration present the default configuration will be created at this location.

### Default directory

The default directory is the location new notes will be added into your workspace. The default value is `library/`.

```yaml
default_directory: library
```




