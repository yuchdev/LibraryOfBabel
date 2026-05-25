from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from babel.constants import DEFAULT_PUNCTUATION
from babel.generators.constants import SHARED_PUNCTUATION
from babel.generators.metadata import ModelMetadata
from babel.rendering.page_renderer import render_tokens


class BookConfig(BaseModel):
    mode_id: str
    seed: str
    pages: int = 410
    tokens_per_page: int = 320
    vocabulary_id: str = "unknown"
    punctuation: list[str] = Field(default_factory=lambda: list(DEFAULT_PUNCTUATION))


class GeneratedPage(BaseModel):
    book_config: BookConfig
    page_index: int
    tokens: list[str]
    text: str


class LibraryGenerator(ABC):
    mode_id: str
    metadata: ModelMetadata

    def __init__(self, words: list[str], punctuation: list[str]) -> None:
        self.words = words
        if punctuation and punctuation != SHARED_PUNCTUATION:
            mode_name = getattr(self, "mode_id", self.__class__.__name__)
            raise ValueError(
                f"{mode_name} requires shared punctuation "
                f"{SHARED_PUNCTUATION}, got {punctuation}"
            )
        self.punctuation = list(SHARED_PUNCTUATION)

    @property
    def display_name(self) -> str:
        return self.metadata.display_name

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
