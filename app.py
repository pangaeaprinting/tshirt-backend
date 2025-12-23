from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get-quote', methods=['POST'])
def calculate():
    data = request.json
    qty = int(data.get('quantity', 1))
    
    # 1. Analyze the Front Design
    front_design = data.get('front_design', {})
    # Fabric.js adds the base shirt as an object, so we look for more than 1 object
    has_front = len(front_design.get('objects', [])) > 1 if front_design else False
    
    # 2. Analyze the Back Design
    back_design = data.get('back_design', {})
    has_back = len(back_design.get('objects', [])) > 1 if back_design else False

    # 3. Pricing Logic
    base_price = 20.00
    side_fee = 0
    
    if has_front and has_back:
        side_fee = 10.00  # $10 extra for double-sided
    elif has_front or has_back:
        side_fee = 5.00   # $5 for single-sided
        
    total = (base_price + side_fee) * qty
    
    return jsonify({
        "price": f"${total:.2f}",
        "details": {
            "front": "Yes" if has_front else "No",
            "back": "Yes" if has_back else "No",
            "quantity": qty
        },
        "message": "Quote calculated for " + ("double-sided" if has_front and has_back else "single-sided") + " design."
    })

if __name__ == "__main__":
    app.run()
