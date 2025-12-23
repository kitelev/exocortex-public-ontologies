#!/usr/bin/env python3
"""Pytest configuration for exocortex-public-ontologies tests."""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
