#!/usr/bin/env python3
"""
Product model for the e-commerce cart system
"""

from decimal import Decimal
from typing import Dict, Any


class Product:
    """Product model with pricing and inventory info"""
    
    def __init__(self, product_id: str, name: str, price: Decimal, inventory_count: int = 0):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.inventory_count = inventory_count
        self.category = "general"
        self.tax_rate = Decimal('0.08')  # 8% tax rate
        self.weight = Decimal('1.0')  # Weight in kg
        self.dimensions = {'length': 10, 'width': 10, 'height': 5}  # cm
        self.is_active = True
        self.description = f"High quality {name}"
    
    def __str__(self):
        return f"Product({self.product_id}: {self.name} - ${self.price})"
    
    def __repr__(self):
        return f"Product(product_id='{self.product_id}', name='{self.name}', price={self.price})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary representation"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': float(self.price),
            'inventory_count': self.inventory_count,
            'category': self.category,
            'tax_rate': float(self.tax_rate),
            'weight': float(self.weight),
            'dimensions': self.dimensions,
            'is_active': self.is_active,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create product from dictionary representation"""
        product = cls(
            product_id=data['product_id'],
            name=data['name'],
            price=Decimal(str(data['price'])),
            inventory_count=data.get('inventory_count', 0)
        )
        product.category = data.get('category', 'general')
        product.tax_rate = Decimal(str(data.get('tax_rate', '0.08')))
        product.weight = Decimal(str(data.get('weight', '1.0')))
        product.dimensions = data.get('dimensions', {'length': 10, 'width': 10, 'height': 5})
        product.is_active = data.get('is_active', True)
        product.description = data.get('description', f"High quality {product.name}")
        return product
    
    def calculate_shipping_cost(self) -> Decimal:
        """Calculate shipping cost based on weight and dimensions"""
        # Simple shipping calculation
        volume = Decimal(str(self.dimensions['length'] * self.dimensions['width'] * self.dimensions['height'])) / 1000  # cubic cm to litres
        weight_cost = self.weight * Decimal('2.50')  # $2.50 per kg
        volume_cost = volume * Decimal('0.10')  # $0.10 per litre
        return max(weight_cost, volume_cost)
    
    def is_available(self) -> bool:
        """Check if product is available for purchase"""
        return self.is_active and self.inventory_count > 0
    
    def get_tax_amount(self) -> Decimal:
        """Calculate tax amount for this product"""
        return self.price * self.tax_rate
    
    def get_total_price(self) -> Decimal:
        """Get total price including tax"""
        return self.price + self.get_tax_amount()


# Sample products for testing
SAMPLE_PRODUCTS = {
    'LAPTOP001': Product(
        product_id='LAPTOP001',
        name='Gaming Laptop',
        price=Decimal('1299.99'),
        inventory_count=15
    ),
    'MOUSE001': Product(
        product_id='MOUSE001', 
        name='Wireless Mouse',
        price=Decimal('29.99'),
        inventory_count=100
    ),
    'KEYBOARD001': Product(
        product_id='KEYBOARD001',
        name='Mechanical Keyboard', 
        price=Decimal('89.99'),
        inventory_count=50
    ),
    'MONITOR001': Product(
        product_id='MONITOR001',
        name='4K Monitor',
        price=Decimal('399.99'),
        inventory_count=25
    ),
    'HEADPHONES001': Product(
        product_id='HEADPHONES001',
        name='Noise Cancelling Headphones',
        price=Decimal('199.99'),
        inventory_count=30
    )
}

# Initialize sample products with details
SAMPLE_PRODUCTS['LAPTOP001'].category = 'electronics'
SAMPLE_PRODUCTS['LAPTOP001'].weight = Decimal('2.5')
SAMPLE_PRODUCTS['LAPTOP001'].dimensions = {'length': 35, 'width': 25, 'height': 3}

SAMPLE_PRODUCTS['MOUSE001'].category = 'electronics'
SAMPLE_PRODUCTS['MOUSE001'].weight = Decimal('0.1')
SAMPLE_PRODUCTS['MOUSE001'].dimensions = {'length': 12, 'width': 7, 'height': 4}

SAMPLE_PRODUCTS['KEYBOARD001'].category = 'electronics'
SAMPLE_PRODUCTS['KEYBOARD001'].weight = Decimal('0.8')
SAMPLE_PRODUCTS['KEYBOARD001'].dimensions = {'length': 45, 'width': 15, 'height': 4}

SAMPLE_PRODUCTS['MONITOR001'].category = 'electronics'
SAMPLE_PRODUCTS['MONITOR001'].weight = Decimal('5.2')
SAMPLE_PRODUCTS['MONITOR001'].dimensions = {'length': 60, 'width': 40, 'height': 8}

SAMPLE_PRODUCTS['HEADPHONES001'].category = 'electronics'
SAMPLE_PRODUCTS['HEADPHONES001'].weight = Decimal('0.3')
SAMPLE_PRODUCTS['HEADPHONES001'].dimensions = {'length': 20, 'width': 18, 'height': 8} 
