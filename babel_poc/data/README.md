# Vocabulary Data Directory

Place vocabulary files here in plain text format (one word per line).

## Expected Format

```
the
house
river
memory
darkness
```

Lines starting with `#` are treated as comments and ignored. Empty lines are ignored. Words are deduplicated and sorted.

## Recommended Sources

- **SCOWL / English Wordlist**: https://wordlist.aspell.net/ — permissive license, multiple size options
- **WordNet / Open English WordNet**: https://wordnet.princeton.edu/
- **wordfreq**: `pip install wordfreq` then export a frequency list
- **Kaggle English word frequency**: https://www.kaggle.com/datasets/rtatman/english-word-frequency

## Demo Vocabulary

`vocabulary/demo.txt` contains a small demo vocabulary for testing and examples.
