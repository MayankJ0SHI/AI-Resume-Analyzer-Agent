# 🤖 AI Resume Analyzer Agent

An AI-powered resume analysis system built using **LangGraph, LangChain,
OpenAI LLMs, and Pydantic structured outputs**.

The application analyzes a candidate resume against a job description,
evaluates ATS compatibility, identifies skill gaps, generates
improvement recommendations, and creates a professional AI-generated
resume analysis report.

------------------------------------------------------------------------

## 🚀 Features

### 📄 Resume Intelligence Pipeline

-   Extracts resume content from PDF documents
-   Parses candidate information using LLM structured extraction
-   Identifies:
    -   Candidate name
    -   Experience summary
    -   Total experience
    -   Technical skills
    -   Tools
    -   Domain knowledge
    -   Projects and impact

### 💼 Job Description Analysis

Extracts important job requirements:

-   Job title
-   Company information
-   Required experience
-   Skills and technologies
-   Responsibilities
-   Qualifications

### 🎯 ATS Compatibility Evaluation

The AI evaluator analyzes:

-   Skill matching
-   Missing skills
-   Keyword alignment
-   Experience relevance
-   Project relevance

Generates:

-   ATS score (0-100)
-   Detailed reasoning
-   Match analysis

### 🚀 AI Resume Improvement Recommendations

Generates actionable recommendations:

Categories:

-   Skill gaps
-   Resume improvements
-   Project improvements
-   Keyword optimization
-   Experience alignment

Each recommendation includes:

-   Priority level
-   Impact area
-   Suggested improvement

### 📊 Professional Report Generation

Creates an interactive terminal report containing:

-   Candidate overview
-   ATS score visualization
-   Skill analysis
-   Strengths
-   Improvement areas
-   AI recommendations
-   Final assessment

------------------------------------------------------------------------

# 🏗️ Architecture

The project uses a LangGraph multi-node workflow.

    START

     |
     v

    Resume Pre Processor
     |
     +----------------+
     |                |
     v                v

    Resume Content   Job Description
    Extractor        Extractor

     |                |
     +-------+--------+

             v

     ATS Evaluator

             v

     Recommendation Generator

             v

     Report Generator

             v

            END

------------------------------------------------------------------------

# 🧩 LangGraph Nodes

## 1. Resume Pre Processor

Responsible for:

-   Reading resume files
-   Extracting raw text
-   Preparing content for LLM processing

## 2. Resume Content Extractor

Uses LLM structured extraction to identify:

-   Candidate details
-   Skills
-   Projects
-   Experience

## 3. Job Description Extractor

Extracts:

-   Required skills
-   Responsibilities
-   Experience requirements

## 4. ATS Evaluator

Compares:

Resume vs Job Description

Produces:

-   Matched skills
-   Missing skills
-   ATS score
-   Evaluation reasoning

## 5. Recommendation Generator

Generates personalized resume improvement suggestions.

## 6. Report Generator

Creates the final AI Resume Analysis Report.

------------------------------------------------------------------------

# 📂 Project Structure

    AI-RESUME-ANALYZER-AGENT

    │
    ├── components
    │   ├── ats_evaluator.py
    │   ├── job_description_extraction.py
    │   ├── recommendation_engine.py
    │   ├── report_generator.py
    │   ├── resume_extraction.py
    │   └── resume_processing.py
    │
    ├── nodes
    │   ├── ats_evaluator_node.py
    │   ├── final_report_node.py
    │   ├── jd_extractor_node.py
    │   ├── recommendations_node.py
    │   ├── resume_content_extractor_node.py
    │   └── resume_processor_node.py
    │
    ├── schemas
    │   └── resume_analyze_state_schema.py
    │
    ├── utils
    │   ├── config_loader.py
    │   ├── llm_loader.py
    │   └── report_display.py
    │
    ├── resume
    │   └── candidate_resume.pdf
    │
    ├── config
    │   └── config.yaml
    │
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

# 🛠️ Tech Stack

## AI / LLM

-   LangChain
-   LangGraph
-   OpenAI APIs
-   Pydantic Structured Outputs

## Backend

-   Python
-   PDF Processing

## Development

-   VS Code
-   Jupyter Notebook

------------------------------------------------------------------------

# ⚙️ Installation

Clone repository:

``` bash
git clone <repository-url>

cd AI-RESUME-ANALYZER-AGENT
```

Create virtual environment:

``` bash
python -m venv myenv
```

Activate environment:

Windows:

``` bash
myenv\Scripts\activate
```

Linux/Mac:

