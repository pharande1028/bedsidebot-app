from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>BedsideBot - Live!</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: #f0f8ff;">
        <h1 style="color: #28a745;">🏥 BedsideBot is Live!</h1>
        <p style="font-size: 20px;">Your patient monitoring system is successfully deployed!</p>
        <p>✅ Status: <strong>Online and Ready</strong></p>
        <p>🌐 Access from any device with internet connection</p>
        <p>📱 Share this URL with your team</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting BedsideBot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)