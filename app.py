from flask import Flask, jsonify
from flask_cors import CORS
import requests
import logging
import os

app = Flask(__name__)
CORS(app)  # Cho phép truy cập từ domain khác

# Cấu hình log
logging.basicConfig(level=logging.INFO)

@app.route('/get_tickers')
def get_tickers():
    logging.info("Nhận request /get_tickers")
    try:
        url = "https://api-gateway.onus.io/v2/exchange/public/spot/tickers"
        logging.info(f"Đang gọi API: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Báo lỗi nếu API trả lỗi
        data = response.json()
        logging.info("Lấy dữ liệu thành công")
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi request: {e}")
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        logging.error(f"Lỗi không xác định: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render tự cấp PORT
    app.run(host='0.0.0.0', port=port)
