# 🚀 Quick Start Guide

Get up and running with the Multi-Agent Study Assistant in 5 minutes!

## ⚡ Fast Setup (3 Steps)

### 1️⃣ Get an API Key (Free!)

**Option A: Groq (Recommended - Free & Fast)**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Create an API key
4. Copy the key

**Option B: OpenAI (Paid)**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up and add payment method
3. Create an API key
4. Copy the key

### 2️⃣ Install & Configure

**Automatic Setup (Linux/Mac):**
```bash
cd Multi-Agent-Study-Assistant
chmod +x setup.sh
./setup.sh
```

**Manual Setup:**
```bash
cd Multi-Agent-Study-Assistant

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your favorite editor
```

Add your key to `.env`:
```bash
# For Groq (free)
GROQ_API_KEY=your_groq_api_key_here

# OR for OpenAI (paid)
OPENAI_API_KEY=your_openai_api_key_here
```

### 3️⃣ Run the App

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

## 🎯 First Time Usage

### Step 1: Choose Your Subject
Click on a category:
- 💻 Programming
- 🔢 Mathematics
- 🔬 Science
- 🌍 Languages
- 💼 Business
- 📝 Test Preparation

### Step 2: Set Your Goals
Fill in:
- **Topic**: What you want to learn (e.g., "Python for Data Science")
- **Knowledge Level**: Beginner, Intermediate, Advanced, or Expert
- **Learning Goal**: What you want to achieve (e.g., "Build ML projects")
- **Time Available**: How many hours per week
- **Learning Style**: Visual, Auditory, Kinesthetic, or Reading/Writing

### Step 3: Get Your Plan
Click "Create My Learning Plan" and wait ~30 seconds while AI agents:
- Analyze your needs
- Create a custom roadmap
- Find the best resources

### Step 4: Start Learning!
Use the dashboard tabs:
- 📋 **Roadmap**: Your personalized learning path
- 📚 **Resources**: Curated learning materials
- ❓ **Quiz**: Generate practice questions
- 🤖 **Tutor**: Ask questions anytime
- 📄 **Documents**: Upload materials for Q&A

## 💡 Pro Tips

### For Best Results:
1. **Be specific** with your learning goals
2. **Upload your textbooks** to the Document Q&A tab
3. **Take quizzes regularly** to test understanding
4. **Ask the tutor** when stuck - it's like having a personal teacher!

### Example Learning Goals:
- ✅ "Build 3 portfolio projects using React"
- ✅ "Pass the AWS Solutions Architect exam"
- ✅ "Understand calculus well enough to take physics"
- ❌ "Learn programming" (too vague)

### Time Commitments:
- **1-2 hours/week**: Casual learning, 3-6 months per topic
- **3-5 hours/week**: Steady progress, 2-3 months per topic
- **6-10 hours/week**: Fast learning, 1-2 months per topic
- **10+ hours/week**: Intensive, 2-4 weeks per topic

## 🎓 Feature Highlights

### 📋 Learning Roadmap
- Structured into phases (Foundation → Intermediate → Advanced)
- Clear milestones and checkpoints
- Time estimates for each phase
- Download as markdown for offline reference

### 📚 Resource Finder
- AI searches for best learning materials
- Includes: courses, videos, books, articles, practice platforms
- Filtered by quality and relevance
- Matched to your learning style

### ❓ Quiz Generator
- Adaptive difficulty (beginner to advanced)
- Multiple question types
- Detailed explanations for each answer
- Focus on specific topics or general coverage
- 5-20 questions per quiz

### 🤖 AI Tutor
- Available 24/7
- Explains concepts in your learning style
- Step-by-step problem solving
- Real-world examples and analogies
- Patient and never judges!

### 📄 Document Q&A (RAG)
- Upload PDFs or text files
- Ask questions about your materials
- Get answers with source citations
- Perfect for textbooks, lecture notes, papers
- Supports multiple documents

