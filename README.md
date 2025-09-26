# Commandly 1.02 with Agent 🎯

**An intelligent voice-controlled AI assistant with autonomous system control capabilities**

Commandly is a Python-based AI assistant that combines voice recognition, natural language processing, and system automation. It features an animated orb interface and can autonomously control your computer through voice commands while maintaining conversation context.

![Commandly Orb Interface](https://img.shields.io/badge/Interface-Animated_Orb-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![OpenAI](https://img.shields.io/badge/Powered_by-OpenAI-black?style=for-the-badge&logo=openai)

## ✨ Features

### 🎤 Voice Control
- **Real-time voice recognition** using OpenAI Whisper
- **Natural speech synthesis** with OpenAI TTS
- **Continuous listening mode** with wake word detection
- **Audio device management** and configuration

### 🤖 AI Agent Capabilities
- **Autonomous system control** - Execute commands and manage files
- **Intelligent conversation** - Context-aware responses using GPT models
- **Tool integration** - Access to file operations and system controls
- **Safety controls** - Configurable permission levels

### 🎨 Interactive Interface
- **Animated Orb Display** - Beautiful matplotlib-based visualization
- **Real-time audio visualization** - Responsive to voice input
- **Draggable window** - Always-on-top floating interface
- **Status indicators** - Visual feedback for AI states

### 🛠️ System Integration
- **Program launching** - Open applications by voice command
- **File management** - Create, read, and organize files
- **System controls** - Volume, power, and settings management
- **Web browser control** - Open URLs and search

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Audio input/output devices

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SalvatoreJAmico/commandly_1.02_with_agent.git
   cd commandly_1.02_with_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   COMMANDLY_ALLOW_WRITE=true
   COMMANDLY_FULL_CONTROL=false
   ```

4. **Run Commandly**
   ```bash
   python commandly.py
   ```

## 🎛️ Configuration

### Environment Variables

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required | - |
| `COMMANDLY_ALLOW_WRITE` | Allow file writing operations | `true` | `true`, `false` |
| `COMMANDLY_FULL_CONTROL` | Enable full system control | `false` | `true`, `false` |

### Safety Levels

- **Basic Mode** (`FULL_CONTROL=false`): Limited to safe operations like opening programs and basic file reading
- **Full Control** (`FULL_CONTROL=true`): Complete system access including file modifications and system commands

## 📋 Usage Examples

### Voice Commands

```
"Open Calculator"              # Launch applications
"What files are in my Documents?"  # File system queries  
"Create a new text file called notes.txt"  # File operations
"Set volume to 50%"           # System controls
"Search for Python tutorials" # Web searches
"What's the weather like?"    # General questions
```

### Conversation Flow

1. **Launch Commandly** - The orb interface appears
2. **Speak naturally** - No specific wake words required in continuous mode
3. **Visual feedback** - Orb animates during listening and processing
4. **AI responses** - Both visual text and spoken audio responses
5. **Command execution** - Automatic system actions when requested

## 🏗️ Project Structure

```
commandly_1.02_with_agent/
├── commandly.py              # Main application entry point
├── modules/
│   ├── __init__.py
│   ├── orb_animation.py      # GUI and animation system
│   ├── agent_core.py         # AI agent logic and tool routing
│   ├── gpt_integration.py    # OpenAI API integration
│   ├── voice_openai.py       # Voice I/O using OpenAI services
│   └── tools/
│       ├── __init__.py
│       ├── file_tools.py     # File system operations
│       └── system_control.py # System control functions
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔧 API Integration

### OpenAI Services Used
- **GPT-4/3.5-turbo** - Natural language understanding and response generation
- **Whisper** - Speech-to-text transcription
- **TTS (Text-to-Speech)** - Voice synthesis

### Tool System
The agent uses a dynamic tool system that allows it to:
- Execute file operations safely within defined boundaries
- Control system functions with permission checking
- Integrate with external APIs and services
- Maintain conversation context across interactions

## 🛡️ Security Features

- **API key protection** - Environment variables keep credentials safe
- **Sandboxed file operations** - Restricted to safe directories
- **Permission controls** - Granular control over agent capabilities
- **Safe mode defaults** - Conservative permissions by default

## 🐛 Troubleshooting

### Common Issues

**Audio device not found**
- Check your microphone and speaker connections
- Verify audio device permissions in Windows
- Install/update audio drivers

**OpenAI API errors**
- Verify your API key is correct and has sufficient credits
- Check internet connectivity
- Ensure API key has required permissions

**Permission denied errors**
- Check `COMMANDLY_ALLOW_WRITE` and `COMMANDLY_FULL_CONTROL` settings
- Run as administrator if needed for system-level operations
- Verify file/folder permissions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI services
- The Python community for excellent libraries
- Contributors and testers who help improve Commandly

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/SalvatoreJAmico/commandly_1.02_with_agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SalvatoreJAmico/commandly_1.02_with_agent/discussions)

---

**Made with ❤️ by [Salvatore J. Amico](https://github.com/SalvatoreJAmico)**

*Commandly - Your intelligent voice-controlled assistant*