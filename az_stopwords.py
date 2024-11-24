"""
Azerbaijani Stop Words Remover
"""

import re
from pathlib import Path
from typing import List, Set, Union, Optional
import logging
from dataclasses import dataclass
import unicodedata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WordInfo:
    """Stores information about a word including its original case."""
    original: str
    spaces_before: str
    spaces_after: str


class AzerbaijaniStopWordsRemover:
    """A class for removing Azerbaijani stop words from text while preserving structure and case."""

    DEFAULT_STOPWORDS_PATH = Path(__file__).parent / "az_stopwords.txt"

    def __init__(
            self,
            stop_words_path: Optional[Union[str, Path]] = None,
            case_sensitive: bool = False,
            preserve_structure: bool = True
    ):
        self.case_sensitive = case_sensitive
        self.preserve_structure = preserve_structure
        self.stop_words = self._load_stop_words(stop_words_path)

    def _load_stop_words(self, path: Optional[Union[str, Path]] = None) -> Set[str]:
        """Load stop words from file."""
        try:
            file_path = Path(path) if path else self.DEFAULT_STOPWORDS_PATH
            with open(file_path, 'r', encoding='utf-8') as f:
                stop_words = {line.strip() for line in f if line.strip()}
            logger.info(f"Loaded {len(stop_words)} stop words")
            return stop_words
        except Exception as e:
            logger.error(f"Error loading stop words: {e}")
            raise

    def _normalize_text(self, text: str) -> str:
        """Normalize Unicode characters in text."""
        return unicodedata.normalize('NFKC', text)

    def _process_sentence(self, sentence: str) -> str:
        """Process a single sentence while preserving punctuation, spacing and case."""
        if not sentence.strip():
            return sentence

        leading_space = re.match(r'^(\s*)', sentence).group(1)
        trailing_space = re.search(r'(\s*)$', sentence).group(1)

        pattern = r'(\s*)(\b\w+\b|\W+)(\s*)'
        matches = re.finditer(pattern, sentence.strip())

        result_parts = []
        for match in matches:
            spaces_before, word, spaces_after = match.groups()

            if not word.isalnum():
                result_parts.append(spaces_before + word + spaces_after)
                continue

            check_word = word if self.case_sensitive else word.lower()
            if check_word not in self.stop_words:
                result_parts.append(spaces_before + word + spaces_after)

        processed_text = ''.join(result_parts)
        return leading_space + processed_text + trailing_space

    def remove_stop_words(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        """Remove stop words from text while preserving structure and case."""
        if isinstance(text, list):
            return [self.remove_stop_words(t) for t in text]

        if not isinstance(text, str):
            raise TypeError("Input must be string or list of strings")

        text = self._normalize_text(text)

        sentences = re.split(r'(\n+)', text)

        processed_sentences = [
            self._process_sentence(sentence) if not re.match(r'^\n+$', sentence)
            else sentence
            for sentence in sentences
        ]

        return ''.join(processed_sentences)

    def remove_stop_words_from_file(
            self,
            input_path: Union[str, Path],
            output_path: Union[str, Path]
    ) -> None:
        """Remove stop words from a text file."""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()

            processed_text = self.remove_stop_words(text)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)

            logger.info(f"Processed text saved to {output_path}")
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            raise