## 🔧 Troubleshooting

### App won't start
```bash
# Check if streamlit is installed
streamlit --version

# If not, install it
pip install streamlit
```

### "No API key found"
1. Make sure `.env` file exists in the project folder
2. Open `.env` and verify your API key is there
3. No quotes needed around the key
4. Restart the app after editing `.env`

### Slow responses
- Try switching to Groq (faster than OpenAI)
- Use a smaller model (e.g., `llama-3.1-70b-versatile`)
- Check your internet connection

### Document upload fails
- Ensure PDF is not password-protected
- Try a smaller file (< 10MB)
- Convert to text format if issues persist

## 📊 Example Workflow

**Learning Python for Data Science:**

1. **Initial Setup** (5 min)
   - Category: Programming
   - Topic: "Python for Data Science"
   - Level: Beginner
   - Goal: "Build data analysis projects"
   - Time: 5-10 hours/week

2. **Week 1-2: Foundation**
   - Follow roadmap Phase 1
   - Watch recommended video courses
   - Take beginner quiz
   - Ask tutor about confusing concepts

3. **Week 3-4: Practice**
   - Upload Python textbook to Document Q&A
   - Work through roadmap Phase 2
   - Take intermediate quiz
   - Ask tutor for project ideas

4. **Week 5-6: Projects**
   - Follow roadmap Phase 3
   - Build portfolio projects
   - Take advanced quiz
   - Use tutor for debugging help

5. **Week 7-8: Mastery**
   - Complete final roadmap phase
   - Upload data science papers
   - Query documents for advanced topics
   - Take expert-level quiz

## 🎯 Learning Style Guide

### Visual Learners
- Focus on video resources
- Create mind maps from roadmap
- Use diagram-heavy materials
- Ask tutor for visual explanations

### Auditory Learners
- Prioritize podcast/audio resources
- Read roadmap aloud
- Discuss with AI tutor frequently
- Join study groups (external)

### Kinesthetic Learners
- Start projects immediately
- Practice with every concept
- Use interactive coding platforms
- Build while learning

### Reading/Writing Learners
- Take detailed notes from roadmap
- Write summaries after each phase
- Use text-based resources
- Document your learning journey

## 🚀 Advanced Features

### Custom Quiz Focus
```
Focus Areas: "loops, functions, list comprehensions"
Difficulty: Intermediate
Questions: 15
```

### Effective Tutor Questions
- ✅ "Can you explain recursion with a real-world analogy?"
- ✅ "I don't understand why this code fails: [paste code]"
- ✅ "What's the difference between X and Y?"
- ❌ "Teach me everything about Python" (too broad)

### RAG Document Tips
- Upload chapter-by-chapter for better results
- Ask specific questions: "What does chapter 3 say about X?"
- Reference page numbers when possible
- Upload practice problems with solutions

## 📈 Track Your Progress

Create a learning journal:
1. Download your roadmap
2. Check off completed phases
3. Note quiz scores
4. Save tutor conversations
5. Track time spent

## 🎉 Success Stories

**"Went from zero to building ML models in 8 weeks!"**
- Used 10+ hours/week
- Followed roadmap religiously
- Took quizzes every weekend
- Asked tutor 50+ questions

**"Passed AWS cert on first try!"**
- Uploaded all study materials to RAG
- Generated 100+ practice questions
- Used roadmap for structured study
- 6 weeks of focused learning

## 🆘 Need Help?

1. Check the main [README.md](README.md)
2. Review troubleshooting section above
3. Verify `.env` configuration
4. Try different models/providers
5. Check API key has credits (OpenAI)

## 🎊 You're Ready!

Now you have everything you need to start your learning journey. The AI agents are ready to help you achieve your goals!

**Remember**: Consistent small steps beat sporadic big efforts. Use the roadmap, trust the process, and ask questions freely!

---

**Happy Learning! 📚✨**
