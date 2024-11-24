# Azerbaijani Stop Words Remover

A Python module for removing Azerbaijani stop words while preserving text structure and formatting.

## Features

- Remove Azerbaijani stop words from text
- Preserve original text structure and formatting
- Maintain original case of words
- Support for custom stop words lists
- Handle both single strings and lists of strings
- Process text files directly

## Quick Start

```python
from az_stopwords import AzerbaijaniStopWordsRemover

# Initialize the remover
remover = AzerbaijaniStopWordsRemover()

# Remove stop words from text
text = "Bu mətn sadəcə olaraq nümunədir"
result = remover.remove_stop_words(text)
print(result)  # Output: "mətn nümunədir"
```

## Advanced Usage

### Custom Stop Words

```python
remover = AzerbaijaniStopWordsRemover(
    stop_words_path='custom_stopwords.txt',
    case_sensitive=True
)
```

### Process File

```python
remover.remove_stop_words_from_file(
    'input.txt',
    'output.txt'
)
```

### Process Multiple Texts

```python
texts = [
    "Mən müsiqi dinləməyi çox çox sevirəm.",
    "Əslində mən bu kitabı çoxdan oxumuşam"
]
results = remover.remove_stop_words(texts)
```

## API Reference

### AzerbaijaniStopWordsRemover

#### Parameters

- `stop_words_path` (Optional[str]): Path to custom stop words file
- `case_sensitive` (bool): Whether to perform case-sensitive removal
- `preserve_structure` (bool): Whether to preserve text structure

#### Methods

- `remove_stop_words(text: Union[str, List[str]]) -> Union[str, List[str]]`
- `remove_stop_words_from_file(input_path: str, output_path: str) -> None`



## License

This project is licensed under the MIT License.

## Author

LocalDoc - [v.resad.89@gmail.com](mailto:v.resad.89@gmail.com)
