from confamnode import models

# =========================================================================
# Cloud Models — inference via external providers
# =========================================================================
CLOUD_MODELS = {
    # ------------------------------------------------------------------- FREE -------------------------------------------------------------------

    # Text/Image/Video/File/Audio -> Text
    "gemini/gemini-3.1-flash-lite", 
    "gemini/gemini-3.5-flash-lite",

    # Text -> Text
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",

    # Text -> Embeddings
    "liquid/lfm-2.5-embedding-350m:free",

    # ------------------------------------------------------------------- PAID -------------------------------------------------------------------

    # Text/Image -> Text
    "deepseek/deepseek-v4.1-flash",

    # Text -> Embeddings
    "google/gemini-embedding-001",

    # Text/Image/File/Audio/Video -> Text
    "google/gemini-embedding-2",
}

# =========================================================================
# Local Models — inference on Nigerian hardware, Nigeria data residency
# =========================================================================
LOCAL_MODELS = {
    models.HEALTH,
    models.LOCAL,
    models.EMBED_LOCAL,
}

# =========================================================================
# Nigeria Data Residency Models — data never leaves Nigeria
# =========================================================================
NGN_DATA_RESIDENCY_MODELS = LOCAL_MODELS  # same as local for now

# =========================================================================
# All Valid Models
# =========================================================================
VALID_MODELS = CLOUD_MODELS # | LOCAL_MODELS