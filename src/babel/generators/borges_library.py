import math
from babel.generators.base import BookConfig, GeneratedPage, LibraryGenerator
from babel.utils.hashing import deterministic_index

class BorgesLibraryGenerator(LibraryGenerator):
    mode_id = "borges-library"
    display_name = "Original Borges Library"

    def __init__(self, words: list[str], punctuation: list[str]) -> None:
        super().__init__(words, punctuation)
        # Borges model is character-based.
        # Adjusted to English: 26 letters + space + punctuations
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz ") + punctuation

    def log10_size(self, pages: int = 410, tokens_per_page: int = 3200) -> float:
        """S^N where S is alphabet size and N is total characters."""
        # Note: tokens_per_page for Borges means characters_per_page
        n = pages * tokens_per_page
        return n * math.log10(len(self.alphabet))

    def generate_token(self, seed: str, position: int) -> str:
        idx = deterministic_index(seed, self.mode_id, position, len(self.alphabet))
        return self.alphabet[idx]

    def generate_page(self, config: BookConfig, page_index: int) -> GeneratedPage:
        # Default Borges page: 40 lines * 80 chars = 3200 chars
        chars_per_page = config.tokens_per_page
        page_start = page_index * chars_per_page
        tokens = [
            self.generate_token(config.seed, page_start + i)
            for i in range(chars_per_page)
        ]
        # Text is just joining characters for Borges.
        text = "".join(tokens)
        return GeneratedPage(
            book_config=config,
            page_index=page_index,
            tokens=tokens,
            text=text,
        )
