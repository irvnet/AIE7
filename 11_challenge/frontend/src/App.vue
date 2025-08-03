<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
              <GraduationCap class="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">Student Loan Assistant</h1>
              <p class="text-sm text-gray-500">AI-powered financial aid guidance</p>
            </div>
          </div>
          
          <!-- System Status -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div :class="[
                'w-3 h-3 rounded-full',
                systemStatus.initialized ? 'bg-green-500' : 'bg-red-500'
              ]"></div>
              <span class="text-sm text-gray-600">
                {{ systemStatus.initialized ? 'System Ready' : 'System Offline' }}
              </span>
            </div>
            
            <button 
              @click="showConfig = !showConfig"
              class="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
            >
              <Settings class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Configuration Modal -->
    <div v-if="showConfig" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold mb-4">System Configuration</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              OpenAI API Key
            </label>
            <input 
              v-model="config.openaiApiKey"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="sk-..."
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Tavily API Key (Optional)
            </label>
            <input 
              v-model="config.tavilyApiKey"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="tvly-..."
            />
          </div>
        </div>
        
        <div class="flex space-x-3 mt-6">
          <button 
            @click="initializeSystem"
            :disabled="!config.openaiApiKey || initializing"
            class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ initializing ? 'Initializing...' : 'Initialize System' }}
          </button>
          <button 
            @click="showConfig = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Chat Interface -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 h-[600px] flex flex-col">
            <!-- Chat Header -->
            <div class="p-4 border-b border-gray-200">
              <h2 class="text-lg font-semibold text-gray-900">Chat with AI Assistant</h2>
              <p class="text-sm text-gray-500">Ask questions about student loans and financial aid</p>
            </div>
            
            <!-- Chat Messages -->
            <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="chatContainer">
              <!-- System Status Banner -->
              <div v-if="!systemStatus.initialized" class="flex justify-center">
                <div class="bg-yellow-50 border border-yellow-200 rounded-lg px-4 py-3 max-w-md">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                    <span class="text-sm text-yellow-800">
                      System not initialized. 
                      <button 
                        @click="showConfig = true"
                        class="text-yellow-600 hover:text-yellow-800 underline font-medium"
                      >
                        Click here to configure API keys
                      </button>
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- Initialization Progress -->
              <div v-if="showInitializationProgress" class="flex justify-center">
                <div class="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3 max-w-md w-full">
                  <div class="space-y-2">
                    <div class="flex items-center justify-between">
                      <span class="text-sm font-medium text-blue-800">{{ initializationMessage }}</span>
                      <span class="text-sm text-blue-600">{{ initializationProgress }}%</span>
                    </div>
                    <div class="w-full bg-blue-200 rounded-full h-2">
                      <div 
                        class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        :style="{ width: initializationProgress + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div 
                v-for="(message, index) in messages" 
                :key="index"
                :class="[
                  'flex',
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                ]"
              >
                <div 
                  :class="[
                    'max-w-[80%] rounded-lg px-4 py-3',
                    message.role === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-900'
                  ]"
                >
                  <div v-if="message.role === 'assistant'" class="prose prose-sm max-w-none">
                    <div v-html="renderMarkdown(message.content)"></div>
                  </div>
                  <div v-else>{{ message.content }}</div>
                </div>
              </div>
              
              <!-- Typing Indicator -->
              <div v-if="isTyping" class="flex justify-start">
                <div class="bg-gray-100 rounded-lg px-4 py-3">
                  <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Chat Input -->
            <div class="p-4 border-t border-gray-200">
              <div class="flex space-x-3">
                <input 
                  v-model="newMessage"
                  @keyup.enter="sendMessage"
                  type="text"
                  :placeholder="systemStatus.initialized ? 'Ask about student loans...' : 'Type your question (system will prompt for API keys if needed)...'"
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button 
                  @click="sendMessage"
                  :disabled="!newMessage.trim()"
                  :class="[
                    'px-6 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed',
                    systemStatus.initialized 
                      ? 'bg-blue-600 text-white hover:bg-blue-700' 
                      : 'bg-gray-400 text-white hover:bg-gray-500'
                  ]"
                  :title="systemStatus.initialized ? 'Send message' : 'Send message (will prompt for API keys if needed)'"
                >
                  <Send class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div class="lg:col-span-1">
          <div class="space-y-6">
            <!-- System Status Card -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Vector Store</span>
                  <span :class="[
                    'text-sm font-medium',
                    systemStatus.vector_store_ready ? 'text-green-600' : 'text-red-600'
                  ]">
                    {{ systemStatus.vector_store_ready ? 'Ready' : 'Not Ready' }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Agents</span>
                  <span :class="[
                    'text-sm font-medium',
                    systemStatus.agents_ready ? 'text-green-600' : 'text-red-600'
                  ]">
                    {{ systemStatus.agents_ready ? 'Ready' : 'Not Ready' }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Documents</span>
                  <span class="text-sm font-medium text-gray-900">
                    {{ systemStatus.documents_loaded }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Chunks</span>
                  <span class="text-sm font-medium text-gray-900">
                    {{ systemStatus.total_chunks }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Example Questions -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Example Questions</h3>
              <div class="space-y-2">
                <button 
                  v-for="question in exampleQuestions"
                  :key="question"
                  @click="newMessage = question"
                  class="w-full text-left p-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md transition-colors"
                >
                  {{ question }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { marked } from 'marked'
import { GraduationCap, Settings, Send } from 'lucide-vue-next'
import axios from 'axios'

// Configure marked for security
marked.setOptions({
  breaks: true,
  gfm: true
})

export default {
  name: 'App',
  components: {
    GraduationCap,
    Settings,
    Send
  },
  setup() {
    const messages = ref([])
    const newMessage = ref('')
    const isTyping = ref(false)
    const showConfig = ref(false)
    const initializing = ref(false)
    const chatContainer = ref(null)
    const ws = ref(null)
    
    // Progress tracking
    const initializationProgress = ref(0)
    const initializationMessage = ref('')
    const showInitializationProgress = ref(false)
    
    const systemStatus = reactive({
      initialized: false,
      vector_store_ready: false,
      agents_ready: false,
      documents_loaded: 0,
      total_chunks: 0
    })
    
    const config = reactive({
      openaiApiKey: '',
      tavilyApiKey: ''
    })
    
    const exampleQuestions = [
      "What is the maximum loan amount for dependent undergraduate students?",
      "How do I apply for income-based repayment?",
      "What's the difference between subsidized and unsubsidized loans?",
      "What are the current interest rates for student loans?",
      "How do I qualify for loan forgiveness?"
    ]
    
    const API_BASE_URL = 'http://localhost:8000'
    
    // Initialize WebSocket connection
    const initWebSocket = () => {
      ws.value = new WebSocket(`ws://localhost:8000/ws/chat`)
      
      ws.value.onopen = () => {
        console.log('WebSocket connected')
      }
      
      ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        if (data.type === 'chat_response') {
          isTyping.value = false
          messages.value.push({
            role: 'assistant',
            content: data.content,
            timestamp: data.timestamp
          })
          scrollToBottom()
        } else if (data.type === 'initialization_progress') {
          // Handle initialization progress
          initializationProgress.value = data.progress
          initializationMessage.value = data.message
          showInitializationProgress.value = true
          
          // Hide progress when complete
          if (data.step === 'complete') {
            setTimeout(() => {
              showInitializationProgress.value = false
              initializationProgress.value = 0
            }, 2000)
          }
        }
      }
      
      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
      ws.value.onclose = () => {
        console.log('WebSocket disconnected')
      }
    }
    
    // Send message via WebSocket
    const sendMessage = async () => {
      if (!newMessage.value.trim()) return
      
      const message = newMessage.value.trim()
      messages.value.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      })
      
      newMessage.value = ''
      scrollToBottom()
      
      if (!systemStatus.initialized) {
        // System not initialized - show helpful message
        messages.value.push({
          role: 'assistant',
          content: 'Please initialize the system first by clicking the settings icon (⚙️) and entering your API keys.',
          timestamp: new Date().toISOString()
        })
        scrollToBottom()
        return
      }
      
      isTyping.value = true
      
      if (ws.value && ws.value.readyState === WebSocket.OPEN) {
        ws.value.send(JSON.stringify({
          type: 'chat_message',
          content: message
        }))
      } else {
        // WebSocket not connected - show error
        isTyping.value = false
        messages.value.push({
          role: 'assistant',
          content: 'Connection error. Please check if the backend is running and try again.',
          timestamp: new Date().toISOString()
        })
        scrollToBottom()
      }
    }
    
    // Initialize system
    const initializeSystem = async () => {
      initializing.value = true
      
      try {
        const response = await axios.post(`${API_BASE_URL}/initialize`, {
          openai_api_key: config.openaiApiKey,
          tavily_api_key: config.tavilyApiKey
        })
        
        if (response.data.success) {
          systemStatus.initialized = true
          showConfig.value = false
          await fetchSystemStatus()
          initWebSocket()
        }
      } catch (error) {
        console.error('Initialization failed:', error)
        alert('Failed to initialize system. Please check your API keys.')
      } finally {
        initializing.value = false
      }
    }
    
    // Fetch system status
    const fetchSystemStatus = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/status`)
        Object.assign(systemStatus, response.data)
      } catch (error) {
        console.error('Failed to fetch system status:', error)
      }
    }
    
    // Render markdown
    const renderMarkdown = (content) => {
      return marked(content)
    }
    
    // Scroll to bottom of chat
    const scrollToBottom = async () => {
      await nextTick()
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    }
    
    onMounted(() => {
      fetchSystemStatus()
    })
    
    return {
      messages,
      newMessage,
      isTyping,
      showConfig,
      initializing,
      systemStatus,
      config,
      exampleQuestions,
      chatContainer,
      sendMessage,
      initializeSystem,
      renderMarkdown,
      initializationProgress,
      initializationMessage,
      showInitializationProgress
    }
  }
}
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Prose styles for markdown */
.prose {
  color: #374151;
}

.prose p {
  margin-bottom: 0.75rem;
}

.prose ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-bottom: 0.75rem;
}

.prose ol {
  list-style-type: decimal;
  padding-left: 1.5rem;
  margin-bottom: 0.75rem;
}

.prose strong {
  font-weight: 600;
}

.prose em {
  font-style: italic;
}

.prose code {
  background-color: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

.prose pre {
  background-color: #1f2937;
  color: #f9fafb;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin-bottom: 0.75rem;
}

.prose pre code {
  background-color: transparent;
  padding: 0;
  color: inherit;
}
</style> 