"""
Image Selector Service

This service deterministically maps session IDs to pre-generated test images.
Each test session receives a unique combination of 10 images from a pool of 100:
- 3 protanopia images (from IDs 0-29)
- 3 deuteranopia images (from IDs 30-59)
- 3 tritanopia images (from IDs 60-89)
- 1 control image (from IDs 90-99)

The mapping is deterministic based on session_id, ensuring that the same
session always receives the same images.
"""

import random
import json
from pathlib import Path
from typing import Dict, List, Optional


class ImageSelector:
    """Service for selecting pre-generated images for test sessions."""

    def __init__(self, metadata_path: str):
        """
        Initialize ImageSelector with metadata file.

        Args:
            metadata_path: Path to the metadata.json file containing image information

        Raises:
            FileNotFoundError: If metadata file doesn't exist
            ValueError: If metadata format is invalid
        """
        metadata_file = Path(metadata_path)
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

        self.metadata = json.loads(metadata_file.read_text())
        self.metadata_path = metadata_path

        # Validate metadata version
        if self.metadata.get('version') != '1.0':
            raise ValueError(f"Unsupported metadata version: {self.metadata.get('version')}")

        # Organize images by dichromism type for efficient selection
        self.protanopia_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'protanopia'
        ]
        self.deuteranopia_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'deuteranopia'
        ]
        self.tritanopia_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'tritanopia'
        ]
        self.control_images = [
            img for img in self.metadata['images']
            if img['dichromism_type'] == 'control'
        ]

        # Validate we have enough images of each type
        if len(self.protanopia_images) < 3:
            raise ValueError(f"Insufficient protanopia images: {len(self.protanopia_images)} < 3")
        if len(self.deuteranopia_images) < 3:
            raise ValueError(f"Insufficient deuteranopia images: {len(self.deuteranopia_images)} < 3")
        if len(self.tritanopia_images) < 3:
            raise ValueError(f"Insufficient tritanopia images: {len(self.tritanopia_images)} < 3")
        if len(self.control_images) < 1:
            raise ValueError(f"Insufficient control images: {len(self.control_images)} < 1")

    def get_session_image_mapping(self, session_id: str) -> Dict[int, int]:
        """
        Get mapping of test image numbers (1-10) to pre-generated image IDs.

        This method deterministically selects 10 images from the pool based on
        the session_id. The same session_id will always produce the same mapping.

        Args:
            session_id: Unique session identifier

        Returns:
            Dictionary mapping test image number (1-10) to pre-generated image ID (0-99)
            Example: {1: 5, 2: 12, 3: 7, 4: 35, 5: 41, 6: 58, 7: 62, 8: 75, 9: 88, 10: 92}
        """
        # Seed random with session_id for reproducibility
        rng = random.Random(session_id)

        # Select images from each type
        selected_protanopia = rng.sample(self.protanopia_images, 3)
        selected_deuteranopia = rng.sample(self.deuteranopia_images, 3)
        selected_tritanopia = rng.sample(self.tritanopia_images, 3)
        selected_control = rng.sample(self.control_images, 1)

        # Map to test image numbers (1-10)
        # Images 1-3: Protanopia
        # Images 4-6: Deuteranopia
        # Images 7-9: Tritanopia
        # Image 10: Control
        mapping = {
            1: selected_protanopia[0]['id'],
            2: selected_protanopia[1]['id'],
            3: selected_protanopia[2]['id'],
            4: selected_deuteranopia[0]['id'],
            5: selected_deuteranopia[1]['id'],
            6: selected_deuteranopia[2]['id'],
            7: selected_tritanopia[0]['id'],
            8: selected_tritanopia[1]['id'],
            9: selected_tritanopia[2]['id'],
            10: selected_control[0]['id'],
        }

        return mapping

    def get_image_info(self, image_id: int) -> Optional[dict]:
        """
        Get metadata for a specific pre-generated image.

        Args:
            image_id: The image ID (0-99)

        Returns:
            Dictionary containing image metadata, or None if not found
        """
        # Find image by id
        for img in self.metadata['images']:
            if img['id'] == image_id:
                return img
        return None

    def get_image_info_by_filename(self, filename: str) -> Optional[dict]:
        """
        Get metadata for an image by its filename.

        Args:
            filename: The image filename (e.g., 'image_042.png')

        Returns:
            Dictionary containing image metadata, or None if not found
        """
        for img in self.metadata['images']:
            if img['filename'] == filename:
                return img
        return None

    def verify_image_integrity(self, image_id: int, image_bytes: bytes) -> bool:
        """
        Verify the integrity of an image using its SHA-256 hash.

        Args:
            image_id: The image ID
            image_bytes: The actual image bytes to verify

        Returns:
            True if hash matches, False otherwise
        """
        import hashlib

        image_info = self.get_image_info(image_id)
        if not image_info:
            return False

        actual_hash = hashlib.sha256(image_bytes).hexdigest()
        expected_hash = image_info.get('sha256')

        return actual_hash == expected_hash

    def get_statistics(self) -> dict:
        """
        Get statistics about the pre-generated image pool.

        Returns:
            Dictionary with image pool statistics
        """
        return {
            'total_images': len(self.metadata['images']),
            'protanopia_count': len(self.protanopia_images),
            'deuteranopia_count': len(self.deuteranopia_images),
            'tritanopia_count': len(self.tritanopia_images),
            'control_count': len(self.control_images),
            'total_size_bytes': sum(img['file_size'] for img in self.metadata['images']),
            'total_size_mb': sum(img['file_size'] for img in self.metadata['images']) / 1024 / 1024,
            'generated_at': self.metadata.get('generated_at'),
            'version': self.metadata.get('version'),
        }
