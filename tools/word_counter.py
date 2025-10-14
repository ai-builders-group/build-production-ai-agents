# tools/word_counter.py

from langchain_core.tools import tool


@tool
def count_words(text: str) -> int:
    """
    Counts the number of words in a given text.
    Use this when a user asks for the length of a document, a sentence, or any piece of text.
    The input should be the text whose words you want to count.
    """
    print(f"\n---EXECUTING WORD COUNT TOOL---")
    return len(text.split())
