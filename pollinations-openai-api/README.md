# Pollinations OpenAI-Compatible API Wrapper

A lightweight Python wrapper that simulates the OpenAI Image Generation API (`/v1/images/generations`) but uses the free Pollinations.ai engine.

## 🚀 Features
- Fully compatible with OpenAI-compatible image API clients.
- Supports custom sizes and multiple image generation (via random seeds).
- Zero cost, zero API keys required.

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pollinations-openai-api.git
   cd pollinations-openai-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python main.py
   ```

## ⚙️ Configuration
- **API Base URL:** `http://localhost:8000`
- **API Key:** Not required (any string works)
- **Model:** Any string (e.g., `pollinations`)

## 📄 License
MIT