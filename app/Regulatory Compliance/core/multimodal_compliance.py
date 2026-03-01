"""
Multi-Modal Compliance (Loophole #24)
Validates content across text, image, video, and audio
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from core.context import ComplianceContext, ComplianceReport


class ModalityType(Enum):
    """Content modality types"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"  # Mixed content


class MultiModalValidator:
    """
    Multi-Modal Compliance Validator
    
    Validates content across different modalities:
    1. Text - Direct text analysis
    2. Image - OCR + visual analysis
    3. Video - Frame extraction + audio transcription
    4. Audio - Speech-to-text + audio analysis
    5. Multimodal - Combined analysis
    """
    
    def __init__(self):
        self.supported_modalities = [
            ModalityType.TEXT,
            ModalityType.IMAGE,
            ModalityType.VIDEO,
            ModalityType.AUDIO,
        ]
    
    def validate(self, context: ComplianceContext) -> Dict[str, Any]:
        """
        Validate content based on modality
        
        Args:
            context: Compliance context
            
        Returns:
            Validation results with extracted content
        """
        
        content_type = context.content_type
        
        if content_type == "text":
            return self._validate_text(context)
        elif content_type == "image":
            return self._validate_image(context)
        elif content_type == "video":
            return self._validate_video(context)
        elif content_type == "audio":
            return self._validate_audio(context)
        else:
            return {
                "modality": "unknown",
                "extracted_content": [],
                "warnings": [f"Unsupported content type: {content_type}"],
            }
    
    def _validate_text(self, context: ComplianceContext) -> Dict[str, Any]:
        """Validate text content"""
        
        return {
            "modality": ModalityType.TEXT.value,
            "extracted_content": [
                {
                    "type": "text",
                    "content": context.content,
                    "confidence": 1.0,
                }
            ],
            "warnings": [],
        }
    
    def _validate_image(self, context: ComplianceContext) -> Dict[str, Any]:
        """
        Validate image content
        
        In production, this would:
        1. Run OCR to extract text from image
        2. Analyze visual content (objects, scenes)
        3. Detect embedded text, logos, faces
        4. Check for manipulated/deepfake images
        """
        
        # Placeholder: In production, integrate OCR (Tesseract, Google Vision, AWS Rekognition)
        extracted_content = []
        warnings = []
        
        # Check if image analysis metadata provided
        if "ocr_text" in context.metadata:
            extracted_content.append({
                "type": "text_from_image",
                "content": context.metadata["ocr_text"],
                "confidence": context.metadata.get("ocr_confidence", 0.8),
            })
        else:
            warnings.append("No OCR text provided - image text not analyzed")
        
        # Check for visual content analysis
        if "visual_labels" in context.metadata:
            extracted_content.append({
                "type": "visual_labels",
                "content": context.metadata["visual_labels"],
                "confidence": context.metadata.get("visual_confidence", 0.7),
            })
        else:
            warnings.append("No visual analysis provided - image content not analyzed")
        
        # Check for face detection
        if "faces_detected" in context.metadata:
            extracted_content.append({
                "type": "faces",
                "content": f"{context.metadata['faces_detected']} faces detected",
                "confidence": 0.9,
            })
        
        return {
            "modality": ModalityType.IMAGE.value,
            "extracted_content": extracted_content,
            "warnings": warnings,
            "requires_ocr": "ocr_text" not in context.metadata,
            "requires_visual_analysis": "visual_labels" not in context.metadata,
        }
    
    def _validate_video(self, context: ComplianceContext) -> Dict[str, Any]:
        """
        Validate video content
        
        In production, this would:
        1. Extract key frames
        2. Run OCR on frames
        3. Transcribe audio track
        4. Analyze visual content
        5. Detect scene changes, objects, faces
        """
        
        extracted_content = []
        warnings = []
        
        # Check for video transcription
        if "video_transcript" in context.metadata:
            extracted_content.append({
                "type": "audio_transcript",
                "content": context.metadata["video_transcript"],
                "confidence": context.metadata.get("transcript_confidence", 0.85),
            })
        else:
            warnings.append("No video transcript provided - audio not analyzed")
        
        # Check for frame analysis
        if "frame_texts" in context.metadata:
            for i, frame_text in enumerate(context.metadata["frame_texts"]):
                extracted_content.append({
                    "type": "text_from_frame",
                    "content": frame_text,
                    "frame_number": i,
                    "confidence": 0.8,
                })
        else:
            warnings.append("No frame analysis provided - visual text not analyzed")
        
        # Check for scene analysis
        if "scene_labels" in context.metadata:
            extracted_content.append({
                "type": "scene_labels",
                "content": context.metadata["scene_labels"],
                "confidence": 0.75,
            })
        else:
            warnings.append("No scene analysis provided - video content not analyzed")
        
        return {
            "modality": ModalityType.VIDEO.value,
            "extracted_content": extracted_content,
            "warnings": warnings,
            "requires_transcription": "video_transcript" not in context.metadata,
            "requires_frame_analysis": "frame_texts" not in context.metadata,
            "requires_scene_analysis": "scene_labels" not in context.metadata,
        }
    
    def _validate_audio(self, context: ComplianceContext) -> Dict[str, Any]:
        """
        Validate audio content
        
        In production, this would:
        1. Transcribe speech to text
        2. Analyze audio characteristics (tone, emotion)
        3. Detect background sounds
        4. Identify speakers
        """
        
        extracted_content = []
        warnings = []
        
        # Check for audio transcription
        if "audio_transcript" in context.metadata:
            extracted_content.append({
                "type": "audio_transcript",
                "content": context.metadata["audio_transcript"],
                "confidence": context.metadata.get("transcript_confidence", 0.85),
            })
        else:
            warnings.append("No audio transcript provided - speech not analyzed")
        
        # Check for speaker identification
        if "speakers" in context.metadata:
            extracted_content.append({
                "type": "speakers",
                "content": f"{context.metadata['speakers']} speakers detected",
                "confidence": 0.8,
            })
        
        # Check for emotion analysis
        if "audio_emotion" in context.metadata:
            extracted_content.append({
                "type": "emotion",
                "content": context.metadata["audio_emotion"],
                "confidence": 0.7,
            })
        
        return {
            "modality": ModalityType.AUDIO.value,
            "extracted_content": extracted_content,
            "warnings": warnings,
            "requires_transcription": "audio_transcript" not in context.metadata,
        }
    
    def extract_all_text(self, validation_result: Dict[str, Any]) -> str:
        """Extract all text content from validation result"""
        
        all_text = []
        
        for item in validation_result.get("extracted_content", []):
            if item["type"] in ["text", "text_from_image", "text_from_frame", "audio_transcript"]:
                all_text.append(str(item["content"]))
        
        return " ".join(all_text)
    
    def get_integration_guide(self) -> Dict[str, Any]:
        """Get integration guide for multi-modal analysis"""
        
        return {
            "image_ocr": {
                "recommended_services": [
                    "Google Cloud Vision API",
                    "AWS Rekognition",
                    "Azure Computer Vision",
                    "Tesseract OCR (open-source)",
                ],
                "metadata_required": ["ocr_text", "ocr_confidence", "visual_labels"],
            },
            "video_analysis": {
                "recommended_services": [
                    "Google Cloud Video Intelligence",
                    "AWS Rekognition Video",
                    "Azure Video Indexer",
                ],
                "metadata_required": [
                    "video_transcript",
                    "frame_texts",
                    "scene_labels",
                    "transcript_confidence",
                ],
            },
            "audio_transcription": {
                "recommended_services": [
                    "Google Cloud Speech-to-Text",
                    "AWS Transcribe",
                    "Azure Speech Services",
                    "Whisper (OpenAI, open-source)",
                ],
                "metadata_required": ["audio_transcript", "transcript_confidence", "speakers"],
            },
        }


