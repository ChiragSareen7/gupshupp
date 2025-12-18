
import json
import os
from typing import List, Dict, Any
from groq import Groq
from pydantic import BaseModel, Field

class UserPreference(BaseModel):
    category: str
    preference: str
    confidence: float
    evidence: str

class EmotionalPattern(BaseModel):
    emotion: str
    frequency: str
    triggers: List[str]
    evidence: str

class Fact(BaseModel):
    fact: str
    category: str
    importance: str
    evidence: str

class ExtractedMemory(BaseModel):
    preferences: List[UserPreference]
    emotional_patterns: List[EmotionalPattern]
    facts: List[Fact]
    summary: str

def handler(event, context):
    
    try:
        # CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Content-Type': 'application/json'
        }
        
        # Handle preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Get API key
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': 'GROQ_API_KEY environment variable is not set'})
            }
        client = Groq(api_key=api_key)
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        messages = body.get('messages', [])
        
        # Filter out system messages and clean message objects for API
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
        
        if not cleaned_messages:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No messages provided'})
            }
        
        # Format messages for analysis
        chat_history = "\n\n".join([
            f"{msg['role'].upper()}: {msg['content']}" 
            for msg in cleaned_messages
        ])
        
        prompt = f"""Analyze the following chat conversation and extract structured information about the user.

CHAT HISTORY:
{chat_history}

Extract:
1. USER PREFERENCES: What does the user like/dislike? Include categories like food, music, work style, hobbies, communication preferences, etc.
2. EMOTIONAL PATTERNS: What emotions does the user frequently express? What triggers these emotions?
3. FACTS WORTH REMEMBERING: Important personal information, achievements, goals, relationships, or context that should be remembered.

Be specific and provide evidence from the messages. Only extract information that is clearly stated or strongly implied.
Focus on information that would be useful for building a long-term relationship with the user.

Respond with a valid JSON object matching this structure:
{{
  "preferences": [
    {{"category": "...", "preference": "...", "confidence": 0.0-1.0, "evidence": "..."}}
  ],
  "emotional_patterns": [
    {{"emotion": "...", "frequency": "...", "triggers": ["..."], "evidence": "..."}}
  ],
  "facts": [
    {{"fact": "...", "category": "...", "importance": "high/medium/low", "evidence": "..."}}
  ],
  "summary": "..."
}}"""

        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing conversations and extracting structured information about users. Always provide evidence from the messages. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        memory = ExtractedMemory(**result)
        
        # Format for display
        formatted = {
            "preferences": [
                {
                    "category": p.category,
                    "preference": p.preference,
                    "confidence": p.confidence,
                    "evidence": p.evidence
                }
                for p in memory.preferences
            ],
            "emotional_patterns": [
                {
                    "emotion": e.emotion,
                    "frequency": e.frequency,
                    "triggers": e.triggers,
                    "evidence": e.evidence
                }
                for e in memory.emotional_patterns
            ],
            "facts": [
                {
                    "fact": f.fact,
                    "category": f.category,
                    "importance": f.importance,
                    "evidence": f.evidence
                }
                for f in memory.facts
            ],
            "summary": memory.summary
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(formatted)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

