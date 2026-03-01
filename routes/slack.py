from flask import Blueprint, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os
from agents.graph import create_agent_graph

slack_bp = Blueprint('slack', __name__, url_prefix='/slack')

# Initialize Slack app
app = App(
    token=os.getenv('SLACK_BOT_TOKEN'),
    signing_secret=os.getenv('SLACK_SIGNING_SECRET')
)

handler = SlackRequestHandler(app)

@slack_bp.route('/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    return handler.handle(request)

@slack_bp.route('/commands', methods=['POST'])
def slack_commands():
    """Handle Slack slash commands"""
    return handler.handle(request)

@app.message(".*")
def handle_message(message, say):
    """Handle incoming Slack messages"""
    user_id = message['user']
    text = message['text']
    channel = message['channel']
    
    # Initialize agent graph
    agent = create_agent_graph()
    
    # Process message through agent
    result = agent.invoke({
        'user_id': user_id,
        'input': text
    })
    
    # Send response back to Slack
    say(f"Agent response: {result.get('output', 'No response')}", thread_ts=message.get('ts'))
