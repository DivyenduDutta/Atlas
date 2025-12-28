from atlas.utils.logger import LoggerConfig
from atlas.core.chunker.base_chunker import BaseChunker
from atlas.utils.chunker_utils import slugify

import re
from pathlib import Path
from typing import List, Dict
import json

LOGGER = LoggerConfig().logger


class StructuralChunker(BaseChunker):
    """
    Chunker that splits notes based on their structural elements like headings.
    See comments in `create_chunks` method for detailed chunking strategy.

    Args:
        processed_data_path (str): Path to the processed data file (obsidian indexed data).
        output_path (str): Path to save the chunked data.
        max_words (int): Maximum number of words allowed in a single chunk.
    """

    def __init__(
        self, processed_data_path: str, output_path: str, max_words: int
    ) -> None:
        LOGGER.info("-" * 20)
        LOGGER.info("StructuralChunker initialized.")
        LOGGER.info(f"Chunking processed data at {processed_data_path}")
        self.processed_data_path = Path(processed_data_path)
        self.output_path = Path(output_path)
        self.max_words = max_words

    def read_processed_data(self) -> List[Dict] | None:
        """
        Read the obsidian indexed data which is the output of the previous module
        ie, `ObsidianVaultProcessor`.

        Returns:
            List[Dict] | None: The obsidian indexed data as a list of dictionaries or None if an error occurs.
        """

        try:
            with open(self.processed_data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            LOGGER.info("Obsidian indexed data successfully read.")
            return data
        except Exception as e:
            LOGGER.error(f"Error reading processed data: {e}")
            return None

    def _split_by_word_limit(self, text: str, max_words: int) -> list[str]:
        """
        Split text into chunks based on a maximum word limit.
        Simple and deterministic splitting by spaces.

        Args:
            text (str): The text to be split.
            max_words (int): The maximum number of words per chunk.

        Returns:
            list[str]: A list of text chunks.
        """
        words = text.split()
        chunks = []

        for i in range(0, len(words), max_words):
            chunk_words = words[i : i + max_words]
            chunks.append(" ".join(chunk_words))

        return chunks

    def _split_by_headings(self, text: str) -> List[Dict]:
        """
        Split text into sections based on markdown headings.
        Args:
            text (str): The text to be split.

        Returns:
            List[Dict]: A list of sections with headings and text.

            Returns list of:
            {
                "heading": str | None,
                "text": str
            }
        """
        sections = []
        current_heading = None
        buffer: List[str] = []

        for line in text.splitlines():
            match = re.match(r"^(#{1,6})\s+(.*)", line)
            if match:
                # save previous section
                if buffer:
                    sections.append(
                        {"heading": current_heading, "text": "\n".join(buffer).strip()}
                    )
                    buffer = []

                current_heading = match.group(2).strip()
            else:
                buffer.append(line)

        # last section
        if buffer:
            sections.append(
                {"heading": current_heading, "text": "\n".join(buffer).strip()}
            )

        return sections

    def _make_chunk(
        self, note: Dict, text: str, heading: str | None, chunk_index: int
    ) -> Dict:
        """
        Create a chunk dictionary.

        Args:
            note (Dict): The original note dictionary.
            text (str): The chunk text.
            heading (str | None): The heading of the section.
            chunk_index (int): The index of the chunk within the note.

        Returns:
            Dict: The chunk dictionary.
        """
        section_id = slugify(heading) if heading else "root"

        return {
            "chunk_id": f"{note['note_id']}::{section_id}::chunk_{chunk_index}",
            "note_id": note["note_id"],
            "title": note["title"],
            "relative_path": note["relative_path"],
            "heading": heading,
            "chunk_index": chunk_index,
            "text": text,
            "word_count": len(text.split()),
            "tags": note.get("tags", []),
            "frontmatter": note.get("frontmatter", {}),
        }

    def create_chunks(self, processed_data: List[Dict]) -> List[Dict]:
        """
        Create chunks from processed data based on strucutural chunking strategy.

        Args:
            processed_data (List[Dict]): The processed data to be chunked.

        Returns:
            List[Dict]: The chunked data.
        """
        chunks = []

        for note in processed_data:
            text = note["raw_text"].strip()
            word_count = note["word_count"]

            # -------- Rule 1 --------
            # if word count <= max_words, create single chunk from whole note
            if word_count <= self.max_words:
                chunks.append(self._make_chunk(note, text, heading=None, chunk_index=0))
                continue

            # -------- Rule 2 --------
            # if note has headings, split by headings first
            if note["headings"]:
                sections = self._split_by_headings(text)
                chunk_idx = 0

                for section in sections:
                    section_text = section["text"]
                    section_words = len(section_text.split())

                    # -------- Rule 3 --------
                    # if section > max_words, split by word limit into inidividual chunks
                    if section_words > self.max_words:
                        sub_chunks = self._split_by_word_limit(
                            section_text, self.max_words
                        )
                        for sub_text in sub_chunks:
                            chunks.append(
                                self._make_chunk(
                                    note,
                                    sub_text,
                                    heading=section["heading"],
                                    chunk_index=chunk_idx,
                                )
                            )
                            chunk_idx += 1
                    else:
                        # if section <= max_words, create single chunk from section
                        chunks.append(
                            self._make_chunk(
                                note,
                                section_text,
                                heading=section["heading"],
                                chunk_index=chunk_idx,
                            )
                        )
                        chunk_idx += 1

                continue

            # -------- Rule 4 --------
            # if note has no headings and word count > max_words, split by word limit
            sub_chunks = self._split_by_word_limit(text, self.max_words)
            for idx, sub_text in enumerate(sub_chunks):
                chunks.append(
                    self._make_chunk(note, sub_text, heading=None, chunk_index=idx)
                )

        return chunks

    def save_chunked_data(self, chunked_data: List[Dict]) -> None:
        """
        Save the chunked data to the output path in JSON format.
        This method writes to a temporary file first and then renames it to ensure atomicity.
        This prevents data corruption in case of interruptions during the write process.

        Args:
            chunked_data (List[Dict]): The chunked data to be saved.
        """
        tmp_path = self.output_path.with_suffix(".tmp")

        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(chunked_data, f, indent=2, ensure_ascii=False)

        tmp_path.replace(self.output_path)


if __name__ == "__main__":
    processed_data_path = r"D:\\Deep learning\\Atlas\\Resources\\obsidian_index.json"
    output_path = r"D:\\Deep learning\\Atlas\\Resources\\chunked_data.json"

    # 250 words per chunk because as a rule of thumb, 1 token ~= 0.75 words
    # so 250 words ~= 333 tokens which is a good size for LLM context windows
    # Also we need to have space for 2 - 3 chunks in the prompt along with other prompt text
    # TinyLLama-1.1B-Chat has a context window of 2048 tokens
    # souce - https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0/discussions/9
    max_words = 250  # increase this value to have larger chunks
    chunker = StructuralChunker(processed_data_path, output_path, max_words)
    chunker.chunk()
