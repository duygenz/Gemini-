import os
import google.generativeai as genai
from flask import Flask, request, jsonify

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Lấy API key từ biến môi trường của Render
# Đây là cách an toàn để quản lý key của bạn
try:
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=gemini_api_key)
except ValueError as e:
    # In ra lỗi nếu không tìm thấy key để dễ dàng debug trên Render
    print(f"Error: {e}")


# Tạo model Gemini
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/generate', methods=['POST'])
def generate_content():
    """
    Endpoint nhận prompt và trả về nội dung từ Gemini.
    """
    # Lấy dữ liệu JSON từ request
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided in the request body"}), 400

    try:
        # Gọi Gemini API
        response = model.generate_content(prompt)
        
        # Trả về kết quả dưới dạng JSON
        return jsonify({"response": response.text})

    except Exception as e:
        # Trả về lỗi nếu có vấn đề xảy ra
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy ứng dụng trên cổng do Render cung cấp
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
