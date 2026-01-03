"""Global configuration and runtime placeholders.

This module exposes file paths and module-level variables used to store
startup-loaded resources (embeddings, ids, model, dataframe) so they
can be accessed across the application without passing them explicitly.
"""

recipes_details_path = "data/processed/master_df.parquet"
metadata_embeddings_path = "data/processed/metadata_embs.npy"
recipe_ids_path = "data/processed/ids_embs.npy"

model_name = "all-MiniLM-L6-v2"

model = None
df = None

chroma_collection = None
detail_service = None
search_service = None

ready = False