#!/usr/bin/env python3
"""
E-commerce Shopping Cart System
This is the system that needs comprehensive unit testing.
"""

import json
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid


class Product:
    """Product model with pricing and inventory info"""
    
    def __init__(self, product_id: str, name: str, price: Decimal, inventory_count: int = 0):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.inventory_count = inventory_count
        self.category = "general"
        self.tax_rate = Decimal('0.08')  # 8% tax rate
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': float(self.price),
            'inventory_count': self.inventory_count,
            'category': self.category,
            'tax_rate': float(self.tax_rate)
        }


class DiscountCode:
    """Discount code validation system"""
    
    def __init__(self, code: str, discount_type: str, discount_value: Decimal, 
                 expiry_date: datetime = None, usage_limit: int = None):
        self.code = code.upper()
        self.discount_type = discount_type  # 'percentage' or 'fixed'
        self.discount_value = discount_value
        self.expiry_date = expiry_date or (datetime.now() + timedelta(days=30))
        self.usage_limit = usage_limit
        self.usage_count = 0
    
    def is_valid(self) -> bool:
        """Check if discount code is valid"""
        if datetime.now() > self.expiry_date:
            return False
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
        return True
    
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        """Calculate discount amount"""
        if not self.is_valid():
            return Decimal('0')
        
        if self.discount_type == 'percentage':
            return subtotal * (self.discount_value / Decimal('100'))
        elif self.discount_type == 'fixed':
            return min(self.discount_value, subtotal)
        return Decimal('0')


