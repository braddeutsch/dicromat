"""Dichromat simulation using Machado et al. (2009) transformation matrices."""

import numpy as np
from .luminance import srgb_to_linear, linear_to_srgb


DEUTERANOPIA_MATRIX = np.array([
    [0.625, 0.375, 0.0],
    [0.7,   0.3,   0.0],
    [0.0,   0.03,  0.97]
])

PROTANOPIA_MATRIX = np.array([
    [0.567, 0.433, 0.0],
    [0.558, 0.442, 0.0],
    [0.0,   0.242, 0.758]
])

TRITANOPIA_MATRIX = np.array([
    [0.95,  0.05,  0.0],
    [0.0,   0.433, 0.567],
    [0.0,   0.475, 0.525]
])


def simulate_dichromat(rgb: tuple, dichromat_type: str = 'deuteranopia') -> tuple:
    """
    Simulate how a color appears to someone with dichromacy.
    
    Args:
        rgb: Tuple of (R, G, B) values in 0-255 range
        dichromat_type: One of 'deuteranopia', 'protanopia', or 'tritanopia'
    
    Returns:
        Simulated (R, G, B) tuple in 0-255 range
    """
    r_lin = srgb_to_linear(rgb[0] / 255.0)
    g_lin = srgb_to_linear(rgb[1] / 255.0)
    b_lin = srgb_to_linear(rgb[2] / 255.0)
    
    rgb_linear = np.array([r_lin, g_lin, b_lin])
    
    if dichromat_type == 'protanopia':
        transform = PROTANOPIA_MATRIX
    elif dichromat_type == 'tritanopia':
        transform = TRITANOPIA_MATRIX
    else:
        transform = DEUTERANOPIA_MATRIX
    
    simulated = np.dot(transform, rgb_linear)
    simulated = np.clip(simulated, 0.0, 1.0)
    
    r_out = int(round(linear_to_srgb(simulated[0]) * 255))
    g_out = int(round(linear_to_srgb(simulated[1]) * 255))
    b_out = int(round(linear_to_srgb(simulated[2]) * 255))
    
    return (
        max(0, min(255, r_out)),
        max(0, min(255, g_out)),
        max(0, min(255, b_out))
    )


def simulate_image(image_array: np.ndarray, dichromat_type: str = 'deuteranopia') -> np.ndarray:
    """
    Apply dichromat simulation to an entire image.
    
    Args:
        image_array: NumPy array of shape (H, W, 3) with values 0-255
        dichromat_type: One of 'deuteranopia', 'protanopia', or 'tritanopia'
    
    Returns:
        Simulated image as NumPy array
    """
    if dichromat_type == 'protanopia':
        transform = PROTANOPIA_MATRIX
    elif dichromat_type == 'tritanopia':
        transform = TRITANOPIA_MATRIX
    else:
        transform = DEUTERANOPIA_MATRIX
    
    normalized = image_array / 255.0
    
    linear = np.where(
        normalized <= 0.04045,
        normalized / 12.92,
        ((normalized + 0.055) / 1.055) ** 2.4
    )
    
    h, w, _ = linear.shape
    flat = linear.reshape(-1, 3)
    simulated = np.dot(flat, transform.T)
    simulated = np.clip(simulated, 0.0, 1.0)
    simulated = simulated.reshape(h, w, 3)
    
    srgb = np.where(
        simulated <= 0.0031308,
        simulated * 12.92,
        1.055 * (simulated ** (1/2.4)) - 0.055
    )
    
    return np.clip(srgb * 255, 0, 255).astype(np.uint8)
