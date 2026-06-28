from schemas.resume_analyze_state_schema import ResumeAnalyzeState
from components.job_description_extraction import get_info_from_job_description

def make_jd_extractor_node(llm):
    def jd_extractor_node(state: ResumeAnalyzeState):
        print("\n === Job Description Extractor Node Executed ===")
        result = get_info_from_job_description(llm, state.job_description)

        required = [s for s in result.extracted_skills if s.requirement_level == "required"]
        preferred = [s for s in result.extracted_skills if s.requirement_level == "preferred"]

        return {
            "job_title": result.job_title,
            "company_name": result.company_name,
            "job_summary": result.job_summary,
            "required_experience_years": result.min_experience_years,
            "employment_type": result.employment_type,
            "job_location": result.location,
            "extracted_job_skills": result.extracted_skills,
            "required_skills": [s.name for s in required],
            "preferred_skills": [s.name for s in preferred],
            "responsibilities": result.responsibilities,
            "qualifications": result.qualifications
        }
    return jd_extractor_node