class InventoryService:
    """Mock inventory service for external inventory checking"""
    
    def __init__(self):
        self.inventory = {}
        self.service_available = True
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if product is available in requested quantity"""
        if not self.service_available:
            raise ConnectionError("Inventory service unavailable")
        
        available = self.inventory.get(product_id, 0)
        return available >= quantity
    
    def reserve_inventory(self, product_id: str, quantity: int) -> bool:
        """Reserve inventory for purchase"""
        if not self.service_available:
            raise ConnectionError("Inventory service unavailable")
        
        if self.check_availability(product_id, quantity):
            self.inventory[product_id] = self.inventory.get(product_id, 0) - quantity
            return True
        return False


class ShoppingCart:
    """
    E-commerce shopping cart system
    This class needs comprehensive unit testing!
    """
    
    def __init__(self, customer_id: str = None, inventory_service: InventoryService = None):
        self.cart_id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.items = {}  # product_id -> {'product': Product, 'quantity': int}
        self.discount_codes = []
        self.inventory_service = inventory_service or InventoryService()
        self.created_at = datetime.now()
        self.tax_rate = Decimal('0.08')  # Default 8% tax
        self.max_items_per_product = 10
        self.max_total_items = 100
    
    def add_item(self, product: Product, quantity: int = 1) -> bool:
        """Add item to cart with inventory validation"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if quantity > self.max_items_per_product:
            raise ValueError(f"Cannot add more than {self.max_items_per_product} of the same item")
        
        # Check total cart size limit
        current_total = sum(item['quantity'] for item in self.items.values())
        if current_total + quantity > self.max_total_items:
            raise ValueError(f"Cart cannot contain more than {self.max_total_items} items")
        
        # Check inventory availability
        try:
            if not self.inventory_service.check_availability(product.product_id, quantity):
                raise ValueError("Insufficient inventory")
        except ConnectionError:
            # If inventory service is down, allow adding but warn
            print("Warning: Could not verify inventory")
        
        # Add or update item in cart
        if product.product_id in self.items:
            new_quantity = self.items[product.product_id]['quantity'] + quantity
            if new_quantity > self.max_items_per_product:
                raise ValueError(f"Cannot have more than {self.max_items_per_product} of the same item")
            self.items[product.product_id]['quantity'] = new_quantity
        else:
            self.items[product.product_id] = {
                'product': product,
                'quantity': quantity
            }
        
        return True
    
    def remove_item(self, product_id: str, quantity: int = None) -> bool:
        """Remove item from cart"""
        if product_id not in self.items:
            return False
        
        if quantity is None:
            # Remove all of this item
            del self.items[product_id]
        else:
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            current_quantity = self.items[product_id]['quantity']
            if quantity >= current_quantity:
                del self.items[product_id]
            else:
                self.items[product_id]['quantity'] = current_quantity - quantity
        
        return True
    
    def update_quantity(self, product_id: str, new_quantity: int) -> bool:
        """Update quantity of item in cart"""
        if product_id not in self.items:
            return False
        
        if new_quantity <= 0:
            return self.remove_item(product_id)
        
        if new_quantity > self.max_items_per_product:
            raise ValueError(f"Cannot have more than {self.max_items_per_product} of the same item")
        
        # Check inventory
        try:
            if not self.inventory_service.check_availability(product_id, new_quantity):
                raise ValueError("Insufficient inventory")
        except ConnectionError:
            print("Warning: Could not verify inventory")
        
        self.items[product_id]['quantity'] = new_quantity
        return True
    
    def clear_cart(self) -> None:
        """Remove all items from cart"""
        self.items.clear()
        self.discount_codes.clear()
    
    def get_item_count(self) -> int:
        """Get total number of items in cart"""
        return sum(item['quantity'] for item in self.items.values())
    
    def get_unique_item_count(self) -> int:
        """Get number of unique items in cart"""
        return len(self.items)
    
    def calculate_subtotal(self) -> Decimal:
        """Calculate subtotal before tax and discounts"""
        subtotal = Decimal('0')
        for item in self.items.values():
            item_total = item['product'].price * item['quantity']
            subtotal += item_total
        return subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def calculate_tax(self, subtotal: Decimal = None) -> Decimal:
        """Calculate tax amount"""
        if subtotal is None:
            subtotal = self.calculate_subtotal()
        
        tax_amount = subtotal * self.tax_rate
        return tax_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def apply_discount_code(self, discount_code: DiscountCode) -> bool:
        """Apply discount code to cart"""
        if not discount_code.is_valid():
            return False
        
        # Check if code already applied
        for existing_code in self.discount_codes:
            if existing_code.code == discount_code.code:
                return False
        
        self.discount_codes.append(discount_code)
        discount_code.usage_count += 1
        return True
    
    def remove_discount_code(self, code: str) -> bool:
        """Remove discount code from cart"""
        code = code.upper()
        for i, discount_code in enumerate(self.discount_codes):
            if discount_code.code == code:
                discount_code.usage_count -= 1
                del self.discount_codes[i]
                return True
        return False
    
    def calculate_discount_amount(self) -> Decimal:
        """Calculate total discount amount"""
        subtotal = self.calculate_subtotal()
        total_discount = Decimal('0')
        
        for discount_code in self.discount_codes:
            discount_amount = discount_code.calculate_discount(subtotal)
            total_discount += discount_amount
        
        # Ensure discount doesn't exceed subtotal
        total_discount = min(total_discount, subtotal)
        return total_discount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def calculate_total(self) -> Decimal:
        """Calculate final total including tax and discounts"""
        subtotal = self.calculate_subtotal()
        discount_amount = self.calculate_discount_amount()
        discounted_subtotal = subtotal - discount_amount
        tax_amount = self.calculate_tax(discounted_subtotal)
        total = discounted_subtotal + tax_amount
        
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def get_cart_summary(self) -> Dict[str, Any]:
        """Get detailed cart summary"""
        subtotal = self.calculate_subtotal()
        discount_amount = self.calculate_discount_amount()
        discounted_subtotal = subtotal - discount_amount
        tax_amount = self.calculate_tax(discounted_subtotal)
        total = self.calculate_total()
        
        return {
            'cart_id': self.cart_id,
            'customer_id': self.customer_id,
            'item_count': self.get_item_count(),
            'unique_items': self.get_unique_item_count(),
            'subtotal': float(subtotal),
            'discount_amount': float(discount_amount),
            'tax_amount': float(tax_amount),
            'total': float(total),
            'discount_codes': [code.code for code in self.discount_codes],
            'items': [
                {
                    'product_id': item['product'].product_id,
                    'name': item['product'].name,
                    'price': float(item['product'].price),
                    'quantity': item['quantity'],
                    'total': float(item['product'].price * item['quantity'])
                }
                for item in self.items.values()
            ]
        }
    
    def validate_cart(self) -> List[str]:
        """Validate cart and return list of issues"""
        issues = []
        
        if not self.items:
            issues.append("Cart is empty")
        
        for product_id, item in self.items.items():
            # Check inventory
            try:
                if not self.inventory_service.check_availability(product_id, item['quantity']):
                    issues.append(f"Insufficient inventory for {item['product'].name}")
            except ConnectionError:
                issues.append("Cannot verify inventory - service unavailable")
            
            # Check price validity
            if item['product'].price <= 0:
                issues.append(f"Invalid price for {item['product'].name}")
        
        # Check discount codes
        for discount_code in self.discount_codes:
            if not discount_code.is_valid():
                issues.append(f"Discount code {discount_code.code} is no longer valid")
        
        return issues
    
    def checkout(self) -> Dict[str, Any]:
        """Process checkout - reserve inventory and finalize cart"""
        validation_issues = self.validate_cart()
        if validation_issues:
            raise ValueError(f"Cart validation failed: {', '.join(validation_issues)}")
        
        # Reserve inventory
        reserved_items = []
        try:
            for product_id, item in self.items.items():
                if self.inventory_service.reserve_inventory(product_id, item['quantity']):
                    reserved_items.append(product_id)
                else:
                    # Rollback any reservations made
                    for reserved_id in reserved_items:
                        reserved_item = self.items[reserved_id]
                        self.inventory_service.inventory[reserved_id] = \
                            self.inventory_service.inventory.get(reserved_id, 0) + reserved_item['quantity']
                    raise ValueError(f"Could not reserve inventory for {item['product'].name}")
        except ConnectionError:
            raise ValueError("Checkout failed - inventory service unavailable")
        
        # Generate checkout summary
        checkout_summary = self.get_cart_summary()
        checkout_summary['checkout_time'] = datetime.now().isoformat()
        checkout_summary['status'] = 'completed'
        
        # Clear cart after successful checkout
        self.clear_cart()
        
        return checkout_summary
    
    def save_cart(self, file_path: str) -> None:
        """Save cart to JSON file"""
        cart_data = {
            'cart_id': self.cart_id,
            'customer_id': self.customer_id,
            'created_at': self.created_at.isoformat(),
            'items': {
                product_id: {
                    'product': item['product'].to_dict(),
                    'quantity': item['quantity']
                }
                for product_id, item in self.items.items()
            },
            'discount_codes': [
                {
                    'code': dc.code,
                    'discount_type': dc.discount_type,
                    'discount_value': float(dc.discount_value),
                    'expiry_date': dc.expiry_date.isoformat(),
                    'usage_limit': dc.usage_limit,
                    'usage_count': dc.usage_count
                }
                for dc in self.discount_codes
            ]
        }
        
        with open(file_path, 'w') as f:
            json.dump(cart_data, f, indent=2)
    
    @classmethod
    def load_cart(cls, file_path: str, inventory_service: InventoryService = None) -> 'ShoppingCart':
        """Load cart from JSON file"""
        with open(file_path, 'r') as f:
            cart_data = json.load(f)
        
        cart = cls(
            customer_id=cart_data['customer_id'],
            inventory_service=inventory_service
        )
        cart.cart_id = cart_data['cart_id']
        cart.created_at = datetime.fromisoformat(cart_data['created_at'])
        
        # Restore items
        for product_id, item_data in cart_data['items'].items():
            product_dict = item_data['product']
            product = Product(
                product_id=product_dict['product_id'],
                name=product_dict['name'],
                price=Decimal(str(product_dict['price'])),
                inventory_count=product_dict['inventory_count']
            )
            product.category = product_dict['category']
            product.tax_rate = Decimal(str(product_dict['tax_rate']))
            
            cart.items[product_id] = {
                'product': product,
                'quantity': item_data['quantity']
            }
        
        # Restore discount codes
        for dc_data in cart_data['discount_codes']:
            discount_code = DiscountCode(
                code=dc_data['code'],
                discount_type=dc_data['discount_type'],
                discount_value=Decimal(str(dc_data['discount_value'])),
                expiry_date=datetime.fromisoformat(dc_data['expiry_date']),
                usage_limit=dc_data['usage_limit']
            )
            discount_code.usage_count = dc_data['usage_count']
            cart.discount_codes.append(discount_code)
        
        return cart 
