from flask import Flask
from cars_bp import cars_bp

app = Flask(__name__)

# BLUEPRINT
app.register_blueprint(cars_bp)

if __name__ == "__main__":
    app.run(debug=True)