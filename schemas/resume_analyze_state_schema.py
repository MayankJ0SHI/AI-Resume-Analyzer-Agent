from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Shared building blocks
# ---------------------------------------------------------------------------


class Skill(BaseModel):
    name: str = Field(..., description="Name of the skill.")
    category: Literal["technical", "soft", "tool", "domain"] = Field(
        ..., description="Category of the skill."
    )


class Project(BaseModel):
    name: str = Field(..., description="Name of the project.")
    description: str = Field(..., description="Description about the project.")
    skills_used: List[str] = Field(
        ..., description="List of the skills used in the project."
    )
    impact: Optional[str] = Field(
        None, description="Impact as per the project, if mentioned."
    )


class RequiredSkill(BaseModel):
    name: str = Field(..., description="Name of the skill, tool, or technology.")
    category: Literal["technical", "soft", "tool", "domain"] = Field(
        ..., description="Category of the skill."
    )
    requirement_level: Literal["required", "preferred"] = Field(
        ...,
        description=(
            "Whether the job description states this as a must-have requirement "
            "or a nice-to-have / preferred qualification."
        ),
    )


class Responsibility(BaseModel):
    description: str = Field(
        ...,
        description="A single core responsibility or duty mentioned in the job description.",
    )


# ---------------------------------------------------------------------------
# Resume extraction (LLM output schema)
# ---------------------------------------------------------------------------


class ResumeExtractionPydanticModel(BaseModel):
    candidate_name: str = Field(
        ..., description="Name of the candidate from the resume."
    )
    experience_summary: str = Field(
        ..., description="Overall experience summary of the candidate."
    )
    total_experience_years: float = Field(
        ..., description="Total experience of the candidate, in years."
    )
    extracted_skills: List[Skill]
    extracted_projects: List[Project]


# ---------------------------------------------------------------------------
# Job description extraction (LLM output schema)
# ---------------------------------------------------------------------------


class JobExtractionPydanticModel(BaseModel):
    job_title: str = Field(..., description="The job title as stated in the posting.")
    company_name: Optional[str] = Field(
        None, description="Name of the hiring company, if mentioned in the text."
    )
    job_summary: str = Field(
        ...,
        description="A concise summary of the role, its purpose, and what the team does.",
    )
    min_experience_years: Optional[float] = Field(
        None,
        description=(
            "Minimum years of experience required for the role, if stated. "
            "Null if not specified or not applicable."
        ),
    )
    employment_type: Optional[
        Literal["full-time", "part-time", "contract", "internship", "freelance"]
    ] = Field(None, description="Type of employment, if mentioned.")
    location: Optional[str] = Field(
        None, description="Work location or remote/hybrid/onsite policy, if mentioned."
    )
    extracted_skills: List[RequiredSkill] = Field(
        ...,
        description="List of skills, tools, and technologies mentioned in the job description.",
    )
    responsibilities: List[Responsibility] = Field(
        ...,
        description="Key responsibilities and duties listed in the job description.",
    )
    qualifications: List[str] = Field(
        default_factory=list,
        description=(
            "Educational or certification qualifications mentioned (e.g. degree requirements). "
            "Empty list if none are stated."
        ),
    )


# ---------------------------------------------------------------------------
# ATS evaluation (LLM output schema)
# ---------------------------------------------------------------------------


class ATSEvaluationPydanticModel(BaseModel):
    matched_skills: List[str] = Field(
        ...,
        description=(
            "Skills from the job description (required or preferred) that the "
            "candidate's resume demonstrates, either directly listed or clearly "
            "evidenced through project descriptions."
        ),
    )
    missing_skills: List[str] = Field(
        ...,
        description=(
            "Skills from the job description (required or preferred) that the "
            "candidate's resume does not demonstrate anywhere."
        ),
    )
    keyword_match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description=(
            "Score from 0-100 reflecting how well the candidate's listed skills "
            "and keywords align with the job description's required and preferred skills."
        ),
    )
    experience_match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description=(
            "Score from 0-100 reflecting how well the candidate's years of experience "
            "and experience summary align with the job description's stated requirements."
        ),
    )
    project_match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description=(
            "Score from 0-100 reflecting how relevant the candidate's projects are "
            "to the responsibilities and domain described in the job description."
        ),
    )
    ats_score: float = Field(
        ...,
        ge=0,
        le=100,
        description=(
            "Overall ATS match score from 0-100, considering keyword match, experience "
            "match, and project relevance together as a holistic assessment."
        ),
    )
    reasoning: str = Field(
        ...,
        description="A brief explanation of how the scores were determined, citing specific evidence from the resume and job description.",
    )


