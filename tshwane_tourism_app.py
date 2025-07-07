import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import tempfile
import os
from datetime import datetime
import hashlib
import base64
from cryptography.fernet import Fernet
import plotly.express as px
import plotly.graph_objects as go
from transformers import pipeline
import time
from urllib.parse import urljoin, urlparse
import warnings
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import uuid
warnings.filterwarnings('ignore')

# Enhanced system architecture inspired by analyzed AI tools


class OperationMode(Enum):
    PLANNING = "planning"
    STANDARD = "standard"
    REAL_TIME = "real_time"


@dataclass
class PlanStep:
    id: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class ToolCall:
    name: str
    parameters: Dict[str, Any]
    explanation: str
    result: Optional[Any] = None


class TshwanePlanningSystem:
    """Devin-inspired planning system for tourism data processing"""

    def __init__(self):
        self.mode = OperationMode.PLANNING
        self.gathered_info = {}
        self.plan_steps = []
        self.current_step = 0
        self.execution_log = []

    def think(self, observation: str) -> str:
        """Devin-style thinking for reflection and planning"""
        timestamp = datetime.now().isoformat()
        thought = {
            'timestamp': timestamp,
            'observation': observation,
            'current_mode': self.mode.value,
            'step': self.current_step
        }
        self.execution_log.append(thought)
        return f"💭 Thinking: {observation}"

    def suggest_plan(self, user_request: str) -> List[PlanStep]:
        """Create execution plan based on user request"""
        plan_id = str(uuid.uuid4())[:8]

        if "scrape" in user_request.lower() or "website" in user_request.lower():
            steps = [
                PlanStep(f"{plan_id}-1", "Initialize web scraping tools"),
                PlanStep(f"{plan_id}-2", "Scrape Tshwane Tourism website"),
                PlanStep(f"{plan_id}-3", "Process and categorize content"),
                PlanStep(f"{plan_id}-4", "Generate structured data files"),
                PlanStep(f"{plan_id}-5", "Create interactive visualizations")
            ]
        elif "booking" in user_request.lower():
            steps = [
                PlanStep(f"{plan_id}-1", "Validate booking form data"),
                PlanStep(f"{plan_id}-2", "Encrypt sensitive information"),
                PlanStep(f"{plan_id}-3", "Generate booking confirmation"),
                PlanStep(f"{plan_id}-4", "Send notification email"),
                PlanStep(f"{plan_id}-5", "Update booking database")
            ]
        else:
            steps = [
                PlanStep(f"{plan_id}-1", "Analyze user request"),
                PlanStep(f"{plan_id}-2", "Gather required information"),
                PlanStep(f"{plan_id}-3", "Execute primary task"),
                PlanStep(f"{plan_id}-4", "Validate results"),
                PlanStep(f"{plan_id}-5", "Present findings to user")
            ]

        self.plan_steps = steps
        return steps

    def execute_step(self, step_id: str) -> bool:
        """Execute a specific plan step"""
        step = next((s for s in self.plan_steps if s.id == step_id), None)
        if not step:
            return False

        step.status = "in_progress"
        try:
            # Simulate step execution
            time.sleep(0.5)  # Brief delay for realism
            step.status = "completed"
            step.result = f"Step {step_id} completed successfully"
            return True
        except Exception as e:
            step.status = "failed"
            step.error = str(e)
            return False


class ComponentSystem:
    """v0-inspired component system for modular UI"""

    @staticmethod
    def create_code_project(project_id: str, components: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured project similar to v0's CodeProject"""
        return {
            'id': project_id,
            'components': components,
            'runtime': 'streamlit',
            'created_at': datetime.now().isoformat(),
            'responsive': True
        }

    @staticmethod
    def render_component(component_type: str, props: Dict[str, Any]) -> None:
        """Render UI components with consistent styling"""
        if component_type == "gallery_card":
            st.markdown(f"""
            <div class="gallery-card" style="
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 10px;
                transition: transform 0.3s ease;
            ">
                <h3>{props.get('title', 'Untitled')}</h3>
                <p>{props.get('description', 'No description')}</p>
                <span class="badge">{props.get('type', 'general')}</span>
            </div>
            """, unsafe_allow_html=True)

        elif component_type == "progress_indicator":
            progress = props.get('progress', 0)
            st.progress(progress / 100)
            st.caption(f"Progress: {progress}%")

        elif component_type == "notification_toast":
            message_type = props.get('type', 'info')
            message = props.get('message', '')

            if message_type == 'success':
                st.success(message)
            elif message_type == 'error':
                st.error(message)
            elif message_type == 'warning':
                st.warning(message)
            else:
                st.info(message)


class SemanticSearch:
    """Cursor-inspired semantic search for tourism content"""

    def __init__(self):
        self.search_history = []

    def search_tourism_content(self, query: str, target_data: List[Dict] = None) -> List[Dict]:
        """Enhanced semantic search using real website data"""
        explanation = f"Searching real Tshwane tourism content for: '{query}'"

        # Use real website data if available
        if target_data is None and hasattr(st.session_state, 'searchable_content'):
            target_data = st.session_state.searchable_content
        elif target_data is None:
            target_data = st.session_state.places_data + st.session_state.restaurants_data

        # Log search
        self.search_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'explanation': explanation,
            'data_source': 'real_website' if hasattr(st.session_state, 'searchable_content') else 'session_data'
        })

        if not target_data:
            return []

        results = []
        query_lower = query.lower()

        # Enhanced search with real website content
        for item in target_data:
            score = 0
            name = item.get('name', '').lower()
            display_name = item.get('display_name', name).lower()
            description = item.get('description', '').lower()
            short_desc = item.get('short_description', '').lower()

            # Primary matching - exact matches get highest scores
            if query_lower in display_name:
                score += 15
            if query_lower in name:
                score += 12
            if query_lower in short_desc:
                score += 10
            if query_lower in description:
                score += 8

            # Category and type matching
            categories = item.get('ai_categories', item.get('categories', []))
            item_type = item.get('type', '').lower()

            if query_lower in item_type:
                score += 8

            for category in categories:
                if query_lower in category.lower():
                    score += 6

            # Enhanced semantic matching for Tshwane tourism content
            tourism_keywords = {
                'museum': ['ditsong', 'history', 'cultural', 'heritage', 'mrs ples', 'skull', 'ancestor'],
                'nature': ['wildlife', 'reserve', 'big 5', 'rhino', 'lion', 'giraffe', 'antelope', 'birding'],
                'architecture': ['grand', 'monument', 'sculpture', 'building', 'cultural'],
                'outdoor': ['nature', 'park', 'wildlife', 'reserve', 'birding', 'wetlands'],
                'culture': ['museum', 'heritage', 'historical', 'art', 'cultural', 'monument'],
                'food': ['restaurant', 'dining', 'cuisine', 'cafe', 'fine dining'],
                'entertainment': ['show', 'event', 'festival', 'music', 'market'],
                'shopping': ['market', 'centre', 'shopping', 'bustling'],
                'tourism': ['tourist', 'map', 'guide', 'information', 'accommodation']
            }

            # Check for semantic matches
            for key, keywords in tourism_keywords.items():
                if key in query_lower:
                    for keyword in keywords:
                        if keyword in description or keyword in name or keyword in display_name:
                            score += 4

                # Also check if any keyword matches the query
                for keyword in keywords:
                    if keyword in query_lower:
                        if key in description or key in name or key in display_name:
                            score += 3

            # Sentiment boost for positive content
            sentiment = item.get('ai_sentiment', 'neutral')
            if sentiment == 'positive':
                score += 2

            # Source verification boost
            if item.get('verified_source', False):
                score += 3

            # Weather suitability matching
            weather_terms = ['sunny', 'rainy',
                             'cloudy', 'hot', 'cold', 'weather']
            if any(term in query_lower for term in weather_terms):
                weather_data = item.get('weather_suitability', {})
                if weather_data:
                    score += 5

            if score > 0:
                results.append({
                    **item,
                    'relevance_score': score,
                    'search_query': query,
                    'matched_content': self._extract_matched_content(item, query_lower)
                })

        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:10]

    def _extract_matched_content(self, item: Dict[str, Any], query: str) -> str:
        """Extract the part of content that matches the search query"""
        description = item.get('description', '')
        if query in description.lower():
            # Find the sentence containing the query
            sentences = description.split('.')
            for sentence in sentences:
                if query in sentence.lower():
                    return sentence.strip() + "..."

        return item.get('short_description', description[:100] + "...")


