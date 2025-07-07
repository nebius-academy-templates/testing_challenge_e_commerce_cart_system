#!/usr/bin/env python3
"""
Discount code validation system for the e-commerce cart
"""

from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class DiscountCode:
    """Discount code validation system"""
    
    def __init__(self, code: str, discount_type: str, discount_value: Decimal, 
                 expiry_date: datetime = None, usage_limit: int = None, 
                 minimum_purchase: Decimal = None, category_restriction: str = None):
        self.code = code.upper()
        self.discount_type = discount_type  # 'percentage' or 'fixed'
        self.discount_value = discount_value
        self.expiry_date = expiry_date or (datetime.now() + timedelta(days=30))
        self.usage_limit = usage_limit
        self.usage_count = 0
        self.minimum_purchase = minimum_purchase or Decimal('0')
        self.category_restriction = category_restriction  # None means all categories
        self.is_active = True
        self.created_date = datetime.now()
    
    def __str__(self):
        return f"DiscountCode({self.code}: {self.discount_type} {self.discount_value})"
    
    def __repr__(self):
        return f"DiscountCode(code='{self.code}', discount_type='{self.discount_type}', discount_value={self.discount_value})"
    
    def is_valid(self) -> bool:
        """Check if discount code is valid"""
        if not self.is_active:
            return False
        if datetime.now() > self.expiry_date:
            return False
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
        return True
    
    def can_apply_to_cart(self, cart_subtotal: Decimal, cart_categories: List[str] = None) -> bool:
        """Check if discount can be applied to the cart"""
        if not self.is_valid():
            return False
        
        # Check minimum purchase requirement
        if cart_subtotal < self.minimum_purchase:
            return False
        
        # Check category restriction
        if self.category_restriction and cart_categories:
            if self.category_restriction not in cart_categories:
                return False
        
        return True
    
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        """Calculate discount amount"""
        if not self.is_valid():
            return Decimal('0')
        
        if self.discount_type == 'percentage':
            discount = subtotal * (self.discount_value / Decimal('100'))
        elif self.discount_type == 'fixed':
            discount = min(self.discount_value, subtotal)
        else:
            discount = Decimal('0')
        
        return discount
    
    def apply_discount(self) -> bool:
        """Apply the discount (increment usage count)"""
        if not self.is_valid():
            return False
        
        self.usage_count += 1
        return True
    
    def remove_discount(self) -> bool:
        """Remove the discount (decrement usage count)"""
        if self.usage_count > 0:
            self.usage_count -= 1
            return True
        return False
    
    def get_validation_errors(self, cart_subtotal: Decimal = None, cart_categories: List[str] = None) -> List[str]:
        """Get list of validation errors preventing discount application"""
        errors = []
        
        if not self.is_active:
            errors.append("Discount code is not active")
        
        if datetime.now() > self.expiry_date:
            errors.append("Discount code has expired")
        
        if self.usage_limit and self.usage_count >= self.usage_limit:
            errors.append("Discount code usage limit reached")
        
        if cart_subtotal is not None and cart_subtotal < self.minimum_purchase:
            errors.append(f"Minimum purchase of ${self.minimum_purchase} required")
        
        if self.category_restriction and cart_categories is not None:
            if self.category_restriction not in cart_categories:
                errors.append(f"Discount only applies to {self.category_restriction} category")
        
        return errors
    
    def to_dict(self) -> Dict:
        """Convert discount code to dictionary"""
        return {
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_value': float(self.discount_value),
            'expiry_date': self.expiry_date.isoformat(),
            'usage_limit': self.usage_limit,
            'usage_count': self.usage_count,
            'minimum_purchase': float(self.minimum_purchase),
            'category_restriction': self.category_restriction,
            'is_active': self.is_active,
            'created_date': self.created_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DiscountCode':
        """Create discount code from dictionary"""
        discount_code = cls(
            code=data['code'],
            discount_type=data['discount_type'],
            discount_value=Decimal(str(data['discount_value'])),
            expiry_date=datetime.fromisoformat(data['expiry_date']),
            usage_limit=data.get('usage_limit'),
            minimum_purchase=Decimal(str(data.get('minimum_purchase', '0'))),
            category_restriction=data.get('category_restriction')
        )
        discount_code.usage_count = data.get('usage_count', 0)
        discount_code.is_active = data.get('is_active', True)
        discount_code.created_date = datetime.fromisoformat(data.get('created_date', datetime.now().isoformat()))
        return discount_code


class DiscountManager:
    """Manages multiple discount codes"""
    
    def __init__(self):
        self.discount_codes: Dict[str, DiscountCode] = {}
        self.load_default_codes()
    
    def add_discount_code(self, discount_code: DiscountCode) -> bool:
        """Add a new discount code"""
        if discount_code.code in self.discount_codes:
            return False
        self.discount_codes[discount_code.code] = discount_code
        return True
    
    def get_discount_code(self, code: str) -> Optional[DiscountCode]:
        """Get discount code by code"""
        return self.discount_codes.get(code.upper())
    
    def validate_discount_code(self, code: str, cart_subtotal: Decimal = None, 
                             cart_categories: List[str] = None) -> tuple[bool, List[str]]:
        """Validate discount code and return errors if any"""
        discount_code = self.get_discount_code(code)
        if not discount_code:
            return False, ["Invalid discount code"]
        
        errors = discount_code.get_validation_errors(cart_subtotal, cart_categories)
        return len(errors) == 0, errors
    
    def apply_discount_code(self, code: str, cart_subtotal: Decimal, 
                          cart_categories: List[str] = None) -> tuple[bool, Decimal, List[str]]:
        """Apply discount code and return success, discount amount, and any errors"""
        is_valid, errors = self.validate_discount_code(code, cart_subtotal, cart_categories)
        if not is_valid:
            return False, Decimal('0'), errors
        
        discount_code = self.get_discount_code(code)
        if discount_code.can_apply_to_cart(cart_subtotal, cart_categories):
            discount_amount = discount_code.calculate_discount(cart_subtotal)
            discount_code.apply_discount()
            return True, discount_amount, []
        else:
            return False, Decimal('0'), ["Discount cannot be applied to this cart"]
    
    def get_active_codes(self) -> List[DiscountCode]:
        """Get all active discount codes"""
        return [code for code in self.discount_codes.values() if code.is_valid()]
    
    def get_expired_codes(self) -> List[DiscountCode]:
        """Get all expired discount codes"""
        return [code for code in self.discount_codes.values() if not code.is_valid()]
    
    def cleanup_expired_codes(self) -> int:
        """Remove expired codes and return count of removed codes"""
        expired_codes = [code.code for code in self.get_expired_codes()]
        for code in expired_codes:
            del self.discount_codes[code]
        return len(expired_codes)
    
    def load_default_codes(self):
        """Load some default discount codes for testing"""
        # Valid codes
        self.add_discount_code(DiscountCode(
            code='SAVE10',
            discount_type='percentage',
            discount_value=Decimal('10'),
            expiry_date=datetime.now() + timedelta(days=30),
            usage_limit=100
        ))
        
        self.add_discount_code(DiscountCode(
            code='WELCOME20',
            discount_type='percentage',
            discount_value=Decimal('20'),
            expiry_date=datetime.now() + timedelta(days=60),
            minimum_purchase=Decimal('50'),
            usage_limit=50
        ))
        
        self.add_discount_code(DiscountCode(
            code='FIXED25',
            discount_type='fixed',
            discount_value=Decimal('25'),
            expiry_date=datetime.now() + timedelta(days=45),
            minimum_purchase=Decimal('100')
        ))
        
        self.add_discount_code(DiscountCode(
            code='ELECTRONICS15',
            discount_type='percentage',
            discount_value=Decimal('15'),
            expiry_date=datetime.now() + timedelta(days=30),
            category_restriction='electronics',
            usage_limit=200
        ))
        
        # Expired code for testing
        self.add_discount_code(DiscountCode(
            code='EXPIRED10',
            discount_type='percentage',
            discount_value=Decimal('10'),
            expiry_date=datetime.now() - timedelta(days=1),
            usage_limit=10
        ))
        
        # Used up code for testing
        used_up_code = DiscountCode(
            code='USEDUP5',
            discount_type='percentage',
            discount_value=Decimal('5'),
            expiry_date=datetime.now() + timedelta(days=30),
            usage_limit=1
        )
        used_up_code.usage_count = 1  # Already used up
        self.add_discount_code(used_up_code)
    
    def save_to_file(self, file_path: str):
        """Save discount codes to JSON file"""
        data = {
            'discount_codes': [code.to_dict() for code in self.discount_codes.values()]
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, file_path: str):
        """Load discount codes from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.discount_codes.clear()
            for code_data in data['discount_codes']:
                discount_code = DiscountCode.from_dict(code_data)
                self.discount_codes[discount_code.code] = discount_code
        except FileNotFoundError:
            # If file doesn't exist, keep default codes
            pass


# Global discount manager instance
discount_manager = DiscountManager() 
