from flask import Blueprint, render_template, request, jsonify
import requests

market_bp = Blueprint('market', __name__)

# API URL to fetch commodity prices
API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json"

@market_bp.route('/market-prices', methods=['GET'])
def get_market_prices():
    """Fetches and displays market prices for agricultural commodities."""
    
    # Get optional filter parameters
    state = request.args.get('state')
    district = request.args.get('district')
    commodity = request.args.get('commodity')
    
    try:
        # Fetch data from API
        response = requests.get(API_URL)
        data = response.json()
        records = data.get('records', [])

        # Filter results based on query parameters
        if state:
            records = [r for r in records if r['state'].lower() == state.lower()]
        if district:
            records = [r for r in records if r['district'].lower() == district.lower()]
        if commodity:
            records = [r for r in records if r['commodity'].lower() == commodity.lower()]

        # Get unique filter values for state, district, and commodity
        states = list(set(r['state'] for r in records))
        districts = list(set(r['district'] for r in records))
        commodities = list(set(r['commodity'] for r in records))

        # Render the HTML page with the fetched data and filter options
        return render_template(
            "market.html", 
            market_data=records, 
            states=states, 
            districts=districts, 
            commodities=commodities
        )
    
    except Exception as e:
        return render_template("market.html", market_data=[], error=str(e))
