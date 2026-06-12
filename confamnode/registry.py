from confamnode import models

# =========================================================================
# Cloud Models — inference via external providers
# =========================================================================
CLOUD_MODELS = {
    # Free chat
    models.LITE,
    models.SPEED,
    models.REASONING,

    # Paid chat
    models.INTELLIGENCE,
    models.DEEP_REASONING,
    models.CODE,
    models.CODE_PRO,
    models.VISION,
    models.AUDIO,
    models.TTS,

    # Free embeddings
    models.EMBED_TEXT,
    models.EMBED_MULTIMODAL,
    models.EMBED_MULTIMODAL_2,

    # Paid embeddings
    models.EMBED_TEXT_PRO,
    models.EMBED_MULTIMODAL_PRO,
    models.EMBED_MULTILINGUAL,
    models.EMBED_SMALL,
    models.EMBED_0_6B,

    # Rerank
    models.RERANK,
    models.RERANK_FAST,
}

# =========================================================================
# Local Models — inference on Nigerian hardware, Nigeria data residency
# =========================================================================
LOCAL_MODELS = {
    models.NANO,
    models.EMBED_TEXT_LOCAL,
}

# =========================================================================
# Nigeria Data Residency Models — data never leaves Nigeria
# =========================================================================
NGN_DATA_RESIDENCY_MODELS = LOCAL_MODELS  # same as local for now

# =========================================================================
# All Valid Models
# =========================================================================
VALID_MODELS = CLOUD_MODELS | LOCAL_MODELS