``` bash
source myenv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 🔑 Environment Setup

Create `.env`

Example:

    OPENAI_API_KEY=your_api_key

------------------------------------------------------------------------

# ▶️ Running the Application

The complete workflow can be executed from the notebook:

    notebooks/prototype.ipynb

Execution flow:

1.  Load configuration

``` python
config = load_config(CONFIG_PATH)
```

2.  Initialize LLM

``` python
llm = load_llm(config)
```

3.  Build LangGraph workflow

``` python
graph = builder.compile()
```

4.  Provide inputs

``` python
result = graph.invoke(
{
    "resume_path": "resume/candidate.pdf",
    "job_description": "Job description text"
}
)
```

5.  Generate report

``` python
display_resume_report(
    result["final_report"]
)
```

------------------------------------------------------------------------

# 📈 Example Output

The generated AI Resume Analyzer report:

```text
┌──────────────────────────────────────────────┐
│                                              │
│ 🤖 AI Resume Analyzer Report                 │
│                                              │
│ 📄 Resume Intelligence Report                │
│ 🎯 ATS Compatibility Analysis                │
│ 🚀 Career Improvement Suggestions            │
│                                              │
└──────────────────────────────────────────────┘


👤 Candidate Overview
──────────────────────────────────────────────

🧑 Name        : MAYANK JOSHI

💼 Experience  : 4.0 years

📝 Profile:
MAYANK JOSHI is a GenAI Engineer with 4.10 years
of experience in software engineering, focusing
on production-grade LLM applications, Agentic AI
systems, and Retrieval-Augmented Generation (RAG)
pipelines.

He has worked on AI-powered applications and
automation frameworks using modern technologies.


🎯 ATS Compatibility Score
──────────────────────────────────────────────

Overall ATS Score

███████░░░ 73.0 / 100


📌 Analysis:

The candidate has 4.10 years of experience,
exceeding the required experience level.

Strong alignment was found in:

✅ Python
✅ Docker
✅ FastAPI
✅ Agentic AI
✅ LLM Applications


Missing important job requirements:

❌ AI/ML
❌ REST APIs
❌ Flask
❌ Django REST
❌ AWS
❌ Azure
❌ GCP
❌ Kubernetes


🛠 Skill Match Analysis
──────────────────────────────────────────────

Matched Skills:

✅ Python
✅ Docker
✅ FastAPI
✅ Agentic AI
✅ LLMs


Missing Skills:

❌ AI/ML
❌ REST APIs
❌ Flask
❌ Django REST
❌ AWS
❌ Azure
❌ GCP
❌ Kubernetes


Score Breakdown:

🔑 Keyword Match      : █████░░░░░ 50%

💼 Experience Match   : ██████████ 100%

🚀 Project Match      : ███████░░░ 70%



💪 Candidate Strengths
──────────────────────────────────────────────

✨ Strong experience in LLM applications

✨ Proficient in Python and Docker

✨ Experience building Agentic AI systems

✨ Experience developing AI-powered solutions



🚧 Improvement Areas
──────────────────────────────────────────────

🔻 AI/ML knowledge

🔻 REST API development

🔻 Flask / Django REST frameworks

🔻 Cloud platforms (AWS, Azure, GCP)

🔻 Kubernetes

🔻 Analytical and communication skills



🚀 AI Recommendations
──────────────────────────────────────────────

⭐ HIGH PRIORITY

Add missing skills such as:

• AI/ML
• REST APIs
• Flask
• Django REST
• AWS
• Azure
• GCP
• Kubernetes


⭐ MEDIUM PRIORITY

Improve project descriptions by highlighting:

• API development
• Cloud deployment
• Production AI systems
• Business impact



🧠 Final Assessment
──────────────────────────────────────────────

The candidate demonstrates strong experience
with LLM applications and Agentic AI.

However, additional alignment is required around
API development, cloud technologies, and ML
fundamentals to achieve a stronger ATS match.



🏆 Hiring Decision
──────────────────────────────────────────────

🟡 MODERATE MATCH


Reason:

Based on skills, experience,
projects, and ATS compatibility.



✅ Report Generation Completed
```

# 🎯 Future Improvements

-   Add web UI using Streamlit/FastAPI
-   Support DOCX resumes
-   Add resume rewriting agent
-   Add interview question generation
-   Add multiple job comparison
-   Add vector database based skill matching
-   Add resume ranking system

------------------------------------------------------------------------

# 👨‍💻 Author

Built as an AI Agent project demonstrating:

-   Multi-agent workflow design
-   LLM structured extraction
-   LangGraph orchestration
-   Resume intelligence automation