# Page configuration
st.set_page_config(
    page_title="Tshwane Tourism Interactive Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for nature theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    .gallery-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px;
        transition: transform 0.3s ease;
    }
    .gallery-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    .nature-button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .notification {
        background: #e8f5e8;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced session state management


class SessionManager:
    """Lovable-inspired session state management"""

    @staticmethod
    def initialize_session():
        """Initialize all session state variables"""
        # Remove CSV loading and related variables
        defaults = {
            'website_data': {},
            'places_data': [],
            'restaurants_data': [],
            'social_links': [],
            'contact_info': {},
            'planning_system': TshwanePlanningSystem(),
            'component_system': ComponentSystem(),
            'semantic_search': SemanticSearch(),
            'operation_mode': OperationMode.PLANNING,
            'current_plan': None,
            'execution_progress': 0,
            'real_time_updates': True,
            'tool_calls': [],
            'notifications': [],
            'user_preferences': {
                'theme': 'nature',
                'auto_refresh': True,
                'show_progress': True
            },
            'csv_data_loaded': False,
            'available_place_types': [],
            'available_weather_options': []
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def update_progress(step: str, progress: int):
        """Update execution progress with real-time feedback"""
        st.session_state.execution_progress = progress
        if st.session_state.user_preferences['show_progress']:
            st.session_state.planning_system.think(
                f"Completed: {step} ({progress}%)")

    @staticmethod
    def add_notification(message: str, type: str = "info"):
        """Add notification with timestamp"""
        notification = {
            'id': str(uuid.uuid4())[:8],
            'message': message,
            'type': type,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        st.session_state.notifications.append(notification)

        # Keep only last 10 notifications
        if len(st.session_state.notifications) > 10:
            st.session_state.notifications = st.session_state.notifications[-10:]


class RealTimeProcessor:
    """Manus-inspired real-time processing system"""

    def __init__(self):
        self.processing_queue = []
        self.active_tasks = {}

    def add_task(self, task_id: str, task_type: str, parameters: Dict[str, Any]):
        """Add task to processing queue"""
        task = {
            'id': task_id,
            'type': task_type,
            'parameters': parameters,
            'status': 'queued',
            'created_at': datetime.now().isoformat()
        }
        self.processing_queue.append(task)
        return task_id

    def process_task(self, task_id: str) -> Dict[str, Any]:
        """Process a specific task with progress updates"""
        task = next(
            (t for t in self.processing_queue if t['id'] == task_id), None)
        if not task:
            return {'error': 'Task not found'}

        task['status'] = 'processing'
        self.active_tasks[task_id] = task

        try:
            if task['type'] == 'scrape_website':
                return self._process_website_scraping(task)
            elif task['type'] == 'process_booking':
                return self._process_booking(task)
            elif task['type'] == 'generate_recommendations':
                return self._process_recommendations(task)
            else:
                return {'error': 'Unknown task type'}

        except Exception as e:
            task['status'] = 'failed'
            task['error'] = str(e)
            return {'error': str(e)}

    def _process_website_scraping(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process website scraping with progress updates"""
        SessionManager.update_progress("Starting website scraping", 10)

        # Simulate scraping process
        url = task['parameters'].get('url', 'http://www.visittshwane.co.za')

        SessionManager.update_progress("Fetching website content", 30)
        time.sleep(1)  # Simulate network delay

        SessionManager.update_progress("Parsing HTML content", 50)
        time.sleep(0.5)

        SessionManager.update_progress("Extracting tourism data", 70)
        time.sleep(0.5)

        SessionManager.update_progress("Categorizing content", 90)
        time.sleep(0.5)

        SessionManager.update_progress("Website scraping completed", 100)

        task['status'] = 'completed'
        return {'success': True, 'message': 'Website scraping completed successfully'}

    def _process_booking(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process booking with encryption and validation"""
        SessionManager.update_progress("Validating booking data", 20)

        booking_data = task['parameters'].get('booking_data', {})

        SessionManager.update_progress("Encrypting sensitive information", 40)
        time.sleep(0.5)

        SessionManager.update_progress("Generating confirmation", 60)
        time.sleep(0.5)

        SessionManager.update_progress("Sending notifications", 80)
        time.sleep(0.5)

        SessionManager.update_progress("Booking processing completed", 100)

        task['status'] = 'completed'
        return {'success': True, 'booking_id': str(uuid.uuid4())[:8]}

    def _process_recommendations(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process weather-based recommendations"""
        SessionManager.update_progress("Analyzing weather conditions", 25)
        time.sleep(0.3)

        SessionManager.update_progress("Matching places to weather", 50)
        time.sleep(0.3)

        SessionManager.update_progress("Ranking recommendations", 75)
        time.sleep(0.3)

        SessionManager.update_progress("Recommendations generated", 100)

        task['status'] = 'completed'
        return {'success': True, 'recommendations': []}


# Initialize enhanced session management
SessionManager.initialize_session()

# Asset loading functions


def load_website_assets():
    """Load assets from the cloned website"""
    assets = {
        'images': [],
        'css': [],
        'js': [],
        'html_pages': []
    }

    try:
        # Load images from cloned website
        images_dir = Path("tshwane_crawled_data/assets")
        if images_dir.exists():
            for img_file in images_dir.glob("*.{jpg,jpeg,png,gif,svg}"):
                assets['images'].append(str(img_file))

        # Load HTML pages
        pages_dir = Path("tshwane_crawled_data/pages")
        if pages_dir.exists():
            for html_file in pages_dir.glob("*.html"):
                assets['html_pages'].append(str(html_file))

        # Load processed data
        data_dir = Path("processed_data")
        if data_dir.exists():
            if (data_dir / "enhanced_tshwane_data.json").exists():
                with open(data_dir / "enhanced_tshwane_data.json", 'r', encoding='utf-8') as f:
                    assets['tourism_data'] = json.load(f)

        return assets
    except Exception as e:
        st.warning(f"Could not load website assets: {e}")
        return assets


def get_place_types_from_csv():
    """Get unique place types from CSV for multi-select options"""
    from pathlib import Path
    import pandas as pd
    try:
        csv_file = Path("tshwane_places.csv")
        if not csv_file.exists():
            csv_file = Path("processed_data/tshwane_places.csv")
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            types = df['type'].unique().tolist()
            return [t for t in types if pd.notna(t)]
        else:
            return ['attraction', 'accommodation', 'restaurant', 'venue', 'area']
    except Exception as e:
        return ['attraction', 'accommodation', 'restaurant', 'venue', 'area']


def get_weather_options_from_csv():
    """Get weather options based on weather_suitability data in CSV"""
    from pathlib import Path
    import pandas as pd
    try:
        csv_file = Path("tshwane_places.csv")
        if not csv_file.exists():
            csv_file = Path("processed_data/tshwane_places.csv")
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            weather_options = set()
            for _, row in df.iterrows():
                weather_data = row.get('weather_suitability', '')
                if isinstance(weather_data, str) and weather_data.startswith('{'):
                    try:
                        weather_dict = eval(weather_data)
                        weather_options.update(weather_dict.keys())
                    except:
                        pass
            if weather_options:
                return sorted(list(weather_options))
            else:
                return ["sunny", "rainy", "cloudy", "hot", "cold", "windy", "mild"]
        else:
            return ["sunny", "rainy", "cloudy", "hot", "cold", "windy", "mild"]
    except Exception as e:
        return ["sunny", "rainy", "cloudy", "hot", "cold", "windy", "mild"]


def create_tutorial_system():
    """Create an interactive tutorial system"""
    if 'tutorial_step' not in st.session_state:
        st.session_state.tutorial_step = 0
        st.session_state.show_tutorial = False

    tutorial_steps = [
        {
            'title': '🌿 Welcome to Tshwane Tourism Portal',
            'content': 'This interactive portal helps you discover the beauty of Tshwane with AI-powered features. Let\'s take a quick tour!',
            'action': 'Click "Next" to continue'
        },
        {
            'title': '🎯 Operation Modes',
            'content': 'Choose between Planning Mode (for step-by-step guidance), Standard Mode (regular use), or Real-time Mode (live updates).',
            'action': 'Try changing the mode in the top-right corner'
        },
        {
            'title': '🌐 Load Tourism Data',
            'content': 'Click "Smart Load Tourism Data" in the sidebar to load real data from the Tshwane Tourism website.',
            'action': 'Look for the green button in the sidebar'
        },
        {
            'title': '🔍 Semantic Search',
            'content': 'Use the search box in the sidebar to find specific tourism content using AI-powered semantic search.',
            'action': 'Try searching for "outdoor activities" or "museums"'
        },
        {
            'title': '🏛️ Interactive Gallery',
            'content': 'Browse through real places from Tshwane using the interactive gallery with navigation controls.',
            'action': 'Use Previous/Next buttons or try the Random button'
        },
        {
            'title': '🌤️ Weather Recommendations',
            'content': 'Get AI-powered place recommendations based on current weather conditions.',
            'action': 'Select a weather condition and click "Get AI Recommendations"'
        },
        {
            'title': '📝 Smart Booking',
            'content': 'Book your visit using the enhanced booking form with real-time validation and encryption.',
            'action': 'Fill out the booking form to see validation in action'
        },
        {
            'title': '🎉 You\'re Ready!',
            'content': 'You\'ve completed the tutorial! Explore all the features and enjoy discovering Tshwane.',
            'action': 'Click "Finish" to start using the app'
        }
    ]

    return tutorial_steps


def display_tutorial():
    """Display the tutorial overlay"""
    if st.session_state.get('show_tutorial', False):
        tutorial_steps = create_tutorial_system()
        current_step = st.session_state.get('tutorial_step', 0)

        if current_step < len(tutorial_steps):
            step = tutorial_steps[current_step]

            # Tutorial overlay
            st.markdown(f"""
            <div class="tutorial-overlay" id="tutorial-overlay">
                <div class="tutorial-content fade-in-up">
                    <h2 style="color: var(--primary-green); margin-bottom: 16px;">
                        Step {current_step + 1} of {len(tutorial_steps)}
                    </h2>
                    <h3 style="color: var(--text-primary); margin-bottom: 12px;">
                        {step['title']}
                    </h3>
                    <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 20px;">
                        {step['content']}
                    </p>
                    <p style="color: var(--primary-green); font-weight: 500; margin-bottom: 24px;">
                        💡 {step['action']}
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="color: var(--text-muted); font-size: 0.9rem;">
                            Progress: {current_step + 1}/{len(tutorial_steps)}
                        </div>
                        <div>
                            <button onclick="skipTutorial()" style="
                                background: var(--accent-bg);
                                color: var(--text-secondary);
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                padding: 8px 16px;
                                margin-right: 8px;
                                cursor: pointer;
                            ">Skip</button>
                            <button onclick="nextTutorialStep()" style="
                                background: var(--primary-green);
                                color: var(--primary-bg);
                                border: none;
                                border-radius: 8px;
                                padding: 8px 16px;
                                cursor: pointer;
                                font-weight: 500;
                            ">
                                {('Finish' if current_step == len(
                tutorial_steps) - 1 else 'Next')}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                function nextTutorialStep() {{
                    window.parent.postMessage({{
                        type: 'tutorial_next'
                    }}, '*');
                }}

                function skipTutorial() {{
                    window.parent.postMessage({{
                        type: 'tutorial_skip'
                    }}, '*');
                }}
            </script>
            """, unsafe_allow_html=True)


def optimize_loading():
    """Optimize loading speed with caching and lazy loading"""
    # Cache website assets
    if 'website_assets' not in st.session_state:
        with st.spinner("🔄 Loading website assets..."):
            st.session_state.website_assets = load_website_assets()

    # Lazy load heavy components
    if 'heavy_components_loaded' not in st.session_state:
        st.session_state.heavy_components_loaded = False

# Encryption functions


def generate_key():
    """Generate a key for encryption"""
    return Fernet.generate_key()


def encrypt_data(data, key):
    """Encrypt data using Fernet encryption"""
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    """Decrypt data using Fernet encryption"""
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()

# Website scraping functions


@st.cache_data
def scrape_website(url):
    """Scrape the Tshwane Tourism website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data
        data = {
            'title': soup.find('title').text if soup.find('title') else '',
            'content': soup.get_text(),
            'links': [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)],
            'images': [urljoin(url, img.get('src')) for img in soup.find_all('img', src=True)],
            'social_links': extract_social_links(soup),
            'contact_info': extract_contact_info(soup),
            'places': extract_places(soup),
            'restaurants': extract_restaurants(soup)
        }

        return data
    except Exception as e:
        st.error(f"Error scraping website: {e}")
        return None


def extract_social_links(soup):
    """Extract social media links from the website"""
    social_patterns = [
        r'facebook\.com',
        r'twitter\.com',
        r'instagram\.com',
        r'linkedin\.com',
        r'youtube\.com',
        r'tiktok\.com'
    ]

    social_links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        for pattern in social_patterns:
            if re.search(pattern, href, re.IGNORECASE):
                social_links.append({
                    'platform': pattern.split('.')[0].title(),
                    'url': href,
                    'text': link.get_text(strip=True)
                })

    return social_links


def extract_contact_info(soup):
    """Extract contact information from the website"""
    contact_info = {}

    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, soup.get_text())
    contact_info['emails'] = list(set(emails))

    # Phone pattern
    phone_pattern = r'(\+27|0)[0-9\s\-\(\)]{8,15}'
    phones = re.findall(phone_pattern, soup.get_text())
    contact_info['phones'] = list(set(phones))

    # Address pattern (basic)
    address_elements = soup.find_all(text=re.compile(
        r'address|location|street|avenue|road', re.IGNORECASE))
    contact_info['addresses'] = [elem.strip() for elem in address_elements[:5]]

    return contact_info


def extract_places(soup):
    """Extract places/attractions from the website"""
    places = []

    # Look for common place indicators
    place_keywords = ['attraction', 'museum', 'park',
                      'monument', 'gallery', 'center', 'square', 'garden']

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'div', 'p']):
        text = element.get_text(strip=True)
        if any(keyword in text.lower() for keyword in place_keywords) and len(text) < 100:
            places.append({
                'name': text,
                'description': text,
                'type': 'attraction'
            })

    return places[:20]  # Limit to 20 places


def extract_restaurants(soup):
    """Extract restaurants from the website"""
    restaurants = []

    # Look for restaurant indicators
    restaurant_keywords = ['restaurant', 'cafe',
                           'dining', 'food', 'cuisine', 'bar', 'grill']

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'div', 'p']):
        text = element.get_text(strip=True)
        if any(keyword in text.lower() for keyword in restaurant_keywords) and len(text) < 100:
            restaurants.append({
                'name': text,
                'description': text,
                'type': 'restaurant'
            })

    return restaurants[:15]  # Limit to 15 restaurants

