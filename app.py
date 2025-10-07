from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.chat_routes import chat_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS for Android app integration
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set OPENAI_API_KEY in .env file")
        return None
    
    # Register blueprints (routes)
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    # Root endpoint
    @app.route('/')
    def home():
        return jsonify({
            "message": "Agriculture Chatbot API",
            "version": "1.0",
            "status": "running",
            "endpoints": {
                "chat": "/api/chat (POST)",
                "clear_history": "/api/clear-history (POST)",
                "health": "/api/health (GET)",
                "crops": "/api/crops (GET)"
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint not found"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    if app:
        print("=" * 50)
        print("🌾 Agriculture Chatbot Server Starting...")
        print("=" * 50)
        print(f"Server running on: http://localhost:{Config.PORT}")
        print(f"Health check: http://localhost:{Config.PORT}/api/health")
        print(f"Chat endpoint: http://localhost:{Config.PORT}/api/chat")
        print("=" * 50)
        app.run(
            host='0.0.0.0',
            port=Config.PORT,
            debug=Config.DEBUG
        )
    else:
        print("Failed to start application. Check configuration.")