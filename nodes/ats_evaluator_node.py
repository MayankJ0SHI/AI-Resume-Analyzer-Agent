from schemas.resume_analyze_state_schema import ResumeAnalyzeState
from components.ats_evaluator import ats_evaluation


def make_ats_evaluator_node(llm):
    def ats_evaluator_node(state: ResumeAnalyzeState):
        print("\n=== ATS Evaluator Node Executed ===")

        result = ats_evaluation(
            llm,
            resume_data={
                "candidate_name": state.candidate_name,
                "experience_summary": state.experience_summary,
                "total_experience_years": state.total_experience_years,
                "extracted_skills": state.extracted_skills,
                "extracted_projects": state.extracted_projects,
            },
            jd_data={
                "job_title": state.job_title,
                "company_name": state.company_name,
                "job_summary": state.job_summary,
                "required_experience_years": state.required_experience_years,
                "employment_type": state.employment_type,
                "location": state.location,
                "extracted_job_skills": state.extracted_job_skills,
                "responsibilities": state.responsibilities,
                "qualifications": state.qualifications,
            },
        )

        return {
            "matched_skills": result.matched_skills,
            "missing_skills": result.missing_skills,
            "keyword_match_score": result.keyword_match_score,
            "experience_match_score": result.experience_match_score,
            "project_match_score": result.project_match_score,
            "ats_score": result.ats_score,
            "ats_reasoning": result.reasoning,
        }

    return ats_evaluator_node
