"""Frozen compact-corpus receipt registry; no materializer or data loader."""

from .manifest import CORPUS_RECEIPTS, CompactCorpusReceipt, CorpusFile

__all__ = ["CORPUS_RECEIPTS", "CompactCorpusReceipt", "CorpusFile"]
