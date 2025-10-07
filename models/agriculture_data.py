import json
import os

class AgricultureData:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.crops_data = self.load_crops()
        self.orders_data = self.load_orders()
    
    def load_crops(self):
        """Load crop data from JSON file"""
        try:
            crops_file = os.path.join(self.data_dir, 'crops.json')
            with open(crops_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("crops.json not found. Using empty data.")
            return {"crops": []}
    
    def load_orders(self):
        """Load order data from JSON file"""
        try:
            orders_file = os.path.join(self.data_dir, 'orders.json')
            with open(orders_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("orders.json not found. Using empty data.")
            return {"orders": [], "orderStatuses": {}}
    
    def get_crop_by_name(self, crop_name):
        """Find crop by name (case-insensitive)"""
        crop_name_lower = crop_name.lower()
        for crop in self.crops_data.get('crops', []):
            if crop['name'].lower() == crop_name_lower:
                return crop
        return None
    
    def search_crops(self, query):
        """Search crops by name, season, or soil type"""
        query_lower = query.lower()
        results = []
        for crop in self.crops_data.get('crops', []):
            if (query_lower in crop['name'].lower() or 
                query_lower in crop['season'].lower() or
                query_lower in crop['soilType'].lower()):
                results.append(crop)
        return results
    
    def get_order_by_id(self, order_id):
        """Find order by ID"""
        for order in self.orders_data.get('orders', []):
            if order['orderId'] == order_id:
                return order
        return None
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        return [order for order in self.orders_data.get('orders', []) 
                if order['userId'] == user_id]
    
    def get_all_crops(self):
        """Get list of all crop names"""
        return [crop['name'] for crop in self.crops_data.get('crops', [])]
    
    def format_crop_info(self, crop):
        """Format crop information for chatbot response"""
        if not crop:
            return "Crop information not found."
        
        info = f"**{crop['name']}** ({crop['scientificName']})\n\n"
        info += f"🌱 **Season:** {crop['season']}\n"
        info += f"🌡️ **Temperature:** {crop['temperature']}\n"
        info += f"💧 **Rainfall:** {crop['rainfall']}\n"
        info += f"⏱️ **Duration:** {crop['duration']}\n"
        info += f"📊 **Expected Yield:** {crop['yield']}\n\n"
        
        info += f"🌾 **Soil Type:** {crop['soilType']}\n"
        info += f"☀️ **Climate:** {crop['climate']}\n\n"
        
        info += "**Cultivation Steps:**\n"
        for i, step in enumerate(crop['cultivation'], 1):
            info += f"{i}. {step}\n"
        
        return info
    
    def format_order_info(self, order):
        """Format order information for chatbot response"""
        if not order:
            return "Order not found."
        
        info = f"**Order #{order['orderId']}**\n\n"
        info += f"📦 **Product:** {order['productName']}\n"
        info += f"📊 **Quantity:** {order['quantity']}\n"
        info += f"💰 **Price:** ₹{order['price']}\n"
        info += f"📅 **Order Date:** {order['orderDate']}\n"
        info += f"🚚 **Status:** {order['status']}\n"
        
        if order['status'] == 'Delivered':
            info += f"✅ **Delivered on:** {order['deliveryDate']}\n"
        elif 'expectedDelivery' in order:
            info += f"📍 **Expected Delivery:** {order['expectedDelivery']}\n"
        
        return info