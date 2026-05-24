from abc import ABC, abstractmethod

from pydantic import BaseModel

from babel_poc.constants import DEFAULT_PUNCTUATION
from babel_poc.rendering.page_renderer import render_tokens


class BookConfig(BaseModel):
    mode_id: str
    seed: str
    pages: int = 410
    tokens_per_page: int = 320
    vocabulary_id: str = "unknown"
    punctuation: list[str] = DEFAULT_PUNCTUATION


class GeneratedPage(BaseModel):
    book_config: BookConfig
    page_index: int
    tokens: list[str]
    text: str


class LibraryGenerator(ABC):
    mode_id: str
    display_name: str

    def __init__(self, words: list[str], punctuation: list[str]) -> None:
        self.words = words
        self.punctuation = punctuation

    @abstractmethod
    def log10_size(self, pages: int = 410, tokens_per_page: int = 320) -> float:
        pass

    @abstractmethod
    def generate_token(self, seed: str, position: int) -> str:
        pass

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        tokens_per_page = config.tokens_per_page
        page_start = page_index * tokens_per_page
        tokens = [
            self.generate_token(config.seed, page_start + i)
            for i in range(tokens_per_page)
        ]
        text = render_tokens(tokens, set(config.punctuation))
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
