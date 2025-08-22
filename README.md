# Customer Support Bot - LLM Comparison Tool

A comprehensive customer support bot that integrates **OpenAI GPT** and **Google Gemini** to compare their responses and performance in customer service scenarios.

<video src="/assets/AppOutput.mp4" loop muted autoplay></video>

## 🎯 Goals

- Get familiar with basic LLM APIs of different providers
- Learn different parameters to get quality responses and avoid hallucination
- Learn UI implementation and graph plotting using data
- Compare performance across different LLM providers

## ✨ Features

- **Dual LLM Integration**: Support for OpenAI GPT and Google Gemini
- **Interactive Chat Interface**: Modern, responsive chat UI for customer support conversations
- **Provider Switching**: Easy switching between OpenAI and Google Gemini
- **Response Rating System**: Rate responses on a 1-5 scale with optional feedback
- **Comprehensive Analytics**: Daily and weekly performance metrics with interactive charts
- **Conversation History**: Track and review all conversations with ratings
- **FAQ Context**: Pre-loaded e-commerce FAQ data for better responses
- **Real-time Performance**: Live comparison of different LLM providers

## 🏗️ Architecture

```
genai-customer-support-bot/
├── app/                    # Backend application
│   ├── __init__.py
│   ├── api.py             # FastAPI application and routes
│   ├── config.py          # Configuration and environment variables
│   ├── database.py        # Database models and connection
│   ├── llm_providers.py   # LLM provider integrations (OpenAI + Google)
│   ├── models.py          # Pydantic data models
│   ├── services.py        # Business logic services
│   └── seed_data.py       # Database seeding script
├── static/                 # Frontend assets
│   ├── index.html         # Main chat interface
│   ├── styles.css         # Modern CSS styling
│   └── script.js          # Frontend JavaScript logic
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd genai-customer-support-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Copy the environment template and add your API keys:

```bash
cp env.example .env
```

Edit `.env` and add your API keys:

```env
# LLM API Keys (at least one required)
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 4. Run the Application

```bash
python main.py
```

The application will be available at:
- **Chat Interface**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | - |
| `GOOGLE_API_KEY` | Google API key for Gemini models | - |
| `DEBUG` | Enable debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `MAX_TOKENS` | Maximum tokens for LLM responses | `1000` |
| `TEMPERATURE` | LLM response creativity (0.0-1.0) | `0.7` |

### LLM Provider Setup

#### OpenAI
1. Get API key from [OpenAI Platform](https://platform.openai.com/)
2. Add to `.env`: `OPENAI_API_KEY=your_key_here`

#### Google Gemini
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`: `GOOGLE_API_KEY=your_key_here`

## 💬 Usage

### 1. Select LLM Provider
- Choose between OpenAI GPT or Google Gemini
- Only one provider can be active at a time

### 2. Start Chatting
- Type your customer support questions
- Get responses from the selected LLM provider
- Rate responses on a 1-5 scale

### 3. Compare Performance
- View daily and weekly statistics
- Compare provider performance with interactive charts
- Review conversation history and ratings

### 4. Analytics Dashboard
- **Daily Stats**: Today's conversations, average rating, total ratings
- **Weekly Stats**: Last 7 days performance metrics
- **Provider Comparison**: Side-by-side performance analysis

## 📊 API Endpoints

### Chat
- `POST /api/chat` - Send message and get LLM response
- `GET /api/conversations` - Get conversation history

### Ratings
- `POST /api/rate` - Rate a conversation response

### Analytics
- `GET /api/analytics` - Get performance analytics
- `GET /api/providers` - Get available LLM providers

### FAQ
- `GET /api/faqs` - Get all FAQ items
- `GET /api/faqs/search` - Search FAQs by query

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile devices
- **Modern Interface**: Clean, professional design with smooth animations
- **Real-time Updates**: Live chat with typing indicators
- **Interactive Charts**: Plotly.js powered analytics visualization
- **Rating System**: Intuitive star-based rating interface
- **Provider Switching**: Easy provider selection with visual feedback

## 🔍 Sample Questions

Try these e-commerce related questions to test the bot:

- "What payment methods do you accept?"
- "How long does shipping take?"
- "What is your return policy?"
- "Do you ship internationally?"
- "How can I track my order?"
- "What if my item arrives damaged?"

## 🛠️ Development

### Project Structure

- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript with modern CSS
- **Database**: SQLite (easily configurable for production)
- **Charts**: Plotly.js for interactive visualizations

### Adding New LLM Providers

1. Create a new provider class in `app/llm_providers.py`
2. Inherit from `LLMProvider` base class
3. Implement required methods
4. Add to `LLMProviderFactory`

### Database Schema

- **Conversations**: Store chat messages and responses
- **Ratings**: Store user ratings and feedback
- **FAQs**: Store pre-loaded FAQ data for context

## 🚀 Deployment

### Production Considerations

1. **Database**: Use PostgreSQL or MySQL instead of SQLite
2. **Environment**: Set `DEBUG=False` in production
3. **API Keys**: Ensure secure storage of API keys
4. **HTTPS**: Enable SSL/TLS for production
5. **Monitoring**: Add logging and monitoring

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## 📈 Performance Metrics

The application tracks and compares:

- **Response Quality**: User ratings (1-5 scale)
- **Usage Volume**: Total conversations per provider
- **User Satisfaction**: Average ratings over time
- **Provider Reliability**: Success/failure rates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues and questions:
1. Check the [API documentation](http://localhost:8000/docs)
2. Review the conversation history for similar questions
3. Open an issue on GitHub

## 🔮 Future Enhancements

- **More LLM Providers**: Integration with additional providers
- **Advanced Analytics**: Machine learning insights and predictions
- **Custom Training**: Fine-tune models on specific domain data
- **Multi-language Support**: Internationalization for global users
- **Voice Interface**: Speech-to-text and text-to-speech capabilities
- **Integration APIs**: Connect with CRM and support systems

---

**Happy LLM Comparing! 🚀🤖**
