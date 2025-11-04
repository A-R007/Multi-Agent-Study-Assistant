# 🏗️ Architecture Overview

## Multi-Agent System Design

This project implements a **multi-agent architecture** where specialized AI agents collaborate to provide comprehensive learning assistance. Each agent has a specific role and expertise.

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web App                       │
│                        (app.py)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Agent Handler                              │
│              (agent_handler.py)                             │
│  • Orchestrates agent workflows                             │
│  • Manages state and context                                │
│  • Coordinates multi-agent collaboration                    │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        ▼            ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│   Student    │ │ Roadmap  │ │   Quiz   │ │    Tutor     │
│   Analyzer   │ │ Creator  │ │Generator │ │    Agent     │
│    Agent     │ │  Agent   │ │  Agent   │ │              │
└──────────────┘ └──────────┘ └──────────┘ └──────────────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │     Study Agents           │
        │   (study_agents.py)        │
        │  • Agent definitions       │
        │  • Persona management      │
        │  • Model configuration     │
        └────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌───────────────┐
│   Config     │ │ Prompts  │ │  RAG Helper   │
│   Manager    │ │  YAML    │ │               │
│ (config.py)  │ │          │ │(rag_helper.py)│
└──────────────┘ └──────────┘ └───────────────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │   ChromaDB   │
                              │ Vector Store │
                              └──────────────┘
