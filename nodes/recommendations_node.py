from schemas.resume_analyze_state_schema import ResumeAnalyzeState
from components.recommendation_engine import recommendation_generator


def make_recommendations_node(llm):
    def recommendations_node(state: ResumeAnalyzeState):
        print("\n=== Recommendations Node Executed ===")

        result = recommendation_generator(
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
            ats_result={
                "matched_skills": state.matched_skills,
                "missing_skills": state.missing_skills,
                "keyword_match_score": state.keyword_match_score,
                "experience_match_score": state.experience_match_score,
                "project_match_score": state.project_match_score,
                "ats_score": state.ats_score,
                "ats_reasoning": state.ats_reasoning,
            },
        )

        return {
            "recommendation_category": result.category,
            "recommendation_suggestion": result.suggestion,
            "recommendation_priority": result.priority,
            "recommendation_impact_area": result.impact_area,
        }

    return recommendations_node
