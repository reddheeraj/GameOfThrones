from flask import Blueprint, jsonify, request
from utils import run_simulation_step, get_simulation_state, get_all_posts
from socket_manager import emit_agent_action

api_bp = Blueprint('api', __name__)

@api_bp.route('/simulate', methods=['POST'])
def simulate_step():
    """
    Run one step of the simulation.
    """
    run_simulation_step()
    return jsonify({"message": "Simulation step completed."})

@api_bp.route('/state', methods=['GET'])
def get_state():
    """
    Get the current state of the simulation.
    """
    state = get_simulation_state()
    return jsonify(state)

@api_bp.route('/posts', methods=['GET'])
def get_posts():
    """
    Get all social media posts.
    """
    posts = get_all_posts()
    return jsonify(posts)
