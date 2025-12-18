# Memory & Personality Engine

A system that extracts user memory from conversations and transforms agent responses based on different personality types. Built with React frontend and Python backend functions.

## 🎯 Features

### 1. Memory Extraction Module
- **User Preferences**: Identifies likes, dislikes, and preferences across categories
- **Emotional Patterns**: Detects recurring emotions and their triggers
- **Facts Worth Remembering**: Extracts important personal information, achievements, and context
- **Structured Output**: Uses Pydantic models for reliable JSON parsing

### 2. Personality Engine
- **Multiple Personalities**:
  - **Calm Mentor**: Supportive, wise, and patient guidance
  - **Witty Friend**: Fun, humorous, and lighthearted companion
  - **Therapist Style**: Empathetic, reflective, and therapeutic approach
  - **Neutral**: Standard helpful assistant
- **Memory Integration**: Personalizes responses based on extracted memory
- **Before/After Comparison**: Side-by-side comparison of different personality responses

### 3. Modern Web Interface
- **React-based** interactive chat interface
- Real-time memory extraction visualization
- Personality switching
- Before/after personality comparison
- Responsive, modern UI



## 📖 Usage

### 1. Start a Conversation
- Type messages in the chat interface
- The system will respond based on the selected personality

### 2. Extract Memory
- After sending several messages (ideally 10-30), click "Extract Memory"
- View extracted preferences, emotional patterns, and facts

### 3. Compare Personalities
- Enter a message and click "Compare Personalities"
- See how different personalities respond to the same input
- Toggle "Use Memory for Personalization" to see memory-enhanced responses

### 4. Switch Personalities
- Click on different personality buttons to change the agent's tone
- Continue the conversation with the new personality

## 🔧 Technical Highlights

### Structured Output Parsing
- Uses JSON mode for structured extraction
- Pydantic models ensure type safety
- Includes confidence scores and evidence for each extraction

### Modular Design
- **Python Functions**: Backend API functions
- **React Frontend**: Component-based UI
- **Separation of Concerns**: Clear API boundaries

### Memory Integration
- Extracted memory is formatted and injected into personality prompts
- Enables personalized responses based on user history
- Maintains context across conversations

## 📊 API Endpoints

- `GET /api/personalities` - Get available personalities
- `POST /api/extract_memory` - Extract memory from messages
- `POST /api/generate_response` - Generate response with personality
- `POST /api/compare_personalities` - Compare responses across personalities

## 🎨 Design Decisions

1. **Groq API**: Fast inference with Llama models
2. **Python Functions**: Modular backend functions
3. **React**: Modern, component-based frontend
4. **Evidence-based Extraction**: Each memory item includes evidence from messages
5. **Confidence Scores**: Helps filter low-confidence extractions

## 📝 Assignment Requirements Met

✅ **Memory Extraction Module**: Identifies preferences, emotional patterns, and facts  
✅ **Personality Engine**: Transforms agent tone (calm mentor, witty friend, therapist)  
✅ **Before/After Comparison**: Shows personality response differences  
✅ **Reasoning & Prompt Design**: Thoughtful prompts for extraction and personality  
✅ **Structured Output Parsing**: Pydantic models with JSON mode  
✅ **User Memory**: Core memory system for companion AI  
✅ **Modular Systems**: Clean separation of concerns  
✅ **Modular Architecture**: Clean separation of concerns  



This project is created for the Gupshup AI Engineer assignment.

