#!/usr/bin/env python3
"""
Inventory service for checking product availability
This simulates an external inventory management system
"""

import json
import random
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from product import SAMPLE_PRODUCTS


class InventoryService:
    """External inventory service for product availability checking"""
    
    def __init__(self, service_available: bool = True, response_delay: float = 0.1):
        self.inventory: Dict[str, int] = {}
        self.reserved_inventory: Dict[str, int] = {}  # Reserved but not yet purchased
        self.service_available = service_available
        self.response_delay = response_delay  # Simulate network delay
        self.failure_rate = 0.0  # Simulate random failures (0.0 = never fail, 1.0 = always fail)
        self.last_update = datetime.now()
        self.update_log: List[Dict] = []
        
        # Initialize with sample inventory
        self.load_sample_inventory()
    
    def _simulate_network_delay(self):
        """Simulate network response delay"""
        if self.response_delay > 0:
            time.sleep(self.response_delay)
    
    def _check_service_available(self):
        """Check if service is available and simulate random failures"""
        if not self.service_available:
            raise ConnectionError("Inventory service unavailable")
        
        if random.random() < self.failure_rate:
            raise ConnectionError("Inventory service temporary failure")
    
    def load_sample_inventory(self):
        """Load sample inventory data"""
        for product_id, product in SAMPLE_PRODUCTS.items():
            self.inventory[product_id] = product.inventory_count
        
        # Add some additional test products
        self.inventory.update({
            'OUT_OF_STOCK': 0,
            'LOW_STOCK': 2,
            'HIGH_STOCK': 1000,
            'RESERVED_ITEM': 10
        })
        
        # Reserve some items to test reservation logic
        self.reserved_inventory['RESERVED_ITEM'] = 5
    
    def check_availability(self, product_id: str, quantity: int = 1) -> bool:
        """Check if product is available in requested quantity"""
        self._simulate_network_delay()
        self._check_service_available()
        
        if product_id not in self.inventory:
            return False
        
        available = self.inventory[product_id] - self.reserved_inventory.get(product_id, 0)
        return available >= quantity
    
    def get_available_quantity(self, product_id: str) -> int:
        """Get available quantity for a product"""
        self._simulate_network_delay()
        self._check_service_available()
        
        if product_id not in self.inventory:
            return 0
        
        return max(0, self.inventory[product_id] - self.reserved_inventory.get(product_id, 0))
    
    def reserve_inventory(self, product_id: str, quantity: int) -> bool:
        """Reserve inventory for purchase"""
        self._simulate_network_delay()
        self._check_service_available()
        
        if not self.check_availability(product_id, quantity):
            return False
        
        # Reserve the inventory
        if product_id not in self.reserved_inventory:
            self.reserved_inventory[product_id] = 0
        
        self.reserved_inventory[product_id] += quantity
        
        # Log the reservation
        self.update_log.append({
            'action': 'reserve',
            'product_id': product_id,
            'quantity': quantity,
            'timestamp': datetime.now().isoformat()
        })
        
        return True
    
    def release_reservation(self, product_id: str, quantity: int) -> bool:
        """Release reserved inventory"""
        self._simulate_network_delay()
        self._check_service_available()
        
        if product_id not in self.reserved_inventory:
            return False
        
        current_reserved = self.reserved_inventory[product_id]
        if current_reserved < quantity:
            return False
        
        self.reserved_inventory[product_id] = max(0, current_reserved - quantity)
        
        # Clean up if no more reserved
        if self.reserved_inventory[product_id] == 0:
            del self.reserved_inventory[product_id]
        
        # Log the release
        self.update_log.append({
            'action': 'release',
            'product_id': product_id,
            'quantity': quantity,
            'timestamp': datetime.now().isoformat()
        })
        
        return True
    
    def confirm_purchase(self, product_id: str, quantity: int) -> bool:
        """Confirm purchase and reduce actual inventory"""
        self._simulate_network_delay()
        self._check_service_available()
        
        # Check if we have enough reserved inventory
        if product_id not in self.reserved_inventory:
            return False
        
        if self.reserved_inventory[product_id] < quantity:
            return False
        
        # Reduce actual inventory
        self.inventory[product_id] -= quantity
        
        # Reduce reserved inventory
        self.reserved_inventory[product_id] -= quantity
        if self.reserved_inventory[product_id] == 0:
            del self.reserved_inventory[product_id]
        
        # Log the purchase
        self.update_log.append({
            'action': 'purchase',
            'product_id': product_id,
            'quantity': quantity,
            'timestamp': datetime.now().isoformat()
        })
        
        self.last_update = datetime.now()
        return True
    
    def restock_product(self, product_id: str, quantity: int) -> bool:
        """Restock product inventory"""
        self._simulate_network_delay()
        self._check_service_available()
        
        if product_id not in self.inventory:
            self.inventory[product_id] = 0
        
        self.inventory[product_id] += quantity
        
        # Log the restock
        self.update_log.append({
            'action': 'restock',
            'product_id': product_id,
            'quantity': quantity,
            'timestamp': datetime.now().isoformat()
        })
        
        self.last_update = datetime.now()
        return True
    
    def get_inventory_status(self) -> Dict[str, Dict]:
        """Get full inventory status"""
        self._simulate_network_delay()
        self._check_service_available()
        
        status = {}
        for product_id in self.inventory:
            total = self.inventory[product_id]
            reserved = self.reserved_inventory.get(product_id, 0)
            available = total - reserved
            
            status[product_id] = {
                'total': total,
                'reserved': reserved,
                'available': available,
                'last_updated': self.last_update.isoformat()
            }
        
        return status
    
    def get_low_stock_items(self, threshold: int = 5) -> List[str]:
        """Get list of products with low stock"""
        self._simulate_network_delay()
        self._check_service_available()
        
        low_stock = []
        for product_id, quantity in self.inventory.items():
            available = quantity - self.reserved_inventory.get(product_id, 0)
            if 0 < available <= threshold:
                low_stock.append(product_id)
        
        return low_stock
    
    def get_out_of_stock_items(self) -> List[str]:
        """Get list of out of stock products"""
        self._simulate_network_delay() 
        self._check_service_available()
        
        out_of_stock = []
        for product_id, quantity in self.inventory.items():
            available = quantity - self.reserved_inventory.get(product_id, 0)
            if available <= 0:
                out_of_stock.append(product_id)
        
        return out_of_stock
    
    def bulk_check_availability(self, items: List[Tuple[str, int]]) -> Dict[str, bool]:
        """Check availability for multiple items at once"""
        self._simulate_network_delay()
        self._check_service_available()
        
        results = {}
        for product_id, quantity in items:
            results[product_id] = self.check_availability(product_id, quantity)
        
        return results
    
    def get_update_log(self, since: datetime = None) -> List[Dict]:
        """Get inventory update log"""
        if since is None:
            return self.update_log.copy()
        
        since_iso = since.isoformat()
        return [
            entry for entry in self.update_log 
            if entry['timestamp'] >= since_iso
        ]
    
    def clear_update_log(self):
        """Clear the update log"""
        self.update_log.clear()
    
    def set_failure_rate(self, rate: float):
        """Set the service failure rate for testing"""
        self.failure_rate = max(0.0, min(1.0, rate))
    
    def set_service_available(self, available: bool):
        """Set service availability for testing"""
        self.service_available = available
    
    def reset_inventory(self):
        """Reset inventory to initial state"""
        self.inventory.clear()
        self.reserved_inventory.clear()
        self.update_log.clear()
        self.load_sample_inventory()
        self.last_update = datetime.now()
    
    def save_inventory_state(self, file_path: str):
        """Save current inventory state to file"""
        state = {
            'inventory': self.inventory,
            'reserved_inventory': self.reserved_inventory,
            'last_update': self.last_update.isoformat(),
            'update_log': self.update_log
        }
        
        with open(file_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_inventory_state(self, file_path: str):
        """Load inventory state from file"""
        try:
            with open(file_path, 'r') as f:
                state = json.load(f)
            
            self.inventory = state['inventory']
            self.reserved_inventory = state['reserved_inventory']
            self.last_update = datetime.fromisoformat(state['last_update'])
            self.update_log = state['update_log']
            
        except FileNotFoundError:
            # If file doesn't exist, use defaults
            self.load_sample_inventory()


class MockInventoryService(InventoryService):
    """Mock inventory service for testing purposes"""
    
    def __init__(self, always_available: bool = True, always_unavailable: bool = False):
        super().__init__(service_available=True, response_delay=0)
        self.always_available = always_available
        self.always_unavailable = always_unavailable
        self.call_log: List[Dict] = []
    
    def check_availability(self, product_id: str, quantity: int = 1) -> bool:
        """Mock availability check"""
        self.call_log.append({
            'method': 'check_availability',
            'product_id': product_id,
            'quantity': quantity,
            'timestamp': datetime.now().isoformat()
        })
        
        if self.always_unavailable:
            return False
        if self.always_available:
            return True
        
        # Use parent logic
        return super().check_availability(product_id, quantity)
    
    def reserve_inventory(self, product_id: str, quantity: int) -> bool:
        """Mock inventory reservation"""
        self.call_log.append({
            'method': 'reserve_inventory',
            'product_id': product_id,
            'quantity': quantity,
            'timestamp': datetime.now().isoformat()
        })
        
        if self.always_unavailable:
            return False
        if self.always_available:
            return True
        
        return super().reserve_inventory(product_id, quantity)
    
    def get_call_log(self) -> List[Dict]:
        """Get log of method calls for testing"""
        return self.call_log.copy()
    
    def clear_call_log(self):
        """Clear the call log"""
        self.call_log.clear()


# Create default inventory service instance
inventory_service = InventoryService() 
