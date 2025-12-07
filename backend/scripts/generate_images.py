#!/usr/bin/env python3
"""
Generate pre-computed test images for Dicrhomat application.

This script generates 100 static test images and their metadata to replace
on-the-fly image generation with pre-generated static assets.

Usage:
    python backend/scripts/generate_images.py [OPTIONS]

Options:
    --output-dir DIR    Directory for generated images (default: backend/static/test_images)
    --count NUM         Number of images to generate (default: 100)
    --format FORMAT     Image format: png or jpeg (default: png)
    --seed SEED         Random seed for reproducibility (default: current timestamp)
    --metadata-file FILE Metadata output path (default: output-dir/metadata.json)
"""

import argparse
import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.image_generator import ImageGenerator


def generate_random_answer(image_id: int, seed: str) -> int:
    """Generate a random answer for an image using deterministic seeding."""
    import random
    seed_str = f"{seed}-{image_id}"
    rng = random.Random(hashlib.md5(seed_str.encode()).hexdigest())
    return rng.randint(10, 89)


def main():
    parser = argparse.ArgumentParser(
        description='Generate pre-computed test images for Dicrhomat',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--output-dir',
        default='backend/static/test_images',
        help='Directory for generated images (default: backend/static/test_images)'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=100,
        help='Number of images to generate (default: 100)'
    )
    parser.add_argument(
        '--format',
        default='png',
        choices=['png', 'jpeg'],
        help='Image format (default: png)'
    )
    parser.add_argument(
        '--seed',
        default=None,
        help='Random seed for reproducibility (default: current timestamp)'
    )
    parser.add_argument(
        '--metadata-file',
        default=None,
        help='Metadata output path (default: output-dir/metadata.json)'
    )

    args = parser.parse_args()

    # Set default seed if not provided
    if args.seed is None:
        args.seed = str(datetime.now().timestamp())

    # Initialize generator with seed
    generator = ImageGenerator(seed_salt=args.seed)

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set metadata file path
    if args.metadata_file is None:
        metadata_path = output_dir / 'metadata.json'
    else:
        metadata_path = Path(args.metadata_file)

    # Initialize metadata structure
    metadata = {
        'version': '1.0',
        'generated_at': datetime.now().isoformat() + 'Z',
        'total_images': args.count,
        'seed': args.seed,
        'images': []
    }

    print(f"Generating {args.count} test images...")
    print(f"Output directory: {output_dir.absolute()}")
    print(f"Seed: {args.seed}")
    print("-" * 60)

    # Generate images by type
    for i in range(args.count):
        # Determine dichromism type and generate answer based on image number
        if i < 30:
            dichromism_type = 'protanopia'
            correct_answer = generate_random_answer(i, args.seed)
        elif i < 60:
            dichromism_type = 'deuteranopia'
            correct_answer = generate_random_answer(i, args.seed)
        elif i < 90:
            dichromism_type = 'tritanopia'
            correct_answer = generate_random_answer(i, args.seed)
        else:
            dichromism_type = 'control'
            correct_answer = generate_random_answer(i, args.seed)

        # Generate image using a deterministic session_id
        # Use image number as both session_id component and image_number
        # to ensure unique, reproducible images
        image_bytes = generator.generate_test_image(
            session_id=f'pregenerated-{i}',
            image_number=1,  # Always use 1 since we're using unique session_id per image
            dichromism_type=dichromism_type,
            correct_answer=correct_answer
        )

        # Save image
        filename = f'image_{i:03d}.{args.format}'
        filepath = output_dir / filename
        filepath.write_bytes(image_bytes)

        # Calculate hash for integrity verification
        image_hash = hashlib.sha256(image_bytes).hexdigest()

        # Determine difficulty (can be enhanced with actual difficulty calculation)
        difficulty = 'medium'

        # Store metadata
        metadata['images'].append({
            'id': i,
            'filename': filename,
            'correct_answer': correct_answer,
            'dichromism_type': dichromism_type,
            'difficulty': difficulty,
            'sha256': image_hash,
            'file_size': len(image_bytes)
        })

        # Progress indicator
        print(f"[{i+1:3d}/{args.count}] {filename:16} | {dichromism_type:12} | Answer: {correct_answer:2d} | {len(image_bytes)//1024:3d}KB")

    # Write metadata file
    metadata_path.write_text(json.dumps(metadata, indent=2))

    # Summary
    print("-" * 60)
    print(f"\n✓ Successfully generated {args.count} images")
    print(f"✓ Total size: {sum(img['file_size'] for img in metadata['images']) / 1024 / 1024:.2f} MB")
    print(f"✓ Output directory: {output_dir.absolute()}")
    print(f"✓ Metadata file: {metadata_path.absolute()}")
    print(f"\nImage distribution:")
    print(f"  - Protanopia:   {sum(1 for img in metadata['images'] if img['dichromism_type'] == 'protanopia')} images (IDs 0-29)")
    print(f"  - Deuteranopia: {sum(1 for img in metadata['images'] if img['dichromism_type'] == 'deuteranopia')} images (IDs 30-59)")
    print(f"  - Tritanopia:   {sum(1 for img in metadata['images'] if img['dichromism_type'] == 'tritanopia')} images (IDs 60-89)")
    print(f"  - Control:      {sum(1 for img in metadata['images'] if img['dichromism_type'] == 'control')} images (IDs 90-99)")


if __name__ == '__main__':
    main()
