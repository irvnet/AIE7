# Student Loan Assistant Frontend

A modern Vue.js frontend for the Student Loan Assistant multi-agent RAG system.

## Features

- 🎨 **Modern UI** - Beautiful, responsive design with Tailwind CSS
- 💬 **Real-time Chat** - WebSocket-based chat interface
- 📝 **Markdown Support** - Rich text rendering for AI responses
- 🔧 **System Configuration** - Easy API key management
- 📊 **Status Monitoring** - Real-time system status display
- 📱 **Mobile Responsive** - Works on all device sizes

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Marked** - Markdown parser and renderer
- **Lucide Vue** - Beautiful icons
- **WebSocket** - Real-time communication

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

## Development

The frontend runs on `http://localhost:3000` and communicates with the FastAPI backend on `http://localhost:8000`.

### Project Structure

```
frontend/
├── src/
│   ├── App.vue          # Main application component
│   ├── main.js          # Application entry point
│   └── style.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── postcss.config.js    # PostCSS configuration
```

### Key Features

#### Real-time Chat Interface
- WebSocket connection for instant messaging
- Typing indicators
- Message history
- Markdown rendering for AI responses

#### System Configuration
- API key management
- System initialization
- Status monitoring

#### Responsive Design
- Mobile-first approach
- Tailwind CSS utilities
- Custom animations and transitions

## API Integration

The frontend communicates with the backend through:

1. **REST API** (`/api/*`) - For system management
2. **WebSocket** (`ws://localhost:8000/ws/chat`) - For real-time chat

### Environment Variables

No environment variables needed - all configuration is done through the UI.

## Contributing

1. Follow Vue.js best practices
2. Use Tailwind CSS for styling
3. Maintain responsive design
4. Test on multiple devices 