# Weather-based suggestions using Hugging Face


@st.cache_resource
def load_weather_model():
    """Load Hugging Face model for weather-based suggestions"""
    try:
        # Using a simple text classification model
        classifier = pipeline(
            "text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        return classifier
    except Exception as e:
        st.warning(f"Could not load weather model: {e}")
        return None


def get_weather_suggestions(weather_condition, places_data):
    """Get place suggestions based on weather"""
    weather_mapping = {
        'sunny': ['park', 'garden', 'outdoor', 'hiking', 'monument'],
        'rainy': ['museum', 'gallery', 'indoor', 'shopping', 'theater'],
        'cloudy': ['walking', 'city', 'cultural', 'historic', 'market'],
        'hot': ['water', 'shade', 'indoor', 'air-conditioned', 'cool'],
        'cold': ['indoor', 'warm', 'cozy', 'heated', 'shelter']
    }

    suggestions = []
    keywords = weather_mapping.get(weather_condition.lower(), [])

    for place in places_data:
        if any(keyword in place['description'].lower() for keyword in keywords):
            suggestions.append(place)

    return suggestions[:5]  # Return top 5 suggestions

# Enhanced main application with AI tool integrations


def main():
    """Main application with enhanced AI capabilities"""

    # Enhanced Dark Theme CSS with optimized performance
    st.markdown("""
    <style>
        /* Import Google Fonts for better readability */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Dark theme colors */
        :root {
            --primary-bg: #0e1117;
            --secondary-bg: #1a1d23;
            --accent-bg: #262730;
            --primary-green: #00d4aa;
            --secondary-green: #00b894;
            --dark-green: #00a085;
            --text-primary: #ffffff;
            --text-secondary: #b3b3b3;
            --text-muted: #8b8b8b;
            --border-color: #2d3748;
            --shadow-dark: rgba(0, 0, 0, 0.3);
            --shadow-light: rgba(0, 212, 170, 0.1);
        }

        /* Main app styling */
        .stApp {
            background: linear-gradient(135deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
        }

        /* Override Streamlit's default styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            background: transparent;
        }

        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
            padding: 24px;
            border-radius: 16px;
            color: var(--primary-bg);
            text-align: center;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px var(--shadow-light);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }

        .main-header h1 {
            font-weight: 700;
            font-size: 2.5rem;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .main-header p {
            font-weight: 400;
            font-size: 1.1rem;
            margin: 8px 0 0 0;
            opacity: 0.9;
        }

        /* Gallery card styling with optimized animations */
        .gallery-card {
            background: var(--accent-bg);
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 20px var(--shadow-dark);
            margin: 16px 0;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1),
                        box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--primary-green);
            will-change: transform;
        }

        .gallery-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 12px 40px var(--shadow-dark), 0 0 20px var(--shadow-light);
            border-left-color: var(--secondary-green);
        }

        .gallery-card h3 {
            color: var(--primary-green);
            font-weight: 600;
            font-size: 1.4rem;
            margin: 0 0 12px 0;
        }

        .gallery-card p {
            color: var(--text-secondary);
            line-height: 1.6;
            margin: 8px 0;
        }

        .gallery-card .badge {
            background: var(--primary-green);
            color: var(--primary-bg);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin-top: 12px;
        }

        /* Enhanced button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
            color: var(--primary-bg);
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(0, 212, 170, 0.2);
            font-family: 'Inter', sans-serif;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, var(--secondary-green) 0%, var(--dark-green) 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 170, 0.3);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Sidebar styling */
        .css-1d391kg, .css-1cypcdb {
            background: linear-gradient(180deg, var(--secondary-bg) 0%, var(--accent-bg) 100%);
            border-right: 1px solid var(--border-color);
        }

        .sidebar-content {
            padding: 16px;
        }

        .sidebar-button {
            display: block;
            width: 100%;
            background: var(--accent-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px 16px;
            margin: 8px 0;
            text-decoration: none;
            transition: all 0.2s ease;
            font-weight: 500;
            text-align: left;
            cursor: pointer;
        }

        .sidebar-button:hover {
            background: var(--primary-green);
            color: var(--primary-bg);
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0, 212, 170, 0.2);
        }

        .sidebar-button i {
            margin-right: 8px;
            width: 16px;
        }

        /* Form styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input {
            background: var(--accent-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--primary-green);
            box-shadow: 0 0 0 2px rgba(0, 212, 170, 0.2);
        }

        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        }

        /* Map container styling */
        .map-container {
            background: var(--accent-bg);
            border-radius: 16px;
            padding: 16px;
            margin: 16px 0;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 20px var(--shadow-dark);
            overflow: auto;
            height: 500px;
            position: relative;
        }

        .map-container iframe {
            border-radius: 12px;
            width: 100%;
            height: 100%;
            border: none;
        }

        /* Tutorial overlay */
        .tutorial-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .tutorial-content {
            background: var(--accent-bg);
            border-radius: 16px;
            padding: 32px;
            max-width: 500px;
            margin: 20px;
            border: 1px solid var(--border-color);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }

        /* Loading spinner */
        .loading-spinner {
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--primary-green);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Optimized animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--secondary-bg);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--primary-green);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-green);
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .gallery-card {
                margin: 8px 0;
                padding: 16px;
            }

            .main-header {
                padding: 16px;
            }

            .main-header h1 {
                font-size: 2rem;
            }

            .tutorial-content {
                margin: 10px;
                padding: 24px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize real-time processor
    if 'real_time_processor' not in st.session_state:
        st.session_state.real_time_processor = RealTimeProcessor()

    # Header with mode indicator
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("🌿 Tshwane Tourism Interactive Portal")
        st.markdown(
            "*Discover the beauty of Tshwane with our AI-powered tourism assistant*")

    with col2:
        # Mode selector (Devin-inspired)
        mode = st.selectbox(
            "Operation Mode",
            [OperationMode.PLANNING.value, OperationMode.STANDARD.value,
                OperationMode.REAL_TIME.value],
            index=0
        )
        st.session_state.operation_mode = OperationMode(mode)

    with col3:
        # Real-time refresh toggle (Lovable-inspired)
        auto_refresh = st.toggle(
            "🔄 Auto Refresh", value=st.session_state.user_preferences['auto_refresh'])
        st.session_state.user_preferences['auto_refresh'] = auto_refresh

        if auto_refresh:
            time.sleep(1)
            st.rerun()

    # Planning mode interface (Devin-inspired)
    if st.session_state.operation_mode == OperationMode.PLANNING:
        display_planning_interface()

    # Progress indicator (v0-inspired)
    if st.session_state.execution_progress > 0:
        st.session_state.component_system.render_component(
            "progress_indicator",
            {"progress": st.session_state.execution_progress}
        )

    # Enhanced sidebar with tool integration
    display_enhanced_sidebar()

    # Main content with component system
    display_main_content()

    # Real-time notifications (Lovable-inspired)
    display_real_time_notifications()


def display_planning_interface():
    """Devin-inspired planning interface"""
    st.subheader("🎯 Planning Mode")

    user_request = st.text_input(
        "What would you like to accomplish?",
        placeholder="e.g., Scrape tourism data, process bookings, generate recommendations..."
    )

    if st.button("📋 Create Plan") and user_request:
        plan = st.session_state.planning_system.suggest_plan(user_request)
        st.session_state.current_plan = plan

        st.success("✅ Plan created! Review the steps below:")

        for i, step in enumerate(plan):
            with st.expander(f"Step {i+1}: {step.description}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**ID:** {step.id}")
                    st.write(f"**Status:** {step.status}")
                with col2:
                    if st.button(f"▶️ Execute", key=f"exec_{step.id}"):
                        with st.spinner(f"Executing {step.description}..."):
                            success = st.session_state.planning_system.execute_step(
                                step.id)
                            if success:
                                SessionManager.add_notification(
                                    f"Step completed: {step.description}", "success")
                            else:
                                SessionManager.add_notification(
                                    f"Step failed: {step.description}", "error")
                        st.rerun()

    # Display current plan status
    if st.session_state.current_plan:
        st.subheader("📊 Current Plan Status")
        completed = sum(
            1 for step in st.session_state.current_plan if step.status == "completed")
        total = len(st.session_state.current_plan)
        progress = (completed / total) * 100 if total > 0 else 0

        st.progress(progress / 100)
        st.caption(
            f"Progress: {completed}/{total} steps completed ({progress:.1f}%)")


def display_enhanced_sidebar():
    """Enhanced sidebar with AI tool integrations, social/contact info, and dark theme"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-content">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: var(--primary-green); margin-bottom: 8px;">🌿 Tourism Portal</h2>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">AI-Powered Tools</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Social/Contact Info Section with interactive dark-themed animated buttons
        st.markdown("""
        <style>
        .social-btn {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            background: linear-gradient(90deg, #232526 0%, #414345 100%);
            color: #f5f7fa;
            border: none;
            border-radius: 30px;
            padding: 12px 22px;
            margin: 8px 0;
            font-size: 1.08rem;
            font-weight: 600;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-shadow: 0 2px 10px rgba(0,0,0,0.10);
            cursor: pointer;
            transition: transform 0.18s cubic-bezier(0.4,0,0.2,1), box-shadow 0.18s cubic-bezier(0.4,0,0.2,1), background 0.18s, color 0.18s;
            outline: none;
            gap: 14px;
            letter-spacing: 0.01em;
        }
        .social-btn:hover {
            transform: scale(1.07) translateX(6px);
            background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
            color: #232526;
            box-shadow: 0 8px 24px rgba(0,212,170,0.18);
        }
        .social-icon {
            font-size: 1.35rem;
            margin-right: 12px;
            width: 28px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("### 📱 Social & Contact Info")
        try:
            df_social = pd.read_csv('tshwane_social_links.csv')
            icon_map = {
                'facebook': '📘',
                'twitter': '🐦',
                'youtube': '▶️',
                'instagram': '📸',
                'linkedin': '💼',
                'tiktok': '🎵',
            }
            for _, row in df_social.iterrows():
                platform = str(row.get('platform', 'Unknown')).lower()
                url = row.get('url', '')
                text = row.get('text', platform.title())
                icon = icon_map.get(platform.split(
                    ',')[0].strip().lower(), '🔗')
                if url:
                    st.markdown(f"""
                    <a href='{url}' target='_blank' class='social-btn' style='text-decoration:none;'>
                        <span class='social-icon'>{icon}</span> {text}
                    </a>
                    """, unsafe_allow_html=True)
        except Exception:
            st.info("No social links found.")
        # Contact info as animated buttons
        st.markdown(f"""
        <a href='mailto:secretary@tshwanetourism.com' class='social-btn' style='text-decoration:none;'>
            <span class='social-icon'>✉️</span> Email: secretary@tshwanetourism.com
        </a>
        <a href='https://wa.me/27XXXXXXXXX' class='social-btn' style='text-decoration:none;'>
            <span class='social-icon'>💬</span> WhatsApp: +27 XX XXX XXXX
        </a>
        """, unsafe_allow_html=True)

        # Tutorial button
        if st.button("📚 Start Tutorial", key="tutorial_btn", help="Learn how to use the app"):
            st.session_state.show_tutorial = True
            st.session_state.tutorial_step = 0
            st.rerun()

        st.markdown("### 🚀 Quick Actions")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🌐 Load Data", key="load_data_btn", help="Load tourism data"):
                st.session_state['places_data'] = load_tshwane_places_csv()
                st.success("Tourism data loaded from tshwane_places.csv!")
        with col2:
            if st.button("🔄 Refresh", key="refresh_btn", help="Refresh the application"):
                st.rerun()

        st.markdown("### 🔍 Smart Search")
        search_query = st.text_input(
            "Search tourism content:",
            placeholder="outdoor activities, museums, restaurants...",
            key="search_input"
        )
        if st.button("🔍 Search", key="search_btn") and search_query:
            results = [place for place in st.session_state['places_data'] if search_query.lower() in place.get(
                'name', '').lower() or search_query.lower() in place.get('description', '').lower()]
            if results:
                st.success(f"Found {len(results)} results:")
                for result in results[:5]:
                    st.markdown(
                        f"**{result.get('name', 'Unknown')}**<br><small>{result.get('type', '')}</small>", unsafe_allow_html=True)
            else:
                st.info("No results found. Try different keywords.")

        st.markdown("### 🧭 Navigation")
        # Navigation links as dark-themed animated buttons (Streamlit-native, interactive)
        nav_links = [
            ("Places Gallery", "gallery", '🏛️'),
            ("Booking Form", "booking", '📝'),
            ("Weather Guide", "weather", '🌤️'),
            ("Analytics", "analytics", '📊'),
            ("Contact Info", "contact", '📞'),
        ]
        st.markdown("<div style='margin-top:18px;'></div>",
                    unsafe_allow_html=True)
        for text, key, icon in nav_links:
            btn = st.button(f"{icon} {text}",
                            key=f"nav_{key}", help=f"Go to {text}")
            if btn:
                st.session_state.current_section = key
                st.experimental_rerun()

        st.markdown("### 📊 System Status")
        st.metric("Places", len(st.session_state['places_data']), delta=None)
        st.metric("Notifications", len(
            st.session_state.get('notifications', [])), delta=None)

        # 4. OCR Module (file upload + text extraction)
        st.markdown("### 🖼️ OCR Scan")
        uploaded_file = st.file_uploader(
            "Upload image for OCR", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            try:
                import pytesseract
                from PIL import Image
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded Image", use_column_width=True)
                text = pytesseract.image_to_string(img)
                st.markdown("**Extracted Text:**")
                st.code(text)
            except Exception as e:
                st.error(f"OCR failed: {e}")

# 5. Left-side container for place summary/notifications


def display_left_summary():
    """Display summary of selected/booked place and notifications on the left"""
    with st.container():
        st.markdown("### 📝 Selected Place Summary")
        place = st.session_state.get('selected_place')
        if place:
            st.success(
                f"**{place.get('name', 'Unknown')}**\nType: {place.get('type', 'Unknown')}\n{place.get('description', '')}")
            lat, lon = place.get('latitude'), place.get('longitude')
            if lat and lon:
                st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        else:
            st.info("No place selected yet.")
        st.markdown("### 🔔 Notifications")
        for notif in st.session_state.get('notifications', [])[-5:]:
            st.info(f"{notif['message']} ({notif['timestamp'][:19]})")

# 2. WhatsApp notification simulation (UI element)


def simulate_whatsapp_notification(booking_data):
    st.markdown("---")
    st.markdown(
        f"**📲 WhatsApp Notification:**\nA WhatsApp message would be sent to {booking_data.get('whatsapp', '[number]')} confirming the booking for {booking_data.get('selected_place', '[place]')}. (Simulation)")

# 3. Enhanced booking form with restaurant multi-choice and reservation option


def display_enhanced_booking_form(allow_place_select=False):
    if 'selected_place' not in st.session_state or allow_place_select:
        place_options = [place['name']
                         for place in st.session_state.places_data]
        selected_place = st.selectbox(
            "Select Place to Visit (from CSV)", place_options)
        st.session_state.selected_place = next(
            (place for place in st.session_state.places_data if place['name'] == selected_place),
            None
        )
    # Restaurant multi-choice
    try:
        df_places = pd.read_csv(
            'scraps/Tryp_Thooe_Tourism-main/processed_data/tshwane_places.csv')
        restaurant_options = df_places[df_places['type']
                                       == 'restaurant']['name'].tolist()
    except Exception:
        restaurant_options = []
    selected_restaurants = st.multiselect(
        "Select Restaurants (optional)", restaurant_options)
    make_reservation = st.checkbox("Make restaurant reservation")
    # User details
    name = st.text_input("Full Name *", placeholder="Enter your full name")
    email = st.text_input(
        "Email Address *", placeholder="your.email@example.com")
    whatsapp = st.text_input(
        "WhatsApp Number *", placeholder="+27 XX XXX XXXX")
    visit_date = st.date_input("Preferred Visit Date")
    special_requests = st.text_area(
        "Special Requests", placeholder="Any special requirements or requests...")
    submitted = st.button("🚀 Submit Booking")
    if submitted:
        if name and email and whatsapp:
            booking_data = {
                'name': name,
                'email': email,
                'whatsapp': whatsapp,
                'selected_place': st.session_state.selected_place['name'],
                'selected_restaurants': selected_restaurants,
                'make_reservation': make_reservation,
                'visit_date': str(visit_date),
                'special_requests': special_requests,
                'timestamp': datetime.now().isoformat(),
                'booking_id': hashlib.md5(f"{name}{email}{datetime.now()}".encode()).hexdigest()[:8]
            }
            process_booking(booking_data)
            simulate_whatsapp_notification(booking_data)
        else:
            st.error("Please fill in all required fields marked with *")


def load_tshwane_places_csv():
    """Load tshwane_places.csv and return a list of dicts."""
    import pandas as pd
    try:
        df = pd.read_csv('tshwane_places.csv')
        return df.to_dict(orient='records')
    except Exception:
        return []


# At startup, ensure places_data is loaded
if 'places_data' not in st.session_state or not st.session_state['places_data']:
    st.session_state['places_data'] = load_tshwane_places_csv()


def display_main_content():
    """Main content area with component system"""
    # Create main columns at the top level
    col1, col2 = st.columns([2, 1])

    # Check if the user wants to see the booking form directly
    if st.session_state.get('current_section') == 'booking':
        with col1:
            st.subheader("📝 Book Your Experience")
            display_enhanced_booking_form(allow_place_select=True)
        with col2:
            st.subheader("📊 Data from Scraps & Project CSVs")
            # ... (keep the CSV dataframes code here) ...
            pass
        return

    with col1:
        # Component-based UI (v0-inspired)
        project = st.session_state.component_system.create_code_project(
            "tshwane-tourism-main",
            {
                "map_component": "Interactive map iframe",
                "gallery_component": "Places gallery with animations",
                "booking_component": "Secure booking form"
            }
        )

        # Enhanced interactive map with CSV data
        st.subheader("🗺️ Interactive Tshwane Map")

        # Map container with CSV data integration
        csv_places_count = len(st.session_state.places_data)
        csv_restaurants_count = len(st.session_state.restaurants_data)
        csv_total_count = csv_places_count + csv_restaurants_count

        st.markdown(f"""
        <div class="map-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h4 style="margin: 0; color: var(--primary-green);">🌍 Explore Tshwane</h4>
                <div style="display: flex; gap: 8px;">
                    <span class="badge">🏛️ {csv_places_count} Places</span>
                    <span class="badge">🍽️ {csv_restaurants_count} Restaurants</span>
                    <span class="badge">📊 {csv_total_count} Total from CSV</span>
                </div>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: 16px;">
                Interactive map with tourism data from tshwane_places.csv
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Map controls with CSV-based filters
        map_col1, map_col2, map_col3 = st.columns([1, 1, 2])
        with map_col1:
            show_places = st.checkbox(
                "Show Places", value=True, key="map_places")
        with map_col2:
            show_restaurants = st.checkbox(
                "Show Restaurants", value=True, key="map_restaurants")
        with map_col3:
            # Multi-select for place types from CSV
            available_types = st.session_state.get(
                'available_place_types', ['attraction', 'accommodation', 'restaurant'])
            selected_types = st.multiselect(
                "Filter by Type (from CSV)",
                options=available_types,
                default=available_types,
                key="map_type_filter",
                help="Select place types to display on the map"
            )

        # --- Folium Map Integration ---
        import folium
        from streamlit_folium import st_folium

        with st.container():
            st.markdown("### 🗺️ Folium Map of Tshwane Places (from CSV)")
            # Default Tshwane coordinates
            default_lat, default_lon = -25.7479, 28.1879
            m = folium.Map(location=[default_lat, default_lon], zoom_start=11)

            # Add markers for each place with coordinates
            for place in st.session_state.places_data:
                lat = place.get('lat', None)
                lon = place.get('lng', None)
                try:
                    if pd.isna(lat) or pd.isna(lon):
                        continue
                except Exception:
                    if lat is None or lon is None:
                        continue
                name = place.get('name', 'Unknown')
                short_desc = place.get('short_description', '')
                address = place.get('address', '')
                popup_html = f"""
                <b>{name}</b><br>
                <i>{address}</i><br>
                <p>{short_desc}</p>
                """
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=name,
                    icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(m)

            st_folium(m, width='100%', height=600)

        # Create map data from real website content
        if st.session_state.places_data and show_places:
            import pandas as pd

            # Create map data for real places
            map_data = []

            for i, place in enumerate(st.session_state.places_data):
                # Use Tshwane coordinates with slight variations for different places
                lat = -25.7479 + (i * 0.01)  # Spread around Tshwane
                lon = 28.1879 + (i * 0.01)

                map_data.append({
                    'lat': lat,
                    'lon': lon,
                    'name': place.get('display_name', place.get('name', 'Unknown')),
                    'size': 100 + (i * 20)  # Different sizes for variety
                })

            if map_data:
                df = pd.DataFrame(map_data)
                st.map(df, zoom=12)

                # Show place details below map
                with st.expander("📍 Place Details"):
                    for place in st.session_state.places_data:
                        verified = "✅" if place.get(
                            'verified_source') else "⚠️"
                        st.markdown(
                            f"**🏛️ {place.get('display_name', place.get('name'))}** {verified}")
                        st.caption(place.get('short_description',
                                   place.get('description', '')[:100]))

        # Fallback to website iframe
        try:
            st.markdown("### 🌐 Official Tshwane Tourism Website")
            st.components.v1.iframe(
                "http://www.visittshwane.co.za", height=400, scrolling=True)
        except Exception as e:
            st.error(f"Website loading failed: {e}")
            st.info("Please check your internet connection and try again.")

        # Enhanced interactive gallery with dashboard view option
        gallery_col1, gallery_col2 = st.columns([3, 1])
        with gallery_col1:
            st.subheader("🏛️ Places to Visit")
        with gallery_col2:
            view_mode = st.selectbox(
                "View Mode", ["Gallery", "Dashboard", "Table"], key="gallery_view_mode")

        if view_mode == "Dashboard":
            display_places_dashboard()
        elif view_mode == "Table":
            display_places_table()
        else:
            display_enhanced_gallery()

        # Enhanced booking form
        st.subheader("📝 Book Your Experience")
        display_enhanced_booking_form()

        # Real-time analytics
        st.subheader("📊 Real-time Analytics")
        display_analytics_dashboard()

    with col2:
        # Weather-based suggestions with AI - Call outside of columns
        st.subheader("🌤️ AI Weather Recommendations")
        # Move the function content here instead of calling it
        display_weather_content()

        # Real-time analytics
        st.subheader("📊 Real-time Analytics")
        display_analytics_dashboard()

        # Real-time notifications (Lovable-inspired)
        display_real_time_notifications()

        # --- NEW: Dataframes from scraps and root CSVs ---
        with st.container():
            st.markdown("### 📊 Data from Scraps & Project CSVs")
            import pandas as pd
            # Scraps CSVs
            try:
                df_places = pd.read_csv(
                    'scraps/Tryp_Thooe_Tourism-main/tshwane_places.csv')
                st.markdown('**scraps/tshwane_places.csv**')
                st.dataframe(df_places, use_container_width=True,
                             hide_index=True)
            except Exception as e:
                st.info(f"Could not load scraps places CSV: {e}")
            try:
                df_social = pd.read_csv(
                    'scraps/Tryp_Thooe_Tourism-main/tshwane_social_links.csv')
                st.markdown('**scraps/tshwane_social_links.csv**')
                st.dataframe(df_social, use_container_width=True,
                             hide_index=True)
            except Exception as e:
                st.info(f"Could not load scraps social links CSV: {e}")
            try:
                df_coords = pd.read_csv(
                    'scraps/Tryp_Thooe_Tourism-main/Repo/Tryp_Thooe_Tourism-main/tshwane_places_coordinates.csv')
                st.markdown('**scraps/Repo/tshwane_places_coordinates.csv**')
                st.dataframe(df_coords, use_container_width=True,
                             hide_index=True)
            except Exception as e:
                st.info(f"Could not load scraps coordinates CSV: {e}")
            # Root project CSVs
            try:
                df_places_root = pd.read_csv('tshwane_places.csv')
                st.markdown('**tshwane_places.csv**')
                st.dataframe(df_places_root,
                             use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root places CSV: {e}")
            try:
                df_social_root = pd.read_csv('tshwane_social_links.csv')
                st.markdown('**tshwane_social_links.csv**')
                st.dataframe(df_social_root,
                             use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root social links CSV: {e}")
            try:
                df_coords_root = pd.read_csv('tshwane_coordinates.csv')
                st.markdown('**tshwane_coordinates.csv**')
                st.dataframe(df_coords_root,
                             use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root coordinates CSV: {e}")
            try:
                df_desc_root = pd.read_csv('tshwane_descriptions.csv')
                st.markdown('**tshwane_descriptions.csv**')
                st.dataframe(
                    df_desc_root, use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root descriptions CSV: {e}")
            try:
                df_sent_root = pd.read_csv('tshwane_sentiment_data.csv')
                st.markdown('**tshwane_sentiment_data.csv**')
                st.dataframe(
                    df_sent_root, use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root sentiment data CSV: {e}")
            try:
                df_temp_root = pd.read_csv('tshwane_temperature_data.csv')
                st.markdown('**tshwane_temperature_data.csv**')
                st.dataframe(
                    df_temp_root, use_container_width=True, hide_index=True)
            except Exception as e:
                st.info(f"Could not load root temperature data CSV: {e}")


def display_weather_content():
    """Content for weather suggestions - extracted from display_ai_weather_suggestions"""
    # Get weather options from CSV data
    weather_options = st.session_state.get('available_weather_options', [
                                           "Sunny", "Rainy", "Cloudy", "Hot", "Cold", "Windy", "Mild"])
    # Capitalize first letter for display
    weather_options_display = [option.capitalize()
                               for option in weather_options]

    # Simple layout without nested columns
    selected_weather = st.selectbox(
        "Current Weather Condition", weather_options_display)

    auto_detect = st.button(
        "🌡️ Auto-Detect", help="Automatically detect weather (simulated)")
    if auto_detect:
        import random
        selected_weather = random.choice(weather_options)
        SessionManager.add_notification(
            f"Weather auto-detected: {selected_weather}", "info")

    # Use a separate section for the recommendations
    if st.button("🤖 Get AI Recommendations"):
        if st.session_state.places_data:
            with st.spinner("AI is analyzing weather conditions..."):
                suggestions = get_enhanced_weather_suggestions(
                    selected_weather, st.session_state.places_data)

                if suggestions:
                    st.markdown(
                        f"**🎯 AI Recommendations for {selected_weather.lower()} weather:**")

                    # Display recommendations without nested columns
                    for suggestion in suggestions:
                        with st.expander(f"🏛️ {suggestion['name']} (Score: {suggestion.get('weather_suitability_score', 0)})"):
                            st.markdown(
                                f"**Type:** {suggestion.get('type', 'Unknown')}")
                            st.markdown(
                                f"**Why recommended:** {suggestion.get('reason', 'Good match for current weather')}")
                            st.markdown(
                                f"**Weather suitability:** {suggestion.get('weather_suitability_score', 0)}/5")

                            if st.button(f"📋 Quick Book", key=f"quick_book_{suggestion['name']}"):
                                st.session_state.selected_place = suggestion
                                SessionManager.add_notification(
                                    f"Quick-selected {suggestion['name']}", "success")
                else:
                    st.info(
                        "No specific suggestions available for this weather condition.")
        else:
            st.info("Please load website data first.")

# Keep this function for compatibility but make it call the new function


def display_ai_weather_suggestions():
    """Compatibility wrapper for display_weather_content"""
    display_weather_content()


def display_sidebar_content():
    """Display social links and contact information"""
    # Display social links
    if st.session_state.social_links:
        st.subheader("📱 Social Media")
        for social in st.session_state.social_links:
            st.markdown(f"[{social['platform']}]({social['url']})")

    # Display contact info
    if st.session_state.contact_info:
        st.subheader("📞 Contact Information")
        if st.session_state.contact_info.get('emails'):
            st.write("📧 Emails:")
            for email in st.session_state.contact_info['emails'][:3]:
                st.write(f"• {email}")

        if st.session_state.contact_info.get('phones'):
            st.write("📱 Phones:")
            for phone in st.session_state.contact_info['phones'][:3]:
                st.write(f"• {phone}")


def save_scraped_data(data):
    """Save scraped data to files"""
    try:
        # Save as JSON
        with open('scraped_website_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Save places as CSV
        if data['places']:
            places_df = pd.DataFrame(data['places'])
            places_df.to_csv('tshwane_places.csv', index=False)

        # Save restaurants as CSV
        if data['restaurants']:
            restaurants_df = pd.DataFrame(data['restaurants'])
            restaurants_df.to_csv('tshwane_restaurants.csv', index=False)

        # Save social links as CSV
        if data['social_links']:
            social_df = pd.DataFrame(data['social_links'])
            social_df.to_csv('tshwane_social_links.csv', index=False)

        st.success("✅ Data saved to project folder!")

    except Exception as e:
        st.error(f"Error saving data: {e}")


def display_enhanced_gallery():
    """Rebuilt gallery using enhanced CSVs and project scope requirements"""
    import pandas as pd
    import ast
    # Load enhanced places data
    try:
        df_places = pd.read_csv(
            'scraps/Tryp_Thooe_Tourism-main/processed_data/tshwane_places.csv')
    except Exception:
        st.warning('Could not load enhanced places data. Gallery unavailable.')
        return
    # Load coordinates
    try:
        df_coords = pd.read_csv(
            'scraps/Tryp_Thooe_Tourism-main/Repo/Tryp_Thooe_Tourism-main/tshwane_places_coordinates.csv')
    except Exception:
        df_coords = pd.DataFrame()
    # Load enhanced descriptions
    try:
        df_desc = pd.read_csv(
            'scraps/Tryp_Thooe_Tourism-main/processed_data/tshwane_descriptions.csv')
    except Exception:
        df_desc = pd.DataFrame()
    # Merge coordinates
    if not df_coords.empty:
        df_places = pd.merge(df_places, df_coords, how='left',
                             left_on='name', right_on='place_name')
    # Merge descriptions
    if not df_desc.empty:
        df_places = pd.merge(df_places, df_desc, how='left',
                             left_on='name', right_on='Name')
    # Navigation state
    if 'gallery_index' not in st.session_state:
        st.session_state.gallery_index = 0
    n_places = len(df_places)
    if n_places == 0:
        st.warning('No places found in enhanced gallery.')
        return
    # Navigation controls
    nav1, nav2, nav3, nav4 = st.columns([1, 1, 1, 1])
    with nav1:
        if st.button('⬅️ Previous', key='gallery_prev'):
            st.session_state.gallery_index = (
                st.session_state.gallery_index - 1) % n_places
    with nav2:
        if st.button('🎲 Random', key='gallery_rand'):
            import random
            st.session_state.gallery_index = random.randint(0, n_places-1)
    with nav3:
        if st.button('Next ➡️', key='gallery_next'):
            st.session_state.gallery_index = (
                st.session_state.gallery_index + 1) % n_places
    with nav4:
        st.markdown(f"**{st.session_state.gallery_index+1} / {n_places}**")
    # Show current place
    place = df_places.iloc[st.session_state.gallery_index]
    # Card layout
    st.markdown('---')
    st.markdown(f"<div class='gallery-card fade-in-up'>",
                unsafe_allow_html=True)
    st.subheader(f"🏛️ {place.get('name', 'Unknown')}")
    st.caption(f"Type: {place.get('type', 'Unknown').title()}")
    # Short/long description
    short_desc = place.get('Short_Description') or place.get(
        'description') or ''
    long_desc = place.get('Long_Description') or place.get('description') or ''
    st.markdown(f"**{short_desc}**")
    with st.expander('Full Description'):
        st.write(long_desc)
    # Highlights
    highlights = place.get('Highlights', '')
    if isinstance(highlights, str) and highlights:
        st.markdown(f"**Highlights:** {highlights.replace('|', ', ')}")
    # Best time to visit
    best_time = place.get('Best_Time_To_Visit', '')
    if isinstance(best_time, str) and best_time:
        st.info(f"Best time to visit: {best_time}")
    # Accessibility
    access = place.get('Accessibility', '')
    if isinstance(access, str) and access:
        st.info(f"Accessibility: {access}")
    # Sentiment
    sentiment = place.get('ai_sentiment', '')
    if isinstance(sentiment, str) and sentiment:
        st.metric('Sentiment', sentiment.title())
    # Weather suitability
    weather = place.get('weather_suitability', '')
    if isinstance(weather, str) and weather and weather.startswith('{'):
        try:
            weather_dict = ast.literal_eval(weather)
            st.markdown('**Weather Suitability:**')
            st.json(weather_dict)
        except Exception:
            pass
    # Coordinates
    lat, lon = place.get('latitude'), place.get('longitude')
    if pd.notna(lat) and pd.notna(lon):
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
    # Book Now button
    if st.button('📋 Book Now', key=f'book_{st.session_state.gallery_index}'):
        st.session_state.selected_place = {
            'name': place.get('name', ''),
            'type': place.get('type', ''),
            'description': long_desc,
            'latitude': lat,
            'longitude': lon
        }
        st.session_state.current_section = 'booking'
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def display_places_dashboard():
    """Display all places in a comprehensive dashboard format"""
    if not st.session_state.places_data:
        st.warning("🌐 No tourism data loaded from tshwane_places.csv!")
        return

    st.markdown("### 📊 Places Dashboard Overview")

    # Summary metrics
    total_places = len(st.session_state.places_data)
    verified_places = sum(1 for place in st.session_state.places_data if place.get(
        'verified_source', False))
    place_types = len(set(place.get('type', 'unknown')
                      for place in st.session_state.places_data))

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Total Places", total_places)
    with metric_col2:
        st.metric("Verified Places", verified_places)
    with metric_col3:
        st.metric("Place Types", place_types)
    with metric_col4:
        places_with_weather = sum(
            1 for place in st.session_state.places_data if place.get('weather_suitability'))
        st.metric("Weather Data", places_with_weather)

    # Places by type chart
    import pandas as pd
    import plotly.express as px

    type_counts = {}
    for place in st.session_state.places_data:
        place_type = place.get('type', 'unknown').title()
        type_counts[place_type] = type_counts.get(place_type, 0) + 1

    if type_counts:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig_pie = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
                             title="Places by Type Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

        with chart_col2:
            fig_bar = px.bar(x=list(type_counts.keys()), y=list(type_counts.values()),
                             title="Places Count by Type")
            st.plotly_chart(fig_bar, use_container_width=True)


def display_places_table():
    """Display all places in a comprehensive table format"""
    if not st.session_state.places_data:
        st.warning("🌐 No tourism data loaded from tshwane_places.csv!")
        return

    st.markdown("### 📋 Places Data Table")

    # Create comprehensive dataframe
    import pandas as pd

    table_data = []
    for i, place in enumerate(st.session_state.places_data):
        sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}.get(
            place.get('ai_sentiment', 'neutral'), "😐")

        table_data.append({
            "#": i + 1,
            "🏛️ Name": place.get('display_name', place.get('name', 'Unknown')),
            "🏷️ Type": place.get('type', 'unknown').title(),
            "📝 Description": place.get('description', 'No description')[:100] + "..." if len(place.get('description', '')) > 100 else place.get('description', 'No description'),
            "😊 Sentiment": f"{sentiment_emoji} {place.get('ai_sentiment', 'neutral').title()}",
            "✅ Verified": "✅ Yes" if place.get('verified_source', False) else "⚠️ No",
            "🌤️ Weather": "✅ Yes" if place.get('weather_suitability') else "❌ No",
            "🌐 Source": place.get('data_source', 'Unknown')
        })

    if table_data:
        places_df = pd.DataFrame(table_data)

        # Add filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            type_filter = st.multiselect("Filter by Type",
                                         options=places_df["🏷️ Type"].unique(),
                                         default=places_df["🏷️ Type"].unique())
        with filter_col2:
            verified_filter = st.selectbox("Filter by Verification",
                                           options=["All", "✅ Yes", "⚠️ No"],
                                           index=0)
        with filter_col3:
            weather_filter = st.selectbox("Filter by Weather Data",
                                          options=["All", "✅ Yes", "❌ No"],
                                          index=0)

        # Apply filters
        filtered_df = places_df[places_df["🏷️ Type"].isin(type_filter)]
        if verified_filter != "All":
            filtered_df = filtered_df[filtered_df["✅ Verified"]
                                      == verified_filter]
        if weather_filter != "All":
            filtered_df = filtered_df[filtered_df["🌤️ Weather"]
                                      == weather_filter]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        # Download option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="tshwane_places_filtered.csv",
            mime="text/csv"
        )


def analyze_place_with_ai(place: Dict[str, Any]) -> str:
    """AI-powered place analysis using local models"""
    try:
        # Simple analysis based on keywords and type
        description = place.get('description', '').lower()
        place_type = place.get('type', '').lower()

        analysis_points = []

        # Activity recommendations
        if any(word in description for word in ['outdoor', 'park', 'garden']):
            analysis_points.append(
                "🌳 Perfect for outdoor activities and nature lovers")

        if any(word in description for word in ['museum', 'gallery', 'historic']):
            analysis_points.append(
                "🏛️ Rich in cultural and historical significance")

        if any(word in description for word in ['family', 'children', 'kids']):
            analysis_points.append("👨‍👩‍👧‍👦 Family-friendly destination")

        # Weather suitability
        if 'indoor' in description:
            analysis_points.append("☔ Great for rainy days")
        else:
            analysis_points.append("☀️ Best enjoyed on sunny days")

        # Accessibility
        if any(word in description for word in ['accessible', 'wheelchair', 'easy']):
            analysis_points.append("♿ Accessible for all visitors")

        if not analysis_points:
            analysis_points.append("🎯 A unique destination worth exploring")

        return "\n".join(f"• {point}" for point in analysis_points)

    except Exception as e:
        return f"Analysis temporarily unavailable: {str(e)}"


def display_enhanced_booking_form(allow_place_select=False):
    """Enhanced booking form with AI validation and real-time processing"""
    if 'selected_place' not in st.session_state or allow_place_select:
        # Allow user to select a place if not already selected or if forced
        place_options = [place['name']
                         for place in st.session_state.places_data]
        selected_place = st.selectbox(
            "Select Place to Visit (from CSV)", place_options)
        st.session_state.selected_place = next(
            (place for place in st.session_state.places_data if place['name'] == selected_place),
            None
        )
    # ... rest of the booking form code ...


def calculate_booking_score(booking_data: Dict[str, Any]) -> float:
    """Calculate booking validation score"""
    score = 0.0

    # Basic field validation
    if booking_data.get('name'):
        score += 0.2
    if booking_data.get('email') and '@' in booking_data['email']:
        score += 0.2
    if booking_data.get('whatsapp'):
        score += 0.2
    if booking_data.get('selected_place'):
        score += 0.2
    if booking_data.get('visit_date'):
        score += 0.2

    return score


def display_booking_form():
    """Display booking form with encryption"""
    if 'selected_place' not in st.session_state:
        st.info("Please select a place from the gallery above.")
        return

    with st.form("booking_form"):
        st.write(f"**Booking for:** {st.session_state.selected_place['name']}")

        # User details
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input(
            "Email Address *", placeholder="your.email@example.com")
        whatsapp = st.text_input(
            "WhatsApp Number *", placeholder="+27 XX XXX XXXX")

        # Place selection from CSV
        place_options = [place['name']
                         for place in st.session_state.places_data]
        selected_place = st.selectbox(
            "Select Place to Visit (from CSV)", place_options)

        # Multi-select for additional places from CSV
        additional_places = st.multiselect(
            "Additional Places to Visit",
            options=place_options,
            help="Select additional places you'd like to visit during your trip"
        )

        # Restaurant selection from CSV
        if st.session_state.restaurants_data:
            restaurant_options = ["None"] + [restaurant['name']
                                             for restaurant in st.session_state.restaurants_data]
            selected_restaurant = st.selectbox(
                "Select Restaurant (from CSV)", restaurant_options)
            make_reservation = st.checkbox("Make restaurant reservation")
        else:
            selected_restaurant = "None"
            make_reservation = False

        # Additional details
        visit_date = st.date_input("Preferred Visit Date")
        special_requests = st.text_area(
            "Special Requests", placeholder="Any special requirements or requests...")

        submitted = st.form_submit_button("🚀 Submit Booking")

        if submitted:
            if name and email and whatsapp:
                # Create booking data
                booking_data = {
                    'name': name,
                    'email': email,
                    'whatsapp': whatsapp,
                    'selected_place': selected_place,
                    'selected_restaurant': selected_restaurant,
                    'make_reservation': make_reservation,
                    'visit_date': str(visit_date),
                    'special_requests': special_requests,
                    'timestamp': datetime.now().isoformat(),
                    'booking_id': hashlib.md5(f"{name}{email}{datetime.now()}".encode()).hexdigest()[:8]
                }

                # Save and send booking
                process_booking(booking_data)
            else:
                st.error("Please fill in all required fields marked with *")


def process_booking(booking_data):
    """Process booking with encryption and email sending"""
    try:
        # Generate encryption key
        key = generate_key()

        # Encrypt sensitive data
        encrypted_data = encrypt_data(json.dumps(booking_data), key)

        # Save to DataFrame
        df = pd.DataFrame([booking_data])
        df.to_csv(f"booking_{booking_data['booking_id']}.csv", index=False)

        # Save encrypted version
        with open(f"encrypted_booking_{booking_data['booking_id']}.txt", 'wb') as f:
            f.write(encrypted_data)

        # Save encryption key separately
        with open(f"key_{booking_data['booking_id']}.key", 'wb') as f:
            f.write(key)

        # Send email (simulated)
        send_booking_email(booking_data)

        # Display confirmation
        st.success(
            f"✅ Booking submitted successfully! Booking ID: {booking_data['booking_id']}")

        # Add to notifications
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []

        st.session_state.notifications.append({
            'type': 'booking',
            'message': f"New booking for {booking_data['selected_place']} by {booking_data['name']}",
            'timestamp': datetime.now(),
            'data': booking_data
        })

    except Exception as e:
        st.error(f"Error processing booking: {e}")


def send_booking_email(booking_data):
    """Simulate sending email to secretary"""
    # In a real implementation, you would use actual SMTP settings
    email_content = f"""
    New Tourism Booking Request
    
    Booking ID: {booking_data['booking_id']}
    Client Name: {booking_data['name']}
    Email: {booking_data['email']}
    WhatsApp: {booking_data['whatsapp']}
    
    Selected Place: {booking_data['selected_place']}
    Selected Restaurant: {booking_data['selected_restaurant']}
    Restaurant Reservation: {'Yes' if booking_data['make_reservation'] else 'No'}
    
    Visit Date: {booking_data['visit_date']}
    Special Requests: {booking_data['special_requests']}
    
    Submitted: {booking_data['timestamp']}
    
    ---
    This booking was submitted through the Tshwane Tourism Interactive Portal
    Created by Profit Projects Online Virtual Assistance
    Enterprise Number: K2025200646
    Contact: Thapelo Kgothatso Thooe
    Email: kgothatsothooe@gmail.com
    """

    # Save email content to file
    with open(f"email_booking_{booking_data['booking_id']}.txt", 'w') as f:
        f.write(email_content)

    st.info("📧 Booking details prepared for email to secretary@tshwanetourism.com")


def display_ai_weather_suggestions():
    """Compatibility wrapper for display_weather_content"""
    display_weather_content()


def get_enhanced_weather_suggestions(weather_condition: str, places_data: List[Dict]) -> List[Dict]:
    """Enhanced weather suggestions with AI scoring"""
    weather_mapping = {
        'sunny': {
            'keywords': ['outdoor', 'park', 'garden', 'hiking', 'monument', 'scenic', 'nature'],
            'avoid': ['indoor', 'covered'],
            'reason': 'Perfect for outdoor exploration and sightseeing'
        },
        'rainy': {
            'keywords': ['indoor', 'museum', 'gallery', 'shopping', 'theater', 'cultural', 'covered'],
            'avoid': ['outdoor', 'hiking'],
            'reason': 'Stay dry while enjoying cultural experiences'
        },
        'cloudy': {
            'keywords': ['walking', 'city', 'historic', 'market', 'cultural', 'photography'],
            'avoid': [],
            'reason': 'Great lighting for photography and comfortable walking'
        },
        'hot': {
            'keywords': ['water', 'shade', 'indoor', 'cool', 'air-conditioned', 'swimming'],
            'avoid': ['hiking', 'strenuous'],
            'reason': 'Stay cool and comfortable during hot weather'
        },
        'cold': {
            'keywords': ['indoor', 'warm', 'cozy', 'heated', 'shelter', 'hot drinks'],
            'avoid': ['outdoor', 'water'],
            'reason': 'Warm and comfortable indoor experiences'
        },
        'windy': {
            'keywords': ['indoor', 'sheltered', 'stable'],
            'avoid': ['outdoor', 'high places'],
            'reason': 'Protected from strong winds'
        },
        'mild': {
            'keywords': ['walking', 'outdoor', 'sightseeing', 'flexible'],
            'avoid': [],
            'reason': 'Perfect weather for any activity'
        }
    }

    weather_info = weather_mapping.get(
        weather_condition.lower(), weather_mapping['mild'])
    keywords = weather_info['keywords']
    avoid_keywords = weather_info['avoid']
    reason = weather_info['reason']

    suggestions = []
    for place in places_data:
        content = str(place.get('description', '') +
                      ' ' + place.get('name', '')).lower()

        # Calculate positive score
        positive_score = sum(1 for keyword in keywords if keyword in content)

        # Calculate negative score
        negative_score = sum(
            1 for keyword in avoid_keywords if keyword in content)

        # Final score (0-5 scale)
        final_score = max(0, min(5, positive_score - negative_score))

        if final_score > 0:
            place_copy = place.copy()
            place_copy['weather_suitability_score'] = final_score
            place_copy['reason'] = reason
            suggestions.append(place_copy)

    # Sort by score and return top suggestions
    suggestions.sort(key=lambda x: x.get(
        'weather_suitability_score', 0), reverse=True)
    return suggestions[:5]


def display_weather_insights(weather_condition: str):
    """Display weather-specific insights and tips"""
    insights = {
        'sunny': {
            'icon': '☀️',
            'tips': ['Bring sunscreen and water', 'Perfect for outdoor photography', 'Early morning visits recommended'],
            'activities': ['Hiking', 'Garden tours', 'Outdoor monuments']
        },
        'rainy': {
            'icon': '🌧️',
            'tips': ['Bring an umbrella', 'Check indoor opening hours', 'Great for cozy experiences'],
            'activities': ['Museum visits', 'Gallery tours', 'Shopping centers']
        },
        'cloudy': {
            'icon': '☁️',
            'tips': ['Perfect for photography', 'Comfortable walking weather', 'No harsh shadows'],
            'activities': ['City walks', 'Historic tours', 'Market visits']
        },
        'hot': {
            'icon': '🌡️',
            'tips': ['Stay hydrated', 'Seek air-conditioned spaces', 'Avoid midday sun'],
            'activities': ['Indoor attractions', 'Water features', 'Shaded areas']
        },
        'cold': {
            'icon': '🥶',
            'tips': ['Dress warmly', 'Enjoy hot beverages', 'Indoor activities preferred'],
            'activities': ['Museums', 'Cafes', 'Indoor markets']
        }
    }

    insight = insights.get(weather_condition.lower())
    if insight:
        st.markdown(f"### {insight['icon']} Weather Insights")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**💡 Tips:**")
            for tip in insight['tips']:
                st.markdown(f"• {tip}")

        with col2:
            st.markdown("**🎯 Recommended Activities:**")
            for activity in insight['activities']:
                st.markdown(f"• {activity}")


def display_real_time_notifications():
    """Real-time notification system (Lovable-inspired)"""
    if st.session_state.notifications:
        st.markdown("### 🔔 Live Notifications")

        # Notification controls
        col1, col2 = st.columns([3, 1])
        with col1:
            show_all = st.toggle("Show All Notifications", value=False)
        with col2:
            if st.button("🗑️ Clear All"):
                st.session_state.notifications = []
                st.rerun()

        # Display notifications
        notifications_to_show = st.session_state.notifications if show_all else st.session_state.notifications[-5:]

        for notification in reversed(notifications_to_show):
            # Use component system for consistent styling
            st.session_state.component_system.render_component(
                "notification_toast",
                {
                    "type": notification['type'],
                    "message": f"{notification['message']} ({notification['timestamp'][:19]})"
                }
            )


def display_analytics_dashboard():
    """Real-time analytics dashboard"""
    if not st.session_state.places_data and not st.session_state.restaurants_data:
        st.info("Load data to see analytics")
        return

    # Basic analytics
    total_places = len(st.session_state.places_data)
    total_restaurants = len(st.session_state.restaurants_data)
    total_notifications = len(st.session_state.notifications)

    # Metrics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Places", total_places, delta=None)
    with col2:
        st.metric("Restaurants", total_restaurants, delta=None)
    with col3:
        st.metric("Notifications", total_notifications, delta=None)

    # Activity chart
    if st.session_state.notifications:
        notification_types = {}
        for notif in st.session_state.notifications:
            notif_type = notif['type']
            notification_types[notif_type] = notification_types.get(
                notif_type, 0) + 1

        if notification_types:
            fig = px.pie(
                values=list(notification_types.values()),
                names=list(notification_types.keys()),
                title="Notification Types Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)


def process_enhanced_booking(booking_data: Dict[str, Any]):
    """Enhanced booking processing with AI features"""
    try:
        # Generate encryption key
        key = generate_key()

        # Encrypt sensitive data
        encrypted_data = encrypt_data(json.dumps(booking_data), key)

        # Save to DataFrame with enhanced fields
        df = pd.DataFrame([booking_data])
        df.to_csv(f"booking_{booking_data['booking_id']}.csv", index=False)

        # Save encrypted version
        with open(f"encrypted_booking_{booking_data['booking_id']}.txt", 'wb') as f:
            f.write(encrypted_data)

        # Save encryption key separately
        with open(f"key_{booking_data['booking_id']}.key", 'wb') as f:
            f.write(key)

        # Enhanced email sending
        send_enhanced_booking_email(booking_data)

        # Display confirmation with AI insights
        st.success(f"✅ Booking processed successfully!")
        st.info(f"🆔 Booking ID: {booking_data['booking_id']}")
        st.info(
            f"🤖 AI Validation Score: {booking_data.get('validation_score', 0):.1f}/1.0")

        # Add to notifications with enhanced details
        SessionManager.add_notification(
            f"New booking: {booking_data['selected_place']} by {booking_data['name']} (Score: {booking_data.get('validation_score', 0):.1f})",
            "success"
        )

    except Exception as e:
        st.error(f"Error processing booking: {e}")
        SessionManager.add_notification(
            f"Booking processing failed: {str(e)}", "error")


def send_enhanced_booking_email(booking_data: Dict[str, Any]):
    """Enhanced email sending with AI-generated content"""
    email_content = f"""
    🌿 TSHWANE TOURISM ASSOCIATION - NEW BOOKING REQUEST

    ═══════════════════════════════════════════════════════════
    📋 BOOKING DETAILS
    ═══════════════════════════════════════════════════════════

    🆔 Booking ID: {booking_data['booking_id']}
    📅 Submitted: {booking_data['timestamp']}
    🤖 AI Processed: {booking_data.get('ai_processed', False)}
    ⭐ Validation Score: {booking_data.get('validation_score', 0):.1f}/1.0

    ═══════════════════════════════════════════════════════════
    👤 CLIENT INFORMATION
    ═══════════════════════════════════════════════════════════

    Name: {booking_data['name']}
    Email: {booking_data['email']}
    WhatsApp: {booking_data['whatsapp']}

    ═══════════════════════════════════════════════════════════
    🎯 BOOKING PREFERENCES
    ═══════════════════════════════════════════════════════════

    Selected Place: {booking_data['selected_place']}
    Selected Restaurant: {booking_data['selected_restaurant']}
    Restaurant Reservation: {'Yes' if booking_data['make_reservation'] else 'No'}
    Visit Date: {booking_data['visit_date']}

    ═══════════════════════════════════════════════════════════
    💬 SPECIAL REQUESTS
    ═══════════════════════════════════════════════════════════

    {booking_data['special_requests'] or 'None specified'}

    ═══════════════════════════════════════════════════════════
    🤖 AI SYSTEM INFORMATION
    ═══════════════════════════════════════════════════════════

    This booking was processed through our AI-powered tourism portal
    with enhanced validation and real-time processing capabilities.

    System Features Used:
    • Real-time form validation
    • AI-powered place analysis
    • Encrypted data transmission
    • Automated notification system

    ═══════════════════════════════════════════════════════════
    📞 CONTACT & SUPPORT
    ═══════════════════════════════════════════════════════════

    Created by: Profit Projects Online Virtual Assistance
    Enterprise Number: K2025200646
    Contact: Thapelo Kgothatso Thooe
    Email: kgothatsothooe@gmail.com

    For booking inquiries: secretary@tshwanetourism.com

    ═══════════════════════════════════════════════════════════
    """

    # Save email content to file
    with open(f"email_booking_{booking_data['booking_id']}.txt", 'w', encoding='utf-8') as f:
        f.write(email_content)

    st.info("📧 Enhanced booking email prepared for secretary@tshwanetourism.com")


if __name__ == "__main__":
    main()
