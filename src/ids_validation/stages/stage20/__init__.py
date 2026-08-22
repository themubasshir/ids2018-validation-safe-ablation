"""Stage 20 namespace; scientific extraction is intentionally stage-scoped.

Only static registries and toy-data helpers live here.  The historical PCAP,
reconstruction, corpus, training, and evaluation operations are not callable.
"""

STAGE_NUMBER = 20
SOURCE_CELLS = tuple(range(312, 462))
