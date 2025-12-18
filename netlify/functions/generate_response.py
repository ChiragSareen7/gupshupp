
import json
import os
from groq import Groq

PERSONALITIES = {
    "calm_mentor": {
        "name": "Calm Mentor",
        "system_prompt": """You are a calm and wise mentor. Your responses are:
- Patient and supportive
- Thoughtful and reflective
- Focused on growth and learning
- Use gentle guidance rather than direct commands
- Show empathy and understanding
- Ask thoughtful questions to help the user reflect"""
    },
    "witty_friend": {
        "name": "Witty Friend",
        "system_prompt": """You are a witty and fun friend. Your responses are:
- Lighthearted and humorous
- Use jokes, puns, and playful banter when appropriate
- Casual and conversational
- Show enthusiasm and energy
- Make the conversation enjoyable
- Still supportive, but in a fun way"""
    },
    "therapist_style": {
        "name": "Therapist Style",
        "system_prompt": """You are a therapist-style companion. Your responses are:
- Deeply empathetic and non-judgmental
- Use reflective listening techniques
- Ask open-ended questions to explore feelings
- Validate emotions
- Help users process their thoughts and feelings
- Maintain professional boundaries while being warm"""
    },
    "neutral": {
        "name": "Neutral",
        "system_prompt": """You are a helpful assistant. Be friendly, clear, and concise."""
    }
}

def handler(event, context):
    """Netlify function handler"""
    try:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Content-Type': 'application/json'
        }
        
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': 'GROQ_API_KEY environment variable is not set'})
            }
        client = Groq(api_key=api_key)
        
        body = json.loads(event.get('body', '{}'))
        messages = body.get('messages', [])
        personality = body.get('personality', 'neutral')
        use_memory = body.get('use_memory', False)
        
        # Filter out system messages and clean message objects for API
        # Groq API only accepts 'user' and 'assistant' roles
        cleaned_messages = []
        for msg in messages:
            # Skip system messages (isSystem flag)
            if msg.get('isSystem', False):
                continue
            # Only include user and assistant messages
            if msg.get('role') in ['user', 'assistant']:
                cleaned_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        if personality not in PERSONALITIES:
            personality = 'neutral'
        
        system_prompt = PERSONALITIES[personality]['system_prompt']
        
        # If using memory, extract it first (simplified - in production, cache this)
        memory_context = ""
        if use_memory and cleaned_messages:
            # Extract memory from messages
            chat_history = "\n\n".join([
                f"{msg['role'].upper()}: {msg['content']}" 
                for msg in cleaned_messages
            ])
            
            memory_prompt = f"""Briefly summarize key information about the user from this conversation:
{chat_history}

Provide: preferences, emotional patterns, important facts. Be concise."""
            
            memory_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": memory_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            memory_context = memory_response.choices[0].message.content
            system_prompt += f"\n\nUSER CONTEXT (use this to personalize your responses):\n{memory_context}"
        
        # Prepare messages for API
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(cleaned_messages)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=api_messages,
            temperature=0.8 if personality != "neutral" else 0.7
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'response': response.choices[0].message.content})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