class Recommendation(BaseModel):

    category: Literal[
        "skill_gap",
        "resume_improvement",
        "project_improvement",
        "keyword_optimization",
        "experience_alignment",
    ] = Field(..., description="Type of improvement recommendation.")

    suggestion: str = Field(
        ...,
        description=(
            "Specific actionable recommendation to improve "
            "resume alignment with the job description."
        ),
    )

    priority: Literal["high", "medium", "low"] = Field(
        ..., description="Importance level based on expected ATS impact."
    )

    impact_area: str = Field(
        ...,
        description=(
            "What ATS evaluation area this improves, "
            "such as skills, keywords, experience, or projects."
        ),
    )


class SkillMatchAnalysis(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    keyword_match_score: float
    experience_match_score: float
    project_match_score: float

class CandidateOverview(BaseModel):
    candidate_name: str
    experience_years: float
    profile_summary: str

class FinalResumeAnalysisReport(BaseModel):
    candidate: CandidateOverview
    job_title: str
    company_name: Optional[str]
    ats_score: float
    ats_summary: str = Field(description="Overall explanation of ATS score.")
    skill_analysis: SkillMatchAnalysis
    strengths: List[str] = Field(description="Candidate strengths for this role.")
    skill_gaps: List[str] = Field(description="Important missing skills.")
    recommendations: List[str] = Field(
        description="Actionable improvement recommendations."
    )
    hiring_recommendation: Literal["strong_match", "moderate_match", "weak_match"]
    final_assessment: str

# ---------------------------------------------------------------------------
# Graph state
# ---------------------------------------------------------------------------
class ResumeAnalyzeState(BaseModel):

    # -----------------------------
    # Inputs
    # -----------------------------

    resume_path: str
    job_description: str

    # -----------------------------
    # Resume Processing
    # -----------------------------

    resume_content: str = ""

    candidate_name: Optional[str] = None

    experience_summary: Optional[str] = None

    total_experience_years: Optional[float] = None

    extracted_skills: List[Skill] = Field(default_factory=list)

    extracted_projects: List[Project] = Field(default_factory=list)

    # -----------------------------
    # Job Description Processing
    # -----------------------------

    job_title: Optional[str] = None

    company_name: Optional[str] = None

    job_summary: Optional[str] = None

    required_experience_years: Optional[float] = None

    employment_type: Optional[
        Literal["full-time", "part-time", "contract", "internship", "freelance"]
    ] = None

    location: Optional[str] = None

    extracted_job_skills: List[RequiredSkill] = Field(default_factory=list)

    responsibilities: List[Responsibility] = Field(default_factory=list)

    qualifications: List[str] = Field(default_factory=list)

    # -----------------------------
    # ATS Evaluation
    # -----------------------------

    matched_skills: List[str] = Field(default_factory=list)

    missing_skills: List[str] = Field(default_factory=list)

    keyword_match_score: float = 0.0

    experience_match_score: float = 0.0

    project_match_score: float = 0.0

    ats_score: float = 0.0

    ats_reasoning: Optional[str] = None

    # =============================
    # Recommendation Generation
    # =============================

    recommendation_category: Optional[
        Literal[
            "skill_gap",
            "resume_improvement",
            "project_improvement",
            "keyword_optimization",
            "experience_alignment",
        ]
    ] = None

    recommendation_suggestion: Optional[str] = None

    recommendation_priority: Optional[Literal["high", "medium", "low"]] = None

    recommendation_impact_area: Optional[str] = None
    
    final_report: Optional[FinalResumeAnalysisReport] = None
