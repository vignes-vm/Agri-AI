class AgricultureKnowledgeBase:
    """
    Agriculture knowledge base for common farming questions
    """
    
    def __init__(self):
        self.knowledge = {
            "organic_farming": """
Organic farming is an agricultural method that avoids synthetic chemicals. Key practices:
- Use natural fertilizers like compost, vermicompost, and green manure
- Biological pest control using beneficial insects
- Crop rotation to maintain soil health
- No synthetic pesticides or GMO seeds
- Focus on sustainable and eco-friendly methods
            """,
            
            "soil_health": """
Healthy soil is crucial for good crop yield:
- Test soil pH regularly (most crops prefer 6.0-7.5)
- Add organic matter to improve structure
- Practice crop rotation
- Avoid over-tilling
- Maintain proper drainage
- Use cover crops to prevent erosion
            """,
            
            "irrigation": """
Efficient irrigation methods:
1. Drip irrigation - saves 30-70% water
2. Sprinkler irrigation - suitable for large fields
3. Furrow irrigation - traditional method
4. Subsurface irrigation - water applied below surface

Best practices:
- Irrigate early morning or evening
- Monitor soil moisture
- Avoid overwatering
            """,
            
            "pest_management": """
Integrated Pest Management (IPM):
- Regular field monitoring
- Use pest-resistant varieties
- Biological control (natural predators)
- Cultural practices (crop rotation, sanitation)
- Mechanical control (traps, barriers)
- Chemical control as last resort

Natural pesticides:
- Neem oil
- Garlic spray
- Chilli pepper spray
            """,
            
            "fertilizers": """
Main fertilizer types:
1. Nitrogen (N) - leaf growth
2. Phosphorus (P) - root development
3. Potassium (K) - overall plant health

Organic options:
- Compost
- Vermicompost
- Green manure
- Bone meal
- Farmyard manure (FYM)

Apply based on soil test results and crop requirements.
            """,
            
            "crop_rotation": """
Crop rotation benefits:
- Breaks pest and disease cycles
- Improves soil fertility
- Reduces weed pressure
- Better nutrient management

Example rotation:
Year 1: Legumes (adds nitrogen)
Year 2: Leafy vegetables (uses nitrogen)
Year 3: Root crops
Year 4: Fruiting crops
            """,
            
            "harvest_storage": """
Proper harvesting and storage:

Harvesting:
- Harvest at right maturity stage
- Use clean, sharp tools
- Avoid damage to produce
- Harvest in cool hours

Storage:
- Clean and dry produce
- Maintain proper temperature and humidity
- Good ventilation
- Regular inspection for spoilage
- Use appropriate containers
            """,
            
            "weather_farming": """
Weather considerations:
- Monitor weather forecasts
- Plan sowing based on monsoon
- Protect crops from extreme weather
- Use mulching to retain moisture
- Install shade nets for heat protection
- Drainage systems for heavy rainfall
- Greenhouse for controlled environment
            """
        }
    
    def get_agriculture_context(self):
        """Get general agriculture context for the chatbot"""
        context = """
You are an expert agriculture assistant helping farmers with:
- Crop cultivation guidance
- Pest and disease management
- Soil health and fertilization
- Irrigation techniques
- Organic farming practices
- Order tracking and product information
- Yield optimization strategies
- Weather and seasonal advice

Always provide practical, actionable advice suitable for farmers.
Use simple language and include local context when relevant.
        """
        return context
    
    def search_knowledge(self, query):
        """Search knowledge base for relevant information"""
        query_lower = query.lower()
        relevant_info = []
        
        keywords_map = {
            "organic": "organic_farming",
            "soil": "soil_health",
            "irrigation": "irrigation",
            "water": "irrigation",
            "pest": "pest_management",
            "disease": "pest_management",
            "fertilizer": "fertilizers",
            "manure": "fertilizers",
            "rotation": "crop_rotation",
            "harvest": "harvest_storage",
            "storage": "harvest_storage",
            "weather": "weather_farming",
            "climate": "weather_farming"
        }
        
        for keyword, topic in keywords_map.items():
            if keyword in query_lower and topic not in relevant_info:
                relevant_info.append(self.knowledge[topic])
        
        return "\n\n".join(relevant_info) if relevant_info else ""