class MultiModalComplianceEngine:
    """
    Multi-Modal Compliance Engine
    
    Orchestrates multi-modal validation with compliance checking
    """
    
    def __init__(self, compliance_engine):
        self.compliance_engine = compliance_engine
        self.multimodal_validator = MultiModalValidator()
    
    def check(self, context: ComplianceContext) -> ComplianceReport:
        """
        Check compliance across all modalities
        
        Args:
            context: Compliance context
            
        Returns:
            ComplianceReport with multi-modal analysis
        """
        
        # Step 1: Validate and extract content from all modalities
        validation_result = self.multimodal_validator.validate(context)
        
        # Step 2: Extract all text content
        extracted_text = self.multimodal_validator.extract_all_text(validation_result)
        
        # Step 3: Create enriched context with extracted content
        enriched_context = ComplianceContext(
            user_id=context.user_id,
            content=context.content if context.content_type == "text" else extracted_text,
            content_type=context.content_type,
            metadata={
                **context.metadata,
                "multimodal_validation": validation_result,
                "extracted_text": extracted_text,
                "original_content_type": context.content_type,
            }
        )
        
        # Step 4: Run compliance check on enriched context
        report = self.compliance_engine.check(enriched_context)
        
        # Step 5: Add multi-modal warnings to report
        if validation_result.get("warnings"):
            multimodal_warnings = "\n\n⚠️  MULTI-MODAL WARNINGS:\n"
            for warning in validation_result["warnings"]:
                multimodal_warnings += f"• {warning}\n"
            
            report.message = (
                f"{report.message}{multimodal_warnings}"
                if report.message
                else multimodal_warnings
            )
        
        # Step 6: Flag if content not fully analyzed
        if validation_result.get("requires_ocr") or \
           validation_result.get("requires_transcription") or \
           validation_result.get("requires_frame_analysis"):
            
            report.message = (
                f"{report.message}\n\n⚠️  INCOMPLETE ANALYSIS: "
                f"Some content modalities not fully analyzed. "
                f"Integrate OCR/transcription services for complete compliance checking."
                if report.message
                else "⚠️  INCOMPLETE ANALYSIS: Some content modalities not fully analyzed."
            )
            
            # Mark as requiring human review
            context.metadata["requires_manual_review"] = True
            context.metadata["manual_review_reason"] = "Incomplete multi-modal analysis"
        
        return report
