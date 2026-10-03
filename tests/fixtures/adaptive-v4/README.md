# Synthetic native v4 contract fixture

This self-contained package is the authored-file protocol replay produced by
`tests/adaptive_fixture.py`, copied from the 2026-10-03 smoke run. The two repositories,
sources, resolutions and reviewer decisions are synthetic. It was not extracted
from Pylint, Pyflakes or Ruff, and no live model authored this replay.

Keep this fixture outside the serving package roots. It demonstrates package
integrity, semantic ports, Pattern alternatives and two historical realizations;
its eval definitions retain `not_executed`. The generated manifest's
`model_direct` authorship field denotes the file-authoring protocol, not a claim
that a model was called for this fixture.

Run the contained `scripts/verify_package.py` after copying the package. Current
bindings and oracles belong to each TaskContext and are not published into it.
