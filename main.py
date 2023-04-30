from waitress import serve
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

my_secret = '82911c729emsh04ca3274c4c5073p1ddc39jsne8ff2bf61f64'


def generate_qr_code(QR_TEXT, EYE_STYLE, QR_SIZE, QR_FG_COLOR, QR_BG_COLOR):
  url = "https://qrcode-supercharged.p.rapidapi.com/"

  querystring = {
    "text": f"{QR_TEXT}",
    "eye_style": f"{EYE_STYLE}",
    "size": f"{QR_SIZE}",
    "fg_color": f"{QR_FG_COLOR}",
    "bg_color": f"{QR_BG_COLOR}",
    "validate": 0
  }
  print(querystring, flush=True)
  headers = {
    "content-type": "application/octet-stream",
    "X-RapidAPI-Key": f"{my_secret}",
    "X-RapidAPI-Host": "qrcode-supercharged.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers, params=querystring)
  result = response.text
  print(result)
  return (result)


@app.route('/generate', methods=['GET'])
def gen_qr_code():
  QR_TEXT = request.args.get('QR_TEXT')
  QR_SIZE = request.args.get('QR_SIZE')
  EYE_STYLE = request.args.get('EYE_STYLE')
  QR_FG_COLOR = request.args.get('QR_FG_COLOR')
  QR_BG_COLOR = request.args.get('QR_BG_COLOR')

  try:
    QRCode = generate_qr_code(QR_TEXT, EYE_STYLE, QR_SIZE, QR_FG_COLOR,
                              QR_BG_COLOR)
    return QRCode
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)
