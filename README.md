# Atlas

<div align="center">
  <img src="atlas_icon.png" alt="atlas" width="575" height="337">

  <p><em>Atlas is a RAG-based knowledge copilot for Obsidian markdown vaults. It performs chunking, vector search, and grounded LLM responses with citation to original notes.</em></p>

  <p>
    <a href="https://github.com/DivyenduDutta/Atlas/blob/master/LICENSE"><img src="https://img.shields.io/github/license/DivyenduDutta/Atlas?style=flat-square" alt="License"></a>
    <a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black"></a>
  </p>

![CI](https://github.com/DivyenduDutta/Atlas/actions/workflows/ci.yaml/badge.svg)
[![codecov](https://codecov.io/gh/DivyenduDutta/Atlas/branch/master/graph/badge.svg)](https://codecov.io/gh/DivyenduDutta/Atlas)

  <p>
    <a href="#introduction">Introduction</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#setup">Setup</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#results">Results</a>
  </p>
</div>

## Introduction

#### Knowledge Copilot

As a famous LLM once said.
> A knowledge copilot is an AI assistant that understands your knowledge base and helps you query, synthesize, and navigate it—while staying faithful to the original sources.

A good knowledge copilot can search semantically, answer with context, connect ideas, cite sources and assist, not replace thinking. Its basically a "copilot" for our brains.

A good knowledge copilot is built using RAG (Retrieval-Augmented Generation). And what is that?

#### RAG

RAG or Retrieval Augmented Generation is a technique used to retrieve external knowledge (as context) and feed it into the model when prompted with a query. When an LLM is trained on generic data to perform next token prediction, it might be good at that task but would not be able to answer specific questions such as based on our knowledge sources. Hence RAG ensures that we dont just rely on the model's weights but "augment" it using our knowledge base to answer questions related to our knowledge base.

RAG is good because:
- Reduces hallucinations

- Enables citations

- Keeps answers faithful to source material

#### Chunking

[Chunker Module](atlas/core/chunker/README.md)

#### Embedding and Indexing

[Embedding Module](atlas/core/embedder/README.md)

#### Obsidian

[Obsidian](https://obsidian.md/) is a light weight application used to take notes and create knowledge bases. It saves all the notes as markdown making it easy to load, process and render a huge amount of notes.

- **Obsidian Frontmatter**
  - Obsidian Frontmatter (YAML) is metadata at the top of a note, enclosed in ---, used for organizing data like aliases, tags, type, status, and links, enabling powerful filtering, display, and automation with core features.
  - It provides key-value pairs for structured data, improving note management.

#### Problem Statement and Motivation

Imagine you're like me and spend a lot of time taking notes about various things in your life. I mean everything. Cooking, learning, grocery shopping, books read etc. I do that but increasingly realized that I dont quite often go back and utilize the knowledge in those notes. This is precisely because the knowledge is scattered and not structured. But with the help of a RAG based knowledge copilot, this knowledge generation can be offloaded to them and then we can interact with our knowledge base using natural language via an LLM.

So this repo is a RAG based knowledge copilot that operates on an Obsidian vault. So basically if you have a bunch of notes, you now have a natural language powered AI assistant who can answer your questions based off your notes.

The scope right now (ie, initially) would be to perform note summarization and answer questions based on note(s) reasoning.

#### LLM Choice

[TinyLlama](https://github.com/jzhang38/TinyLlama) was decided to be used. Its an interesting model because
- its pretrained from scratch
- has a tiny parameter budget (1.1 B) and hence its lightweight enough for our purposes
- pretrained on a massive dataset (3T tokens)
- we use the [chat model](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)

So it follows the scaling law that even a small LLM when trained on enough quality data leads to competetive performance.

## Architecture

Initial high level [architecture diagram](https://github.com/DivyenduDutta/Atlas/tree/master/Resources/Atlas_Architecture.png)

A sample of the `obsidian_index.json` is as below:

```json
[
  {
    "note_id": "folder/sample note.md",
    "title": "sample note",
    "relative_path": "folder/sample note.md",
    "raw_text": "note body. Lorem Ipsum",
    "frontmatter": {"tags": ["personal", "health"], "date": "2023-10-01"},
    "headings": ["Heading 1", "Heading 2"],
    "tags": ["tag1", "tag2"],
    "wikilinks": ["wikilink|custom name"],
    "word_count": 127
  },
...
]
```
Its a list of dictionaries, where each dictionary represents one note from the obsidian vault.

## Setup

Add the project root ie, Folder containing this README to PYTHONPATH whichever way you want. One way would be to create a .env and write the following in it
```
PYTHONPATH=\full\path\to\projectroot
```
And place this .env file in the project root. Works for VS Code.

Another option would be to run `$env:PYTHONPATH = \full\path\to\projectroot` in powershell to set the env variable and then run the scripts.

Install pytorch, torchvision via `pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu118` - Conda doesnt install GPU version on Windows.

### Sanity

Before committing changes run `pre-commit run --all-files` or `pre-commit run --file <file1>, <file2> ...`

## Quick Start

### Obsidian Vault Processor Module

Run `python .\atlas\core\ingest\obsidian_vault_processor.py`

This will generate the `obsidian_index.json` in `/Resources` folder. This json file contains the processed data after ingesting and processing the notes from the obsidian vault.

See architecture section for structure of this json.

### Structural Chunker Module

Run `python .\atlas\core\chunker\structural_chunker.py`

This will generate the `chunked_data.json` in `/Resources` folder. This json file contains the chunks generated from the notes processed by the "Obsidian Vault Processor" module.

See `README` in `atlas/core/chunker` for structure of this json.

There is an option to set the `max_words` for `StructuralChunker`. This determines the size of chunks created and should be changed primarily based on the token limit of the encoding model and context size of the LLM used in later modules.

### Embedding

Run `python .\atlas\core\embedder\sentence_transformer\impl_embedder.py`

This will generate the `embedded_chunks.json` in `/Resources` folder. This json is exactly similar to
`chunked_data.json` with the added `embedding` for each chunk.

See `README` in `atlas/core/embedder` for structure of this json.

See `altas/core/configs/sentence_transformer_config.yaml` for changing the encoder model used and its configuration. The following can be changed:

```yaml
model_name: sentence-transformers/all-MiniLM-L6-v2
batch_size: 32
normalize_embeddings: true
device: cuda
```

### Tests

Run unit tests via VS Code or `python -m unittest` to run all unit tests
