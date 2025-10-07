from flask import Blueprint, request, jsonify
from services.chatbot_service import ChatbotService

chat_bp = Blueprint('chat', __name__)
chatbot = ChatbotService()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Request body: {
        "user_id": "USER123",
        "message": "How to grow rice?"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400
        
        user_id = data.get('user_id', 'default_user')
        message = data.get('message')
        
        if not message.strip():
            return jsonify({
                "success": False,
                "error": "Message cannot be empty"
            }), 400
        
        # Process chat
        result = chatbot.chat(user_id, message)
        
        return jsonify(result), 200 if result['success'] else 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/clear-history', methods=['POST'])
def clear_history():
    """
    Clear conversation history
    Request body: {
        "user_id": "USER123"
    }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        
        result = chatbot.clear_history(user_id)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "message": "Chatbot service is running",
        "status": "healthy"
    }), 200


@chat_bp.route('/crops', methods=['GET'])
def get_crops():
    """Get all available crops"""
    try:
        crops = chatbot.ag_data.get_all_crops()
        return jsonify({
            "success": True,
            "crops": crops,
            "count": len(crops)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/crop/<crop_name>', methods=['GET'])
def get_crop_details(crop_name):
    """
    Get detailed information about a specific crop
    URL: /api/crop/rice
    """
    try:
        crop = chatbot.ag_data.get_crop_by_name(crop_name)
        
        if not crop:
            return jsonify({
                "success": False,
                "error": f"Crop '{crop_name}' not found"
            }), 404
        
        return jsonify({
            "success": True,
            "crop": crop
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/search-crops', methods=['GET'])
def search_crops():
    """
    Search crops by query parameter
    URL: /api/search-crops?q=kharif
    """
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Search query 'q' parameter is required"
            }), 400
        
        results = chatbot.ag_data.search_crops(query)
        
        return jsonify({
            "success": True,
            "results": results,
            "count": len(results),
            "query": query
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get order details by order ID
    URL: /api/order/ORD001
    """
    try:
        order = chatbot.ag_data.get_order_by_id(order_id)
        
        if not order:
            return jsonify({
                "success": False,
                "error": f"Order '{order_id}' not found"
            }), 404
        
        return jsonify({
            "success": True,
            "order": order
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/user-orders/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    """
    Get all orders for a specific user
    URL: /api/user-orders/USER123
    """
    try:
        orders = chatbot.ag_data.get_user_orders(user_id)
        
        return jsonify({
            "success": True,
            "orders": orders,
            "count": len(orders),
            "user_id": user_id
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/conversation-history/<user_id>', methods=['GET'])
def get_conversation_history(user_id):
    """
    Get conversation history for a user
    URL: /api/conversation-history/USER123
    """
    try:
        history = chatbot.conversation_history.get(user_id, [])
        
        return jsonify({
            "success": True,
            "history": history,
            "message_count": len(history),
            "user_id": user_id
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route('/quick-questions', methods=['GET'])
def quick_questions():
    """
    Get suggested quick questions for users
    URL: /api/quick-questions
    """
    questions = [
        "How to grow rice?",
        "What is the best fertilizer for wheat?",
        "How to control pests in tomato?",
        "What is crop rotation?",
        "How to improve soil health?",
        "Best irrigation method for cotton?",
        "When to harvest sugarcane?",
        "What is organic farming?",
        "Track my order ORD001",
        "How to increase crop yield?"
    ]
    
    return jsonify({
        "success": True,
        "questions": questions
    }), 200


@chat_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get chatbot statistics
    URL: /api/statistics
    """
    try:
        total_users = len(chatbot.conversation_history)
        total_conversations = sum(len(history) for history in chatbot.conversation_history.values())
        total_crops = len(chatbot.ag_data.get_all_crops())
        total_orders = len(chatbot.ag_data.orders_data.get('orders', []))
        
        return jsonify({
            "success": True,
            "statistics": {
                "total_users": total_users,
                "total_messages": total_conversations,
                "total_crops_database": total_crops,
                "total_orders": total_orders
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500