# Career Conversation Assistant

An AI-powered portfolio assistant built with Gradio and Groq that helps visitors explore professional background, skills, and experience through natural conversation. The assistant uses function calling to record user interactions and unknown questions for follow-up.

## 🚀 Live Demo

**Try it out:** [https://huggingface.co/spaces/Harshrc/career_conversation](https://huggingface.co/spaces/Harshrc/career_conversation)

## ✨ Features

- **Interactive Chat Interface**: Natural conversation about professional background, skills, and experience
- **AI-Powered Responses**: Uses Groq's GPT-OSS-20B model for intelligent, context-aware responses
- **Function Calling**: Automatically records user contact information and tracks unanswered questions
- **Multi-Source Context**: Integrates information from LinkedIn profile, resume, and personal summary
- **Push Notifications**: Sends notifications via Pushover for user interactions and unknown questions
- **Flexible Configuration**: Supports both environment variables (for deployment) and local file-based setup (for development)

## 🛠️ Tech Stack

- **Python 3.x**
- **Gradio** - Web interface framework
- **Groq** - High-performance LLM inference
- **PyPDF** - PDF document parsing
- **Python-dotenv** - Environment variable management
- **Requests** - HTTP requests for Pushover notifications

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/))
- Pushover account (optional, for notifications)
- PDF files for LinkedIn profile and resume (for local development)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd 1_foundations
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   PUSHOVER_TOKEN=your_pushover_token_here
   PUSHOVER_USER=your_pushover_user_here
   
   # Optional: For deployment, you can set these instead of using PDF files
   LINKEDIN_TEXT=your_linkedin_text_here
   RESUME_TEXT=your_resume_text_here
   SUMMARY_TEXT=your_summary_text_here
   ```

4. **Prepare local files (for development)**
   
   Create a `me/` directory with:
   - `linkedin.pdf` - Your LinkedIn profile exported as PDF
   - `resume.pdf` - Your resume as PDF
   - `summary.txt` - A text summary of your background

## 🚀 Usage

### Local Development

Run the application locally:

```bash
python app.py
```

The Gradio interface will launch and display a local URL (typically `http://127.0.0.1:7860`).

### Deployment with Gradio

Deploy to Hugging Face Spaces using Gradio CLI:

1. **Install Gradio CLI** (if not already installed)
   ```bash
   pip install gradio
   ```

2. **Login to Hugging Face**
   ```bash
   huggingface-cli login
   ```

3. **Deploy the app**
   ```bash
   gradio deploy
   ```

   Follow the prompts to:
   - Select your Hugging Face username
   - Choose a space name (e.g., `career_conversation`)
   - Select the Python SDK
   - Confirm deployment

4. **Set up Secrets in Hugging Face**
   
   After deployment, go to your Space settings and add the following secrets:
   - `GROQ_API_KEY`
   - `PUSHOVER_TOKEN`
   - `PUSHOVER_USER`
   - `LINKEDIN_TEXT` (optional, if not using PDF)
   - `RESUME_TEXT` (optional, if not using PDF)
   - `SUMMARY_TEXT` (optional, if not using file)

   The app will automatically use environment variables when deployed, falling back to files for local development.

## 📁 Project Structure

```
1_foundations/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env                  # Environment variables (not in git)
└── me/                   # Local files for development
    ├── linkedin.pdf
    ├── resume.pdf
    └── summary.txt
```

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key for LLM inference |
| `PUSHOVER_TOKEN` | No | Pushover API token for notifications |
| `PUSHOVER_USER` | No | Pushover user key for notifications |
| `LINKEDIN_TEXT` | No* | LinkedIn profile text (or use `me/linkedin.pdf`) |
| `RESUME_TEXT` | No* | Resume text (or use `me/resume.pdf`) |
| `SUMMARY_TEXT` | No* | Summary text (or use `me/summary.txt`) |

*Required if not using local PDF/text files

## 🎯 How It Works

1. **Initialization**: The `Me` class loads your professional information from environment variables or local files
2. **Chat Interface**: Users interact through a Gradio chat interface
3. **AI Processing**: Messages are processed by Groq's GPT-OSS-20B model with function calling capabilities
4. **Tool Execution**: The assistant can call two tools:
   - `record_user_details`: Captures user contact information
   - `record_unknown_question`: Logs questions that couldn't be answered
5. **Notifications**: Tool calls trigger Pushover notifications for tracking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Harsh Chauhan**

- Portfolio Assistant: [Live Demo](https://huggingface.co/spaces/Harshrc/career_conversation)
- Hugging Face: [@Harshrc](https://huggingface.co/Harshrc)

---

⭐ If you find this project helpful, please consider giving it a star!
