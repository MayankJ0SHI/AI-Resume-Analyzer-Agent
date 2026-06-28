from components.report_generator import generate_final_report

def final_report_node(llm):
    def node(state):
        print("\n=== Final Report Generation Node Executed ===")
        report = generate_final_report(
            llm,
            candidate_data={
                "name": state.candidate_name,
                "experience": state.total_experience_years,
                "summary": state.experience_summary,
            },
            job_data={
                "title": state.job_title,
                "company": state.company_name,
                "summary": state.job_summary,
            },
            ats_data={
                "ats_score": state.ats_score,
                "matched_skills": state.matched_skills,
                "missing_skills": state.missing_skills,
                "keyword_score": state.keyword_match_score,
                "experience_score": state.experience_match_score,
                "project_score": state.project_match_score,
                "reasoning": state.ats_reasoning,
            },
            recommendation_data={
                "category": state.recommendation_category,
                "suggestion": state.recommendation_suggestion,
                "priority": state.recommendation_priority,
                "impact_area": state.recommendation_impact_area,
            },
        )
        return {"final_report": report}
    return node
