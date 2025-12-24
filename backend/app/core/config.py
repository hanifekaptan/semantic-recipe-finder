"""Global configuration and runtime placeholders.

This module exposes file paths and module-level variables used to store
startup-loaded resources (embeddings, ids, model, dataframe) so they
can be accessed across the application without passing them explicitly.
"""

import numpy as np
import pandas as pd
from typing import Optional

recipes_details_path = "data/processed/master.parquet"
metadata_embeddings_path = "data/processed/metadata_embeddings.npy"
recipe_ids_path = "data/processed/ids_embeddings.npy"

model_name = "all-MiniLM-L6-v2"

embeddings = None
ids = None
model = None
df = None
temp_results = None 
temp_search_query = None
temp_search_pairs = None

ready = False