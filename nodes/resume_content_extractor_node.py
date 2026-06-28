from components.resume_extraction import get_info_from_resume
from schemas.resume_analyze_state_schema import ResumeAnalyzeState

def make_resume_content_extractor_node(llm):
    def resume_content_extractor_node(state: ResumeAnalyzeState):
        print("\n === Resume Content Extractor Node Executed ===")
        result = get_info_from_resume(llm, state.resume_content)
        return {
            "candidate_name": result.candidate_name,
            "experience_summary": result.experience_summary,
            "total_experience_years": result.total_experience_years,
            "extracted_skills": result.extracted_skills,
            "extracted_projects": result.extracted_projects
        }
    return resume_content_extractor_node