```

## 🤖 Agent Roles & Responsibilities

### 1. Student Analyzer Agent
**Purpose**: Assess learning needs and create student profile

**Capabilities**:
- Analyzes current knowledge level
- Identifies learning gaps
- Determines prerequisites
- Recommends learning approaches
- Evaluates time constraints

**Input**: Student information (topic, level, goals, time, style)
**Output**: Comprehensive student analysis report

**Temperature**: 0.6 (balanced creativity and consistency)

---

### 2. Roadmap Creator Agent
**Purpose**: Design personalized learning paths

**Capabilities**:
- Creates structured learning phases
- Sequences topics logically
- Estimates time requirements
- Sets milestones and checkpoints
- Adapts to learning styles

**Input**: Student analysis, goals, constraints
**Output**: Detailed learning roadmap with phases

**Temperature**: 0.7 (creative planning)

---

### 3. Quiz Generator Agent
**Purpose**: Create adaptive assessments

**Capabilities**:
- Generates multiple question types
- Adapts difficulty levels
- Provides detailed explanations
- Tests conceptual and practical knowledge
- Focuses on specific areas

**Input**: Topic, difficulty, focus areas, question count
**Output**: Complete quiz with answers and explanations

**Temperature**: 0.5 (consistent question quality)

---

### 4. Tutor Agent
**Purpose**: Explain concepts and answer questions

**Capabilities**:
- Breaks down complex concepts
- Uses analogies and examples
- Adapts to learning styles
- Provides step-by-step guidance
- Encourages critical thinking

**Input**: Student question, context, knowledge level
**Output**: Clear, personalized explanation

**Temperature**: 0.7 (engaging explanations)

---

### 5. Resource Finder Agent
**Purpose**: Search and recommend learning materials

**Capabilities**:
- Searches web for resources
- Evaluates quality and relevance
- Matches to learning styles
- Finds diverse resource types
- Prioritizes free resources

**Tools**: DuckDuckGo search
**Input**: Topic, goals, level, learning style
**Output**: Curated resource list

**Temperature**: 0.6 (balanced search)

---

### 6. RAG Tutor Agent
**Purpose**: Answer questions using uploaded documents

**Capabilities**:
- Retrieves relevant document context
- Grounds answers in source material
- Cites specific sections
- Acknowledges information gaps
- Provides accurate, contextual answers

**Tools**: Vector database (ChromaDB)
**Input**: Question, document context
**Output**: Answer with source citations

**Temperature**: 0.6 (accurate retrieval)

## 🔄 Workflow Patterns

### Pattern 1: Initial Learning Plan Creation
```
User Input → Student Analyzer → Roadmap Creator → Resource Finder → Dashboard
```

**Steps**:
1. User provides learning goals and constraints
2. Student Analyzer assesses needs and gaps
3. Roadmap Creator designs learning path using analysis
4. Resource Finder searches for materials
5. Results displayed in dashboard

**Time**: ~30-60 seconds

---

### Pattern 2: Quiz Generation
```
User Request → Quiz Generator → Display Quiz
```

**Steps**:
1. User specifies difficulty, focus, and count
2. Quiz Generator creates questions with explanations
3. Quiz displayed with download option

**Time**: ~10-20 seconds

---

### Pattern 3: Tutoring Session
```
User Question → Tutor Agent → Explanation
```

**Steps**:
1. User asks question with optional context
2. Tutor Agent formulates personalized explanation
3. Response displayed with examples

**Time**: ~5-15 seconds

---

### Pattern 4: RAG Document Q&A
```
User Upload → Document Processing → Vector Storage
User Question → Similarity Search → Context Retrieval → RAG Tutor → Answer
```

**Steps**:
1. User uploads PDF/text documents
2. Documents split into chunks and embedded
3. Chunks stored in ChromaDB vector database
4. User asks question
5. Similarity search finds relevant chunks
6. RAG Tutor generates answer using context
7. Answer displayed with citations

**Time**: Upload ~2-5 seconds per doc, Query ~10-20 seconds

## 🧩 Component Details

### Agent Handler (`agent_handler.py`)
**Role**: Orchestration layer

**Responsibilities**:
- Initializes agents with proper configuration
- Manages agent execution order
- Handles state between agent calls
- Formats prompts with context
- Integrates RAG functionality
- Manages Streamlit status updates

**Key Methods**:
- `analyze_student()`: Runs student analysis workflow
- `create_roadmap()`: Runs roadmap creation workflow
- `generate_quiz()`: Runs quiz generation workflow
- `get_tutoring()`: Single tutor interaction
- `query_documents()`: RAG-powered document Q&A

---

### Study Agents (`study_agents.py`)
**Role**: Agent factory

**Responsibilities**:
- Defines agent configurations
- Loads personas from YAML
- Configures models (OpenAI/Groq)
- Sets appropriate temperatures
- Manages learning style adaptations

**Key Methods**:
- `student_analyzer_agent()`: Creates analyzer
- `roadmap_creator_agent()`: Creates roadmap designer
- `quiz_generator_agent()`: Creates quiz maker
- `tutor_agent()`: Creates tutor
- `resource_finder_agent()`: Creates resource searcher
- `rag_tutor_agent()`: Creates RAG-enabled tutor

---

### RAG Helper (`rag_helper.py`)
**Role**: Document processing and retrieval

**Responsibilities**:
- Loads and processes documents
- Splits text into chunks
- Creates embeddings
- Manages vector database
- Performs similarity search

**Key Methods**:
- `load_pdf()`: Process PDF files
- `load_text()`: Process text files
- `query()`: Retrieve relevant chunks
- `clear_database()`: Reset vector store

**Technology Stack**:
- **LangChain**: Document processing
- **ChromaDB**: Vector storage
- **OpenAI Embeddings**: Text embeddings
- **RecursiveCharacterTextSplitter**: Chunking

---

### Config Manager (`config.py`)
**Role**: Configuration access

**Responsibilities**:
- Loads YAML configuration
- Provides persona definitions
- Manages prompt templates
- Supplies learning style info
- Formats prompts with variables

**Singleton Pattern**: Ensures single config instance

---

### Prompts YAML (`prompts.yaml`)
**Role**: Configuration and prompts

**Contains**:
- **Personas**: Agent system prompts and capabilities
- **Prompts**: Task-specific prompt templates
- **Learning Styles**: Style descriptions and recommendations
- **Subject Categories**: Topic lists and durations
- **Knowledge Levels**: Level definitions and approaches

## 🔧 Technology Stack

### Core Framework
- **Phidata**: Multi-agent orchestration
- **Streamlit**: Web interface
- **Python 3.10+**: Runtime

### AI/ML
- **OpenAI GPT-4**: High-quality LLM (paid)
- **Groq Llama**: Fast, free LLM
- **LangChain**: Document processing
- **ChromaDB**: Vector database
- **OpenAI Embeddings**: Text embeddings

### Tools
- **DuckDuckGo**: Web search
- **PyPDF**: PDF processing
- **YAML**: Configuration
- **python-dotenv**: Environment management

## 🎯 Design Principles

### 1. Separation of Concerns
Each component has a single, well-defined responsibility:
- Agents: AI capabilities
- Handler: Orchestration
- RAG Helper: Document processing
- Config: Configuration management
- App: User interface

### 2. Modularity
Components are loosely coupled and can be:
- Modified independently
- Tested in isolation
- Reused in different contexts
- Extended with new features

### 3. Configurability
Behavior controlled through:
- YAML configuration files
- Environment variables
- Runtime parameters
- User preferences

### 4. Scalability
Architecture supports:
- Adding new agents
- New learning styles
- Additional subject categories
- More document types
- Different LLM providers

### 5. User-Centric
Design prioritizes:
- Clear user workflows
- Immediate feedback
- Progress visibility
- Error handling
- Helpful guidance

## 📈 Performance Considerations

### Response Times
- **Student Analysis**: 10-15 seconds
- **Roadmap Creation**: 15-20 seconds
- **Resource Finding**: 10-15 seconds (with web search)
- **Quiz Generation**: 10-15 seconds
- **Tutoring**: 5-10 seconds
- **RAG Query**: 10-15 seconds

### Optimization Strategies
1. **Model Selection**: Groq for speed, GPT-4 for quality
2. **Temperature Tuning**: Lower for consistency, higher for creativity
3. **Prompt Engineering**: Clear, specific instructions
4. **Caching**: Streamlit session state for results
5. **Chunking**: Optimal chunk size for RAG (1000 chars)

## 🔐 Security Considerations

### API Keys
- Stored in `.env` file (not in code)
- Never committed to version control
- Loaded via python-dotenv

### User Data
- Session-based (not persisted)
- Vector DB local to user
- No external data transmission (except API calls)

### File Uploads
- Temporary storage only
- Cleaned up after processing
- Size limits recommended

## 🚀 Extension Points

### Easy to Add
1. **New Agents**: Add to `study_agents.py`
2. **New Prompts**: Add to `prompts.yaml`
3. **New Learning Styles**: Add to YAML config
4. **New Subject Categories**: Add to YAML config
5. **New LLM Providers**: Add to `_get_model()`

### Moderate Effort
1. **Progress Tracking**: Add database layer
2. **User Accounts**: Add authentication
3. **Collaborative Features**: Add real-time sync
4. **Mobile App**: Create React Native version
5. **Analytics Dashboard**: Add metrics collection

### Complex
1. **Spaced Repetition**: Implement scheduling algorithm
2. **Voice Interaction**: Add speech recognition/synthesis
3. **Live Tutoring**: Add real-time video/chat
4. **Platform Integration**: Connect to Coursera, Udemy, etc.
5. **Adaptive Learning**: ML-based difficulty adjustment

## 📚 Further Reading

- [Phidata Documentation](https://docs.phidata.com/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)

---

**This architecture enables a powerful, flexible, and extensible learning platform that adapts to each student's unique needs!**
