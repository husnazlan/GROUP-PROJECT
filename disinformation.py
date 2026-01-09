# ===============================
# DISINFORMATION PATTERN RECOGNITION SYSTEM
# Advanced Pattern Analysis for Information Verification
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
import re
import random
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter

# -------------------------------
# APP CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Disinformation Pattern Recognition",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with scientific/analytical theme
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        color: #1E3A8A;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(90deg, #1E40AF, #1D4ED8, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .pattern-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .pattern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .pattern-high {
        border-left-color: #DC2626;
        background: linear-gradient(135deg, #FEE2E2, white);
    }
    .pattern-medium {
        border-left-color: #F59E0B;
        background: linear-gradient(135deg, #FEF3C7, white);
    }
    .pattern-low {
        border-left-color: #10B981;
        background: linear-gradient(135deg, #D1FAE5, white);
    }
    .pattern-neutral {
        border-left-color: #6B7280;
        background: linear-gradient(135deg, #F3F4F6, white);
    }
    .confidence-meter {
        height: 8px;
        border-radius: 4px;
        background: #E5E7EB;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    .confidence-high {
        background: linear-gradient(90deg, #10B981, #34D399);
    }
    .confidence-medium {
        background: linear-gradient(90deg, #F59E0B, #FBBF24);
    }
    .confidence-low {
        background: linear-gradient(90deg, #DC2626, #EF4444);
    }
    .metric-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
        background: white;
        border: 2px solid;
    }
    .risk-high {
        border-color: #DC2626;
        color: #DC2626;
        background-color: #FEE2E2;
    }
    .risk-medium {
        border-color: #F59E0B;
        color: #D97706;
        background-color: #FEF3C7;
    }
    .risk-low {
        border-color: #10B981;
        color: #059669;
        background-color: #D1FAE5;
    }
    .analysis-panel {
        background: linear-gradient(135deg, #F8FAFC, #F1F5F9);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px solid #E2E8F0;
        margin: 1rem 0;
    }
    .pattern-indicator {
        display: flex;
        align-items: center;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        background: white;
        border: 1px solid #E5E7EB;
    }
    .indicator-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .pattern-timeline {
        padding: 1rem;
        background: white;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
    }
    .timeline-item {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 6px;
    }
    .timeline-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        background: linear-gradient(135deg, #1E40AF, #3B82F6);
        color: white;
        border: none;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    }
    .secondary-button {
        background: linear-gradient(135deg, #6B7280, #9CA3AF) !important;
    }
    .warning-panel {
        background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
        border: 3px solid #F59E0B;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .scientific-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .pattern-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .grid-item {
        padding: 1rem;
        border-radius: 8px;
        background: white;
        border: 1px solid #E5E7EB;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# DISINFORMATION PATTERN ANALYZER
# -------------------------------
class PatternRecognitionEngine:
    def __init__(self):
        # Define disinformation patterns with confidence scores
        self.patterns = {
            'emotional_amplification': {
                'name': 'Emotional Amplification',
                'indicators': ['!!!', '??!', 'SHOCKING', 'AMAZING', 'HEARTBREAKING', 'TERRIFYING'],
                'weight': 0.85,
                'description': 'Uses excessive emotional language to bypass critical thinking'
            },
            'urgency_creation': {
                'name': 'False Urgency',
                'indicators': ['BREAKING', 'URGENT', 'NOW', 'IMMEDIATE', 'ACT FAST', 'LAST CHANCE'],
                'weight': 0.78,
                'description': 'Creates artificial time pressure to prevent fact-checking'
            },
            'source_obfuscation': {
                'name': 'Source Obfuscation',
                'indicators': ['they say', 'experts claim', 'studies show', 'many people'],
                'weight': 0.72,
                'description': 'Uses vague sources to avoid verification'
            },
            'binary_narrative': {
                'name': 'Binary Narrative',
                'indicators': ['always', 'never', 'everyone', 'no one', '100%', 'complete'],
                'weight': 0.65,
                'description': 'Presents complex issues as simple good/bad dichotomies'
            },
            'conspiracy_framing': {
                'name': 'Conspiracy Framing',
                'indicators': ['cover-up', 'hidden truth', 'they don\'t want you to know', 'mainstream media'],
                'weight': 0.88,
                'description': 'Frames information as suppressed or hidden by authorities'
            },
            'miracle_solutions': {
                'name': 'Miracle Solution',
                'indicators': ['instant cure', 'overnight success', 'secret method', 'guaranteed results'],
                'weight': 0.75,
                'description': 'Promises unrealistic, simple solutions to complex problems'
            },
            'credibility_signaling': {
                'name': 'Credibility Signaling',
                'indicators': ['scientifically proven', 'doctor approved', 'official report', 'verified'],
                'weight': 0.68,
                'description': 'Uses credibility markers without actual verification'
            },
            'social_proof': {
                'name': 'Artificial Social Proof',
                'indicators': ['everyone is talking', 'viral', 'trending', 'millions agree'],
                'weight': 0.70,
                'description': 'Creates illusion of widespread acceptance'
            }
        }
        
        # Authenticity patterns
        self.authenticity_patterns = {
            'source_transparency': {
                'name': 'Source Transparency',
                'indicators': ['according to [specific source]', 'researchers at [institution]', 'study published in'],
                'weight': 0.82,
                'description': 'Clearly identifies specific, verifiable sources'
            },
            'data_specificity': {
                'name': 'Data Specificity',
                'indicators': ['data shows', 'statistics indicate', 'research conducted', 'analysis of'],
                'weight': 0.79,
                'description': 'Provides specific data and statistics'
            },
            'context_provision': {
                'name': 'Context Provision',
                'indicators': ['however', 'although', 'in contrast', 'it is important to note'],
                'weight': 0.76,
                'description': 'Provides balanced context and limitations'
            },
            'methodology_disclosure': {
                'name': 'Methodology Disclosure',
                'indicators': ['methodology', 'study design', 'sample size', 'limitations'],
                'weight': 0.85,
                'description': 'Explains how information was gathered or verified'
            },
            'expert_attribution': {
                'name': 'Expert Attribution',
                'indicators': ['expert in', 'professor of', 'researcher specializing in', 'according to Dr.'],
                'weight': 0.80,
                'description': 'Attributes information to specific, qualified experts'
            }
        }
    
    def analyze_patterns(self, text):
        """Analyze text for disinformation patterns"""
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        results = {
            'patterns_detected': [],
            'pattern_scores': {},
            'overall_risk_score': 0,
            'authenticity_score': 0,
            'pattern_count': 0,
            'text_metrics': {},
            'timeline_analysis': []
        }
        
        # Calculate text metrics
        results['text_metrics'] = {
            'word_count': word_count,
            'sentence_count': len(re.split(r'[.!?]+', text)),
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'exclamation_density': text.count('!') / max(1, word_count) * 1000,
            'question_density': text.count('?') / max(1, word_count) * 1000,
            'all_caps_count': len(re.findall(r'\b[A-Z]{3,}\b', text)),
            'number_count': len(re.findall(r'\b\d+\b', text))
        }
        
        # Detect disinformation patterns
        pattern_scores = {}
        for pattern_id, pattern in self.patterns.items():
            score = 0
            indicators_found = []
            
            for indicator in pattern['indicators']:
                if isinstance(indicator, str):
                    if indicator.lower() in text_lower:
                        count = text_lower.count(indicator.lower())
                        score += count * pattern['weight']
                        indicators_found.append(indicator)
            
            # Check for pattern combinations
            if len(indicators_found) >= 2:
                score *= 1.3  # Boost for multiple indicators
            
            if score > 0:
                pattern_scores[pattern_id] = {
                    'score': min(1.0, score),
                    'name': pattern['name'],
                    'description': pattern['description'],
                    'indicators_found': indicators_found,
                    'confidence': min(0.95, score * 0.8 + 0.2)
                }
        
        # Detect authenticity patterns
        authenticity_scores = {}
        for pattern_id, pattern in self.authenticity_patterns.items():
            score = 0
            
            for indicator in pattern['indicators']:
                if indicator.lower() in text_lower:
                    count = text_lower.count(indicator.lower())
                    score += count * pattern['weight']
            
            if score > 0:
                authenticity_scores[pattern_id] = {
                    'score': min(1.0, score),
                    'name': pattern['name'],
                    'description': pattern['description']
                }
        
        # Calculate overall scores
        if pattern_scores:
            avg_pattern_score = np.mean([p['score'] for p in pattern_scores.values()])
            max_pattern_score = max([p['score'] for p in pattern_scores.values()])
            results['overall_risk_score'] = min(1.0, (avg_pattern_score * 0.6 + max_pattern_score * 0.4))
        else:
            results['overall_risk_score'] = 0.1  # Low baseline risk
        
        if authenticity_scores:
            results['authenticity_score'] = min(1.0, np.mean([p['score'] for p in authenticity_scores.values()]))
        else:
            results['authenticity_score'] = 0.1  # Low baseline authenticity
        
        # Balance the scores (authenticity reduces risk)
        adjusted_risk = results['overall_risk_score'] * (1 - results['authenticity_score'] * 0.5)
        results['overall_risk_score'] = min(1.0, adjusted_risk)
        
        results['patterns_detected'] = pattern_scores
        results['authenticity_patterns'] = authenticity_scores
        results['pattern_count'] = len(pattern_scores)
        
        # Generate timeline analysis
        sentences = re.split(r'[.!?]+', text)
        for i, sentence in enumerate(sentences[:5]):  # Analyze first 5 sentences
            if len(sentence.strip()) > 10:
                sentence_risk = 0
                detected_patterns = []
                
                for pattern_id, pattern in self.patterns.items():
                    for indicator in pattern['indicators']:
                        if isinstance(indicator, str) and indicator.lower() in sentence.lower():
                            sentence_risk += pattern['weight']
                            detected_patterns.append(pattern['name'])
                            break
                
                if detected_patterns:
                    results['timeline_analysis'].append({
                        'sentence': sentence.strip(),
                        'risk': min(1.0, sentence_risk),
                        'patterns': list(set(detected_patterns))[:2]
                    })
        
        return results

# -------------------------------
# PATTERN DATABASE
# -------------------------------
def create_pattern_database():
    """Create database of information patterns for analysis"""
    
    case_studies = [
        {
            'title': 'Emotional Amplification Case',
            'text': 'SHOCKING BREAKING NEWS!!! The government is HIDING the REAL truth about this AMAZING discovery! Doctors are DEVASTATED by what they found! This will CHANGE everything FOREVER!!!',
            'patterns': ['emotional_amplification', 'urgency_creation', 'conspiracy_framing'],
            'risk_level': 'High',
            'analysis_focus': 'Emotional manipulation through excessive punctuation and capitalization'
        },
        {
            'title': 'Source Obfuscation Example',
            'text': 'Experts say that this new discovery will revolutionize everything. Studies show amazing results that they don\'t want you to know about. Many people are already seeing incredible benefits.',
            'patterns': ['source_obfuscation', 'miracle_solutions', 'social_proof'],
            'risk_level': 'Medium',
            'analysis_focus': 'Vague sourcing and unverified claims'
        },
        {
            'title': 'Balanced Scientific Report',
            'text': 'According to a study published in the Journal of Medical Research, researchers found a 15% improvement in outcomes. However, the study authors note limitations including sample size constraints and recommend further research to confirm findings.',
            'patterns': ['source_transparency', 'methodology_disclosure', 'context_provision'],
            'risk_level': 'Low',
            'analysis_focus': 'Clear sourcing and balanced presentation'
        },
        {
            'title': 'Binary Narrative Example',
            'text': 'This solution works 100% of the time for EVERYONE. There are NO side effects and it is COMPLETELY safe. The mainstream media NEVER reports on this because they want to keep you in the dark.',
            'patterns': ['binary_narrative', 'conspiracy_framing', 'miracle_solutions'],
            'risk_level': 'High',
            'analysis_focus': 'Absolute claims combined with conspiracy framing'
        },
        {
            'title': 'Data-Driven Analysis',
            'text': 'Analysis of data from the National Statistics Office shows a 3.2% economic growth. The methodology involved surveying 5,000 households across 50 regions. While positive, economists caution that seasonal factors may have influenced results.',
            'patterns': ['data_specificity', 'methodology_disclosure', 'context_provision'],
            'risk_level': 'Low',
            'analysis_focus': 'Specific data with methodological transparency'
        }
    ]
    
    pattern_definitions = [
        {
            'name': 'Emotional Amplification',
            'description': 'Uses excessive emotional language, punctuation, and capitalization to trigger emotional responses and bypass critical thinking.',
            'examples': ['"SHOCKING revelation!"', '"DEVASTATING consequences!"', 'Multiple exclamation marks (!!!)'],
            'detection_tip': 'Look for clusters of emotional adjectives and excessive punctuation.'
        },
        {
            'name': 'False Urgency',
            'description': 'Creates artificial time pressure to encourage quick sharing without verification.',
            'examples': ['"BREAKING: Act NOW!"', '"Limited time offer!"', '"Share before deleted!"'],
            'detection_tip': 'Check for time-sensitive language without actual time constraints.'
        },
        {
            'name': 'Source Obfuscation',
            'description': 'Uses vague references to authority ("experts say", "studies show") without specific citations.',
            'examples': ['"Scientists confirm..."', '"Research indicates..."', '"They don\'t want you to know..."'],
            'detection_tip': 'Ask "Which experts?" or "Which study?" to test specificity.'
        },
        {
            'name': 'Binary Narrative',
            'description': 'Presents complex issues as simple good/bad dichotomies with absolute language.',
            'examples': ['"100% effective"', '"Everyone agrees"', '"Complete solution"'],
            'detection_tip': 'Watch for absolutes (always, never, everyone, no one).'
        }
    ]
    
    return {
        'case_studies': case_studies,
        'pattern_definitions': pattern_definitions
    }

# -------------------------------
# INITIALIZE SESSION STATE
# -------------------------------
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = PatternRecognitionEngine()

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

if 'pattern_db' not in st.session_state:
    st.session_state.pattern_db = create_pattern_database()

# -------------------------------
# SIDEBAR - PATTERN LIBRARY
# -------------------------------
with st.sidebar:
    st.markdown('<div class="main-title">🔍 Disinformation Pattern Recognition</div>', unsafe_allow_html=True)
    
    # Pattern Library
    st.markdown("### 📚 Pattern Library")
    
    for pattern in st.session_state.pattern_db['pattern_definitions']:
        with st.expander(f"🔎 {pattern['name']}"):
            st.markdown(f"**Description**: {pattern['description']}")
            st.markdown("**Examples**:")
            for example in pattern['examples']:
                st.markdown(f"• `{example}`")
            st.markdown(f"**Detection Tip**: {pattern['detection_tip']}")
    
    st.markdown("---")
    
    # Quick Analysis
    st.markdown("### ⚡ Quick Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔬 Analyze Case", use_container_width=True):
            case = random.choice(st.session_state.pattern_db['case_studies'])
            st.session_state.analysis_text = case['text']
            st.session_state.case_title = case['title']
            st.rerun()
    
    with col2:
        if st.button("🔄 Random Text", use_container_width=True):
            all_texts = [c['text'] for c in st.session_state.pattern_db['case_studies']]
            st.session_state.analysis_text = random.choice(all_texts)
            st.session_state.case_title = "Random Sample"
            st.rerun()
    
    st.markdown("---")
    
    # Analysis Dashboard
    st.markdown("### 📊 Analysis Dashboard")
    
    if st.session_state.analysis_history:
        total_analyses = len(st.session_state.analysis_history)
        high_risk = sum(1 for h in st.session_state.analysis_history 
                       if h['overall_risk'] > 0.7)
        avg_risk = np.mean([h['overall_risk'] for h in st.session_state.analysis_history])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Analyses", total_analyses)
        with col2:
            st.metric("High Risk Cases", high_risk)
        
        # Risk distribution
        risk_levels = ['Low', 'Medium', 'High']
        risk_counts = [
            sum(1 for h in st.session_state.analysis_history if h['overall_risk'] < 0.4),
            sum(1 for h in st.session_state.analysis_history if 0.4 <= h['overall_risk'] <= 0.7),
            sum(1 for h in st.session_state.analysis_history if h['overall_risk'] > 0.7)
        ]
        
        fig = go.Figure(data=[go.Bar(
            x=risk_levels,
            y=risk_counts,
            marker_color=['#10B981', '#F59E0B', '#DC2626']
        )])
        
        fig.update_layout(
            title="Risk Distribution",
            height=200,
            margin=dict(t=30, b=10, l=10, r=10),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Most common patterns
        if total_analyses > 0:
            all_patterns = []
            for h in st.session_state.analysis_history:
                all_patterns.extend(h['patterns_detected'])
            
            if all_patterns:
                pattern_counts = Counter(all_patterns)
                common_patterns = pattern_counts.most_common(3)
                
                st.markdown("**Most Common Patterns:**")
                for pattern, count in common_patterns:
                    st.markdown(f"• {pattern}: {count} times")
    
    else:
        st.info("No analyses yet. Start by analyzing text above!")
    
    st.markdown("---")
    
    # System Information
    st.markdown("### ℹ️ System Info")
    st.caption("**Version**: 2.1 Pattern Recognition")
    st.caption("**Patterns**: 8 disinformation + 5 authenticity")
    st.caption("**Algorithm**: Weighted pattern matching")
    
    st.markdown("---")
    
    # Clear button
    if st.button("🗑️ Clear History", use_container_width=True, type="secondary"):
        st.session_state.analysis_history = []
        st.rerun()

# -------------------------------
# MAIN APPLICATION
# -------------------------------
st.markdown('<div class="main-title">🔍 DISINFORMATION PATTERN RECOGNITION SYSTEM</div>', unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["🔬 Pattern Analysis", "📚 Case Studies", "📈 System Dashboard"])

with tab1:
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🧪 Text Analysis Interface")
        st.caption("Enter text to analyze for disinformation patterns")
    with col2:
        if 'case_title' in st.session_state:
            st.markdown(f'<div style="padding: 0.5rem; border-radius: 8px; background: #E0F2FE; border: 2px solid #0EA5E9; text-align: center;"><strong>📝 {st.session_state.case_title}</strong></div>', unsafe_allow_html=True)
    
    # Text input
    input_text = st.text_area(
        "**Enter text for pattern analysis:**",
        height=200,
        value=st.session_state.get('analysis_text', ''),
        placeholder="Paste news article, social media post, or any text for pattern analysis...",
        key="pattern_analysis_input"
    )
    
    # Analysis buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        analyze_btn = st.button("🔍 Analyze Patterns", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("Clear Text", use_container_width=True, key="clear_pattern")
    with col3:
        sample_btn = st.button("Load Sample", use_container_width=True, key="load_sample")
    
    if clear_btn:
        st.session_state.analysis_text = ""
        st.rerun()
    
    if sample_btn:
        sample = random.choice(st.session_state.pattern_db['case_studies'])
        st.session_state.analysis_text = sample['text']
        st.session_state.case_title = sample['title']
        st.rerun()
    
    if analyze_btn and input_text.strip():
        with st.spinner("🔬 Analyzing patterns..."):
            # Progress animation
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.005)
                progress_bar.progress(i + 1)
            
            # Perform analysis
            results = st.session_state.analyzer.analyze_patterns(input_text)
            
            # Clear progress
            progress_bar.empty()
            
            # Display Risk Assessment
            st.markdown("### 📊 Risk Assessment")
            
            risk_score = results['overall_risk_score']
            authenticity_score = results['authenticity_score']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if risk_score < 0.4:
                    risk_level = "Low Risk"
                    risk_color = "#10B981"
                    risk_class = "risk-low"
                elif risk_score < 0.7:
                    risk_level = "Medium Risk"
                    risk_color = "#F59E0B"
                    risk_class = "risk-medium"
                else:
                    risk_level = "High Risk"
                    risk_color = "#DC2626"
                    risk_class = "risk-high"
                
                st.markdown(f'''
                <div class="scientific-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2.5rem; font-weight: 800; color: {risk_color};">
                            {risk_score:.1%}
                        </div>
                        <div style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">
                            <span class="{risk_class}">{risk_level}</span>
                        </div>
                        <div style="font-size: 0.9rem; color: #6B7280;">
                            Pattern Risk Score
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div class="scientific-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2.5rem; font-weight: 800; color: #3B82F6;">
                            {results['pattern_count']}
                        </div>
                        <div style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0; color: #1E40AF;">
                            Patterns Detected
                        </div>
                        <div style="font-size: 0.9rem; color: #6B7280;">
                            Unique disinformation patterns
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'''
                <div class="scientific-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2.5rem; font-weight: 800; color: #059669;">
                            {authenticity_score:.1%}
                        </div>
                        <div style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0; color: #065F46;">
                            Authenticity Score
                        </div>
                        <div style="font-size: 0.9rem; color: #6B7280;">
                            Positive pattern presence
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Confidence Meter
            st.markdown("#### 🎯 Pattern Confidence")
            confidence_value = risk_score
            confidence_class = "confidence-high" if confidence_value < 0.4 else "confidence-medium" if confidence_value < 0.7 else "confidence-low"
            
            st.markdown(f'''
            <div class="confidence-meter">
                <div class="confidence-fill {confidence_class}" style="width: {confidence_value*100}%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #6B7280; margin-top: 0.5rem;">
                <span>Low Risk</span>
                <span>Medium Risk</span>
                <span>High Risk</span>
            </div>
            ''', unsafe_allow_html=True)
            
            # Detected Patterns
            st.markdown("### 🔎 Detected Patterns")
            
            if results['patterns_detected']:
                for pattern_id, pattern_data in results['patterns_detected'].items():
                    pattern_score = pattern_data['score']
                    
                    if pattern_score > 0.7:
                        pattern_class = "pattern-high"
                    elif pattern_score > 0.4:
                        pattern_class = "pattern-medium"
                    else:
                        pattern_class = "pattern-low"
                    
                    st.markdown(f'''
                    <div class="pattern-card {pattern_class}">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="margin: 0; color: #1F2937;">{pattern_data['name']}</h4>
                                <p style="margin: 0.5rem 0; color: #6B7280; font-size: 0.9rem;">
                                    {pattern_data['description']}
                                </p>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.8rem; font-weight: 800; color: #DC2626;">
                                    {pattern_score:.0%}
                                </div>
                                <div style="font-size: 0.8rem; color: #9CA3AF;">
                                    Pattern Strength
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <div style="font-size: 0.85rem; color: #4B5563; font-weight: 600;">
                                Indicators Found:
                            </div>
                            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.3rem;">
                                {''.join([f'<span class="metric-badge risk-high">{ind}</span>' for ind in pattern_data['indicators_found'][:3]])}
                            </div>
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <div style="font-size: 0.85rem; color: #4B5563;">
                                <strong>Confidence:</strong> {pattern_data['confidence']:.1%}
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown('<div class="pattern-card pattern-neutral"><div style="text-align: center; padding: 1rem;"><h4 style="color: #6B7280;">✅ No Strong Disinformation Patterns Detected</h4><p style="color: #9CA3AF;">The text shows minimal indicators of common disinformation patterns.</p></div></div>', unsafe_allow_html=True)
            
            # Authenticity Patterns
            if results['authenticity_patterns']:
                st.markdown("### ✅ Authenticity Indicators")
                
                for pattern_id, pattern_data in results['authenticity_patterns'].items():
                    st.markdown(f'''
                    <div class="pattern-indicator">
                        <div class="indicator-dot" style="background: #10B981;"></div>
                        <div style="flex: 1;">
                            <strong>{pattern_data['name']}</strong>
                            <div style="font-size: 0.85rem; color: #6B7280;">
                                {pattern_data['description']}
                            </div>
                        </div>
                        <div style="font-weight: 600; color: #059669;">
                            +{pattern_data['score']:.0%}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            # Timeline Analysis
            if results['timeline_analysis']:
                st.markdown("### ⏳ Text Timeline Analysis")
                st.markdown('<div class="pattern-timeline">', unsafe_allow_html=True)
                
                for i, item in enumerate(results['timeline_analysis']):
                    risk_color = "#DC2626" if item['risk'] > 0.7 else "#F59E0B" if item['risk'] > 0.4 else "#10B981"
                    
                    st.markdown(f'''
                    <div class="timeline-item" style="background: {risk_color}10;">
                        <div class="timeline-dot" style="background: {risk_color};"></div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; margin-bottom: 0.2rem;">
                                Sentence {i+1} • Risk: <span style="color: {risk_color};">{item['risk']:.0%}</span>
                            </div>
                            <div style="font-size: 0.9rem; color: #4B5563; font-style: italic;">
                                "{item['sentence']}..."
                            </div>
                            <div style="font-size: 0.8rem; color: #6B7280; margin-top: 0.2rem;">
                                <strong>Patterns:</strong> {', '.join(item['patterns'])}
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Text Metrics - CORRECTED SECTION
            st.markdown("### 📈 Text Metrics")

            metrics = results['text_metrics']
            cols = st.columns(4)

            metric_config = [
                ("Word Count", metrics['word_count'], "#3B82F6", "📊"),
                ("Sentences", metrics['sentence_count'], "#8B5CF6", "🔤"),
                ("Exclamations", metrics['exclamation_density'], "#EF4444", "❗"),
                ("Numbers", metrics['number_count'], "#10B981", "🔢")
            ]

            for idx, (label, value, color, icon) in enumerate(metric_config):
                with cols[idx]:
                    # Format the value outside the f-string
                    if isinstance(value, float):
                        display_value = f"{value:.1f}"
                    else:
                        display_value = str(value)
                    
                    st.markdown(f'''
                    <div class="grid-item">
                        <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                            {icon}
                        </div>
                        <div style="font-size: 1.8rem; font-weight: 800; color: {color};">
                            {display_value}
                        </div>
                        <div style="font-size: 0.9rem; color: #6B7280; margin-top: 0.2rem;">
                            {label}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            # Save to history
            history_entry = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'text_preview': input_text[:80] + "..." if len(input_text) > 80 else input_text,
                'overall_risk': risk_score,
                'pattern_count': results['pattern_count'],
                'patterns_detected': list(results['patterns_detected'].keys()),
                'word_count': metrics['word_count']
            }
            
            st.session_state.analysis_history.append(history_entry)
            
            # Success message
            st.success(f"✅ Analysis complete! Detected {results['pattern_count']} disinformation patterns with {risk_score:.1%} overall risk.")
            
            # Clear case title
            if 'case_title' in st.session_state:
                del st.session_state.case_title
    
    elif analyze_btn:
        st.error("❌ Please enter text to analyze (minimum 10 characters).")

with tab2:
    st.markdown("### 📚 Case Studies Library")
    st.caption("Study real examples of different information patterns")
    
    for i, case in enumerate(st.session_state.pattern_db['case_studies']):
        risk_color = "#DC2626" if case['risk_level'] == 'High' else "#F59E0B" if case['risk_level'] == 'Medium' else "#10B981"
        
        st.markdown(f'''
        <div class="scientific-card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <h3 style="margin: 0; color: #1F2937;">{case['title']}</h3>
                    <div style="display: flex; align-items: center; margin-top: 0.3rem;">
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: {risk_color}; margin-right: 0.5rem;"></div>
                        <span style="font-weight: 600; color: {risk_color};">{case['risk_level']} Risk</span>
                    </div>
                </div>
                <div>
                    <span class="metric-badge risk-medium">Pattern Analysis</span>
                </div>
            </div>
            
            <div style="background: #F8FAFC; border-radius: 8px; padding: 1rem; margin: 1rem 0; border: 1px solid #E2E8F0;">
                <div style="font-size: 0.9rem; color: #4B5563; font-style: italic;">
                    "{case['text']}"
                </div>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.9rem; color: #374151; font-weight: 600;">
                    🔍 Analysis Focus:
                </div>
                <div style="font-size: 0.9rem; color: #6B7280;">
                    {case['analysis_focus']}
                </div>
            </div>
            
            <div>
                <div style="font-size: 0.9rem; color: #374151; font-weight: 600;">
                    🎯 Detected Patterns:
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">
                    {''.join([f'<span class="metric-badge risk-high">{pattern.replace("_", " ").title()}</span>' for pattern in case['patterns']])}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🔬 Analyze This Case", key=f"analyze_case_{i}", use_container_width=True):
                st.session_state.analysis_text = case['text']
                st.session_state.case_title = case['title']
                st.rerun()
        with col2:
            if st.button(f"📋 Copy Text", key=f"copy_case_{i}", use_container_width=True):
                st.code(case['text'], language="text")
        
        st.divider()

with tab3:
    st.markdown("### 📈 System Dashboard")
    
    if not st.session_state.analysis_history:
        st.info("No analysis data available. Start analyzing texts to see statistics.")
    else:
        # Convert history to DataFrame for analysis
        df = pd.DataFrame(st.session_state.analysis_history)
        
        # Overall Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Analyses", len(df))
        with col2:
            avg_risk = df['overall_risk'].mean()
            st.metric("Average Risk", f"{avg_risk:.1%}")
        with col3:
            max_risk = df['overall_risk'].max()
            st.metric("Highest Risk", f"{max_risk:.1%}")
        with col4:
            avg_patterns = df['pattern_count'].mean()
            st.metric("Avg Patterns", f"{avg_patterns:.1f}")
        
        # Risk Distribution Chart
        st.markdown("#### 📊 Risk Score Distribution")
        
        fig = px.histogram(
            df,
            x='overall_risk',
            nbins=10,
            color_discrete_sequence=['#3B82F6'],
            opacity=0.8
        )
        
        fig.update_layout(
            xaxis_title="Risk Score",
            yaxis_title="Count",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Pattern Frequency
        st.markdown("#### 🔍 Most Common Patterns")
        
        # Flatten pattern lists
        all_patterns = []
        for patterns in df['patterns_detected']:
            all_patterns.extend(patterns)
        
        if all_patterns:
            pattern_counts = Counter(all_patterns)
            pattern_df = pd.DataFrame(
                pattern_counts.items(),
                columns=['Pattern', 'Count']
            ).sort_values('Count', ascending=True)
            
            fig = px.bar(
                pattern_df.tail(10),
                x='Count',
                y='Pattern',
                orientation='h',
                color='Count',
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Detection Count",
                yaxis_title="Pattern Type"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent Analyses
        st.markdown("#### 📝 Recent Analyses")
        
        for entry in st.session_state.analysis_history[-5:]:
            risk_color = "#DC2626" if entry['overall_risk'] > 0.7 else "#F59E0B" if entry['overall_risk'] > 0.4 else "#10B981"
            
            st.markdown(f'''
            <div style="padding: 1rem; border-radius: 8px; background: white; border: 1px solid #E5E7EB; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="font-weight: 600; color: #1F2937;">
                        {entry['timestamp']}
                    </div>
                    <div style="font-weight: 800; color: {risk_color};">
                        {entry['overall_risk']:.1%}
                    </div>
                </div>
                <div style="color: #6B7280; font-size: 0.9rem; margin-bottom: 0.5rem;">
                    {entry['text_preview']}
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #9CA3AF;">
                    <span>📊 {entry['word_count']} words</span>
                    <span>🔍 {entry['pattern_count']} patterns</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Export Data
        st.markdown("---")
        st.markdown("#### 📥 Export Data")
        
        if st.button("Export Analysis Data as CSV", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="pattern_analysis_data.csv",
                mime="text/csv"
            )

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**🔍 Pattern Recognition**")
    st.caption("Advanced disinformation detection")

with footer_col2:
    st.markdown("**⚡ Real-time Analysis**")
    st.caption("Instant pattern identification")

with footer_col3:
    st.markdown("**🎓 Educational Tool**")
    st.caption("For research and analysis")

st.markdown("---")

st.caption("""
© 2024 Disinformation Pattern Recognition System | Version 2.1 | 
This system is designed for educational and research purposes to identify common patterns in information dissemination.
Always verify information through multiple credible sources.
""")