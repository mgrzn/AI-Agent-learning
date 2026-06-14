from src.summarizer import summarize as _summarize

def summarize(text: str, context: str = "crypto/NFT/Web3") -> str:
    return _summarize(text, context)