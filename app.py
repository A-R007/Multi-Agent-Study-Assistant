import streamlit as st
from dotenv import load_dotenv
from agent_handler import StudyAssistantHandler
from config import ConfigManager
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="AI Study Assistant", layout="wide", page_icon="📚")
st.title("📚 Multi-Agent AI Study Assistant")
st.markdown("Personalized learning with AI agents - Analysis, Roadmaps, Quizzes & RAG-powered Tutoring!")

# Initialize config manager
config_manager = ConfigManager()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Provider selection
    provider = st.selectbox(
        "AI Provider",
        ["groq", "openai"],
        index=0,
        help="Groq is free and fast. OpenAI requires paid API key."
    )
    
    # Model selection based on provider
    if provider == "groq":
        model_options = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]
        selected_model = st.selectbox("Select Model", model_options, index=0)
    else:
        model_options = ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo"]
        selected_model = st.selectbox("Select Model", model_options, index=0)
    
    st.divider()
    
    st.subheader("📖 About")
    st.markdown("""
    This AI Study Assistant uses multiple specialized agents to:
    - **Analyze** your learning needs
    - **Create** personalized roadmaps
    - **Generate** custom quizzes
    - **Tutor** you with RAG assistance
    - **Find** the best learning resources
    
    **Groq**: Free, fast inference (recommended)  
    **OpenAI**: Requires paid API key
    """)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "subject_category" not in st.session_state:
    st.session_state.subject_category = None
if "topic" not in st.session_state:
    st.session_state.topic = None
if "knowledge_level" not in st.session_state:
    st.session_state.knowledge_level = None
if "learning_goal" not in st.session_state:
    st.session_state.learning_goal = None
if "time_available" not in st.session_state:
    st.session_state.time_available = None
if "learning_style" not in st.session_state:
    st.session_state.learning_style = None
if "student_analysis" not in st.session_state:
    st.session_state.student_analysis = None
if "learning_roadmap" not in st.session_state:
    st.session_state.learning_roadmap = None
if "learning_resources" not in st.session_state:
    st.session_state.learning_resources = None
if "handler" not in st.session_state:
    st.session_state.handler = None
if "uploaded_files_count" not in st.session_state:
    st.session_state.uploaded_files_count = 0

# Step 1: Choose Subject Category
if st.session_state.step == 1:
    st.header("Step 1: Choose Your Subject Category")
    
    categories = config_manager.get_all_subject_categories()
    category_display = {
        "programming": "💻 Programming",
        "mathematics": "🔢 Mathematics",
        "science": "🔬 Science",
        "languages": "🌍 Languages",
        "business": "💼 Business",
        "test_preparation": "📝 Test Preparation"
    }
    
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            display_name = category_display.get(category, category.title())
            if st.button(display_name, use_container_width=True, key=f"cat_{category}"):
                st.session_state.subject_category = category
                st.session_state.step = 2
                st.rerun()

# Step 2: Enter Topic and Learning Details
elif st.session_state.step == 2:
    st.header("Step 2: Tell Us About Your Learning Goals")
    st.subheader(f"Category: {st.session_state.subject_category.title()}")
    
    # Show category info
    category_info = config_manager.get_subject_category_info(st.session_state.subject_category)
    if category_info:
        with st.expander("ℹ️ About this category"):
            st.write(f"**Topics include:** {', '.join(category_info.get('topics', []))}")
            st.write(f"**Typical Duration:** {category_info.get('typical_duration', 'Varies')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "What specific topic do you want to learn?",
            placeholder="e.g., Python for Data Science, Calculus, Spanish Grammar"
        )
        
        knowledge_levels = config_manager.get_all_knowledge_levels()
        knowledge_level = st.selectbox(
            "What's your current knowledge level?",
            knowledge_levels,
            format_func=lambda x: x.title()
        )
        
        # Show knowledge level info
        level_info = config_manager.get_knowledge_level_info(knowledge_level)
        if level_info:
            st.info(f"**{knowledge_level.title()}:** {level_info.get('description', '')}")
    
    with col2:
        learning_goal = st.text_area(
            "What do you want to achieve?",
            placeholder="e.g., Build a portfolio project, Pass an exam, Get job-ready",
            height=100
        )
        
        time_available = st.selectbox(
            "How much time can you dedicate?",
            ["1-2 hours per week", "3-5 hours per week", "6-10 hours per week", 
             "10+ hours per week", "Full-time (30+ hours per week)"]
        )
        
        learning_styles = config_manager.get_all_learning_styles()
        learning_style = st.selectbox(
            "What's your preferred learning style?",
            learning_styles,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        # Show learning style info
        style_info = config_manager.get_learning_style_info(learning_style)
        if style_info:
            st.info(f"**{learning_style.replace('_', ' ').title()}:** {style_info.get('description', '')}")
    
    col_back, col_next = st.columns([1, 5])
    with col_back:
        if st.button("← Back", type="secondary"):
            st.session_state.step = 1
            st.rerun()
    with col_next:
        if st.button("Create My Learning Plan", type="primary", 
                    disabled=not (topic and learning_goal)):
            st.session_state.topic = topic
            st.session_state.knowledge_level = knowledge_level
            st.session_state.learning_goal = learning_goal
            st.session_state.time_available = time_available
            st.session_state.learning_style = learning_style
            st.session_state.step = 3
            st.rerun()

# Step 3: Generate Analysis and Roadmap
elif st.session_state.step == 3:
    st.header("Creating Your Personalized Learning Plan")
    st.subheader(f"Topic: {st.session_state.topic}")
    
    # Initialize handler
    if not st.session_state.handler:
        st.session_state.handler = StudyAssistantHandler(
            topic=st.session_state.topic,
            subject_category=st.session_state.subject_category,
            knowledge_level=st.session_state.knowledge_level,
            learning_goal=st.session_state.learning_goal,
            time_available=st.session_state.time_available,
            learning_style=st.session_state.learning_style,
            model_name=selected_model,
            provider=provider
        )
    
    # Analyze student
    if not st.session_state.student_analysis:
        analysis_results = st.session_state.handler.analyze_student()
    
    # Create roadmap
    if st.session_state.student_analysis and not st.session_state.learning_roadmap:
        roadmap_results = st.session_state.handler.create_roadmap(
            st.session_state.student_analysis
        )
    
    # Find resources
    if st.session_state.learning_roadmap and not st.session_state.learning_resources:
        resource_results = st.session_state.handler.find_resources()
    
    # Move to dashboard when complete
    if (st.session_state.student_analysis and 
        st.session_state.learning_roadmap and 
        st.session_state.learning_resources):
        st.session_state.step = 4
        st.rerun()

# Step 4: Learning Dashboard
elif st.session_state.step == 4:
    st.header("🎯 Your Learning Dashboard")
    
    # Create tabs for different features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Learning Roadmap", 
        "📚 Resources", 
        "❓ Quiz Generator",
        "🤖 AI Tutor",
        "📄 Document Q&A (RAG)"
    ])
    
    # Tab 1: Learning Roadmap
    with tab1:
        st.subheader("Your Personalized Learning Roadmap")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"**Topic:** {st.session_state.topic} | **Level:** {st.session_state.knowledge_level.title()}")
        with col2:
            if st.button("🔄 Regenerate Roadmap"):
                st.session_state.learning_roadmap = None
                roadmap_results = st.session_state.handler.create_roadmap(
                    st.session_state.student_analysis
                )
                st.rerun()
        
        st.markdown(st.session_state.learning_roadmap)
        
        with st.expander("📊 View Student Analysis"):
            st.markdown(st.session_state.student_analysis)
        
        st.download_button(
            label="📥 Download Roadmap",
            data=f"# Learning Roadmap: {st.session_state.topic}\n\n{st.session_state.learning_roadmap}",
            file_name=f"roadmap_{st.session_state.topic.replace(' ', '_')}.md",
            mime="text/markdown"
        )
    
    # Tab 2: Resources
    with tab2:
        st.subheader("Recommended Learning Resources")
        
        if st.button("🔄 Find New Resources"):
            st.session_state.learning_resources = None
            resource_results = st.session_state.handler.find_resources()
            st.rerun()
        
        st.markdown(st.session_state.learning_resources)
        
        st.download_button(
            label="📥 Download Resources",
            data=f"# Learning Resources: {st.session_state.topic}\n\n{st.session_state.learning_resources}",
            file_name=f"resources_{st.session_state.topic.replace(' ', '_')}.md",
            mime="text/markdown"
        )
    
    # Tab 3: Quiz Generator
    with tab3:
        st.subheader("Generate Practice Quizzes")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            difficulty = st.selectbox(
                "Difficulty Level",
                ["beginner", "intermediate", "advanced"],
                index=1
            )
        with col2:
            num_questions = st.slider("Number of Questions", 5, 20, 10)
        with col3:
            focus_areas = st.text_input(
                "Focus Areas (optional)",
                placeholder="e.g., loops, functions"
            )
        
        if st.button("🎲 Generate Quiz", type="primary"):
            with st.spinner("Generating quiz..."):
                quiz_results = st.session_state.handler.generate_quiz(
                    difficulty_level=difficulty,
                    focus_areas=focus_areas if focus_areas else "general",
                    num_questions=num_questions
                )
                st.session_state.current_quiz = quiz_results["quiz"]
        
        if "current_quiz" in st.session_state and st.session_state.current_quiz:
            st.markdown(st.session_state.current_quiz)
            
            st.download_button(
                label="📥 Download Quiz",
                data=f"# Quiz: {st.session_state.topic}\n\n{st.session_state.current_quiz}",
                file_name=f"quiz_{st.session_state.topic.replace(' ', '_')}.md",
                mime="text/markdown"
            )
    
    # Tab 4: AI Tutor
    with tab4:
        st.subheader("Ask Your AI Tutor")
        st.write("Get personalized explanations and help with your questions.")
        
        question = st.text_area(
            "What would you like help with?",
            placeholder="e.g., Can you explain recursion with an example?",
            height=100
        )
        
        context = st.text_input(
            "Additional context (optional)",
            placeholder="e.g., I'm working on a specific problem..."
        )
        
        if st.button("💬 Ask Tutor", type="primary", disabled=not question):
            with st.spinner("Thinking..."):
                response = st.session_state.handler.get_tutoring(question, context)
                st.session_state.tutor_response = response
        
        if "tutor_response" in st.session_state and st.session_state.tutor_response:
            st.markdown("### 🤖 Tutor Response:")
            st.markdown(st.session_state.tutor_response)
    
    # Tab 5: Document Q&A (RAG)
    with tab5:
        st.subheader("Upload Study Materials & Ask Questions")
        st.write("Upload PDFs or text files and ask questions about them using RAG technology.")
        
        # File upload section
        col1, col2 = st.columns([2, 1])
        with col1:
            uploaded_files = st.file_uploader(
                "Upload study materials (PDF or TXT)",
                type=["pdf", "txt"],
                accept_multiple_files=True
            )
        
        with col2:
            if st.session_state.handler:
                doc_count = st.session_state.handler.get_document_count()
                st.metric("Documents Loaded", doc_count)
                
                if doc_count > 0 and st.button("🗑️ Clear All Documents"):
                    st.session_state.handler.clear_documents()
                    st.session_state.uploaded_files_count = 0
                    st.success("Documents cleared!")
                    st.rerun()
        
        # Process uploaded files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save file temporarily
                temp_path = f"./temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Add to RAG
                file_type = "pdf" if uploaded_file.name.endswith(".pdf") else "text"
                success = st.session_state.handler.add_document_to_rag(temp_path, file_type)
                
                if success:
                    st.success(f"✅ Loaded: {uploaded_file.name}")
                    st.session_state.uploaded_files_count += 1
                else:
                    st.error(f"❌ Failed to load: {uploaded_file.name}")
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        st.divider()
        
        # Question answering section
        if st.session_state.handler and st.session_state.handler.get_document_count() > 0:
            st.markdown("### 💡 Ask Questions About Your Documents")
            
            doc_question = st.text_area(
                "What would you like to know?",
                placeholder="e.g., What are the key concepts in chapter 3?",
                height=100,
                key="doc_question"
            )
            
            if st.button("🔍 Search Documents", type="primary", disabled=not doc_question):
                with st.spinner("Searching documents..."):
                    answer = st.session_state.handler.query_documents(doc_question)
                    st.session_state.rag_answer = answer
            
            if "rag_answer" in st.session_state and st.session_state.rag_answer:
                st.markdown("### 📖 Answer from Your Documents:")
                st.markdown(st.session_state.rag_answer)
        else:
            st.info("📤 Upload documents above to start asking questions!")
    
    # Bottom navigation
    st.divider()
    if st.button("🏠 Start New Learning Plan"):
        # Clear session state
        keys_to_clear = [k for k in st.session_state.keys() if k != "step"]
        for key in keys_to_clear:
            del st.session_state[key]
        st.session_state.step = 1
        st.rerun()

if __name__ == "__main__":
    pass
