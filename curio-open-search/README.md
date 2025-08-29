# 🔍 Curio AI Tutor

A Streamlit-based AI learning assistant that helps students find personalized educational resources including YouTube videos and PDF documents. The app uses Perplexity AI's API to provide intelligent, context-aware learning recommendations.

## ✨ Features

- **AI-Powered Learning Guidance**: Get personalized learning recommendations based on your subject and grade level
- **Rich Media Embedding**: Automatically embeds YouTube videos and PDF documents for seamless learning
- **Interactive Chat Interface**: Natural conversation flow with the AI tutor
- **Smart Resource Curation**: Focuses on free, high-quality educational content
- **Citation Management**: Automatic conversion of citations to embedded content
- **Customizable AI Parameters**: Adjust temperature, model selection, and search recency
- **Session Management**: Maintains conversation history and allows easy reset

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Perplexity AI API key

### Installation

1. **Clone or download the project files**
   ```bash
   cd curio-open-search
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Perplexity AI API key**
   - Visit [Perplexity AI](https://www.perplexity.ai/)
   - Sign up for an account
   - Navigate to API settings to get your API key

4. **Run the application**
   ```bash
   streamlit run curio-open-search.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Enter your Perplexity API key in the sidebar
   - Start learning!

## 🎯 How to Use

### Basic Usage

1. **Enter your API key** in the sidebar configuration
2. **Ask a learning question** in the chat input, for example:
   - "I want to learn about photosynthesis for 8th grade"
   - "Help me understand calculus for high school"
   - "Find resources about World War II for 10th grade"

3. **Get personalized recommendations** including:
   - Curated YouTube videos
   - Relevant PDF documents
   - Learning path suggestions

4. **Refine your search** by:
   - Specifying your grade level
   - Narrowing down the subject area
   - Asking for different types of resources

### Advanced Features

- **Model Selection**: Choose between "sonar" and "sonar-pro" models
- **Temperature Control**: Adjust AI creativity (0.0 = focused, 1.0 = creative)
- **Search Recency**: Filter results by time (day, week, month, year)
- **Chat History**: View and continue previous conversations
- **Reset Function**: Clear chat history when needed

## 🔧 Configuration

### Sidebar Settings

- **API Key**: Your Perplexity AI API key (required)
- **Model**: Choose between available AI models
- **Temperature**: Control response randomness
- **Search Recency**: Filter search results by time
- **Reset Chat**: Clear conversation history

### Supported Content Types

- **YouTube Videos**: Automatically embedded with proper formatting
- **PDF Documents**: Embedded using Google Docs viewer
- **Citations**: Converted to clickable links and embedded content

## 📁 Project Structure

```
curio-open-search/
├── curio-open-search.py    # Main application file
├── requirements.txt         # Python dependencies
└── README.md              # This file
```

## 🛠️ Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **Requests**: HTTP library for API calls
- **JSON**: Built-in JSON processing
- **Re**: Regular expressions for text processing

### API Integration

- **Perplexity AI Chat Completions API**: Powers the AI responses
- **Streaming Responses**: Real-time content delivery
- **Search Metadata**: Automatic resource discovery and citation

### Key Functions

- `convert_citations_to_embedded_urls()`: Converts citations to embedded content
- `convert_direct_links_to_embedded()`: Embeds direct YouTube and PDF links
- **Streamlit Session State**: Manages chat history and user preferences

## 🎨 Customization

### Styling

The app includes custom CSS for embedded content:
- Rounded corners for iframes
- Subtle shadows for visual appeal
- Responsive design elements

### System Prompts

The AI behavior can be customized by modifying the system prompt in the code, which currently focuses on:
- Educational resource curation
- YouTube and PDF content prioritization
- Grade-level personalization
- Interactive learning guidance

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your Perplexity API key is correct
   - Check if you have sufficient API credits

2. **No Search Results**
   - Try different search terms
   - Adjust search recency filters
   - Check API key validity

3. **Embedding Issues**
   - YouTube videos require valid video IDs
   - PDFs must be publicly accessible URLs
   - Some content may not embed due to restrictions

### Performance Tips

- Use specific subject terms for better results
- Include grade level for personalized recommendations
- Reset chat history periodically for fresh conversations

## 📝 License

This project is open source. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📞 Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Review the Perplexity AI API documentation
3. Ensure all dependencies are properly installed

---

**Happy Learning! 🎓**

*Curio AI Tutor - Making education accessible, one question at a time.*
