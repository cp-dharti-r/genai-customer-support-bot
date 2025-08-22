# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+ (tested with Python 3.13)
- At least one LLM API key (OpenAI or Google Gemini)

## 🏃‍♂️ Get Started in 3 Steps

### 1. Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy environment template
cp env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Required: At least one of these API keys:**
```env
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here
```

### 3. Run the Application
```bash
# Start the server
python main.py
```

**Access the application:**
- 🌐 **Chat Interface**: http://localhost:8000/
- 📖 **API Docs**: http://localhost:8000/docs
- 🔍 **Health Check**: http://localhost:8000/api/health

## 🎯 What You Can Do

1. **Select an LLM Provider** from OpenAI GPT or Google Gemini
2. **Ask customer support questions** and get AI-powered responses
3. **Rate responses** on a 1-5 scale with optional feedback
4. **View analytics** comparing the two LLM providers
5. **Browse conversation history** and ratings

## 🔧 Troubleshooting

### No API Keys Configured
- Ensure at least one API key is set in `.env`
- Check that the API key is valid and has sufficient credits

### Port Already in Use
- Change the port in `.env`: `PORT=8001`
- Or kill the process using port 8000

### Database Issues
- Delete `customer_support_bot.db` and restart
- The application will recreate the database automatically

## 📱 Sample Questions to Try

- "What payment methods do you accept?"
- "How long does shipping take?"
- "What is your return policy?"
- "Do you ship internationally?"

## 🚀 Next Steps

- Explore the API documentation at `/docs`
- Try different LLM providers to compare responses
- Check the analytics dashboard for performance insights
- Review the conversation history and ratings

---

**Happy LLM Comparing! 🤖✨**
