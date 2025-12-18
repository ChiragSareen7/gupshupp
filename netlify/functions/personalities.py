
import json

PERSONALITIES = [
    {
        "key": "neutral",
        "name": "Neutral",
        "description": "Standard helpful assistant"
    },
    {
        "key": "calm_mentor",
        "name": "Calm Mentor",
        "description": "Supportive, wise, and patient guidance"
    },
    {
        "key": "witty_friend",
        "name": "Witty Friend",
        "description": "Fun, humorous, and lighthearted companion"
    },
    {
        "key": "therapist_style",
        "name": "Therapist Style",
        "description": "Empathetic, reflective, and therapeutic approach"
    }
]

def handler(event, context):
    """Netlify function handler"""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'personalities': PERSONALITIES})
    }

