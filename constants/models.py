"""Constants related to LLM model configuration and client behavior."""

# Default model
DEFAULT_MODEL_NAME = "arcee-ai/trinity-large-preview:free"
DEFAULT_TEMPERATURE = 1
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0
DEFAULT_CONTEXT_WINDOW = 256_000

# Context compression threshold (fraction of context window)
CONTEXT_COMPRESSION_RATIO = 0.8

# LLM client retry settings
LLM_MAX_RETRIES = 3

# Default tokenizer encoding fallback
DEFAULT_TOKENIZER_ENCODING = "cl100k_base"
DEFAULT_TOKEN_MODEL = "gpt-4"
