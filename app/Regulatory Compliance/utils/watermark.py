def apply_meity_label(content: str, content_type: str = "text") -> str:
    """
    Appends mandatory disclaimer based on MeitY Advisory.
    """
    disclaimer = "\n\n[Disclaimer: This content is artificially generated.]"

    if content_type == "text":
        return content + disclaimer
    elif content_type == "image":
        # In a real scenario, you would modify image metadata here
        # For now, we return a placeholder instruction
        return content
    else:
        return content


def apply_sgi_label(
    content: str, content_type: str = "text", metadata: dict = None
) -> dict:
    """
    Applies Synthetically Generated Information (SGI) labeling
    as per IT Amendment Rules 2026.

    Requirements:
    - Prominent labeling (visible for 10% of content duration/area)
    - Metadata embedding for traceability
    - Timestamp and source information

    Returns:
    - Dictionary with labeled content and metadata
    """
    from datetime import datetime

    if metadata is None:
        metadata = {}

    # Add SGI metadata
    sgi_metadata = {
        "is_ai_generated": True,
        "has_sgi_label": True,
        "generation_timestamp": datetime.now().isoformat(),
        "sgi_compliance": "IT Amendment Rules 2026",
        "label_visibility": "10% minimum",
    }

    if content_type == "text":
        # Add prominent label at the beginning and end
        labeled_content = (
            "🤖 [AI-GENERATED CONTENT]\n\n"
            + content
            + "\n\n🤖 [END AI-GENERATED CONTENT]"
            + "\n[Disclaimer: This content is synthetically generated using AI. "
            + f"Generated on: {sgi_metadata['generation_timestamp']}]"
        )

    elif content_type == "image":
        # For images, return instructions for watermarking
        labeled_content = content
        sgi_metadata["watermark_instruction"] = (
            "Apply visible watermark covering 10% of image area with text: 'AI-GENERATED'"
        )
        sgi_metadata["metadata_embedding"] = (
            "Embed generation timestamp and source in EXIF/XMP metadata"
        )

    elif content_type == "video":
        labeled_content = content
        sgi_metadata["watermark_instruction"] = (
            "Apply visible watermark throughout video duration (10% of frame area)"
        )
        sgi_metadata["audio_disclaimer"] = (
            "Add audio disclaimer at start: 'This is AI-generated content'"
        )

    elif content_type == "audio":
        labeled_content = content
        sgi_metadata["audio_disclaimer"] = (
            "Prepend audio: 'This is AI-generated audio content'"
        )

    else:
        labeled_content = content

    return {"content": labeled_content, "metadata": {**metadata, **sgi_metadata}}


def generate_content_hash(content: str) -> str:
    """
    Generates hash for content traceability
    """
    import hashlib

    return hashlib.sha256(content.encode()).hexdigest()


def verify_consent_declaration(user_id: str, consent_type: str = "sgi") -> bool:
    """
    Verifies user consent declaration for SGI generation
    In production, this would check against a consent management system
    """
    # Placeholder - in production, query consent database
    return False  # Default to no consent for safety