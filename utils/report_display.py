from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

from schemas.resume_analyze_state_schema import FinalResumeAnalysisReport

console = Console()


def score_bar(score: float):
    filled = int(score / 10)
    empty = 10 - filled

    return (
        f"[green]{'█' * filled}[/green]"
        f"[grey50]{'░' * empty}[/grey50] "
        f"[bold]{score}/100[/bold]"
    )


def display_resume_report(report: FinalResumeAnalysisReport):

    console.print(
        Panel(
            """
[bold cyan]🤖 AI Resume Analyzer Report[/bold cyan]

📄 Resume Intelligence Report
🎯 ATS Compatibility Analysis
🚀 Career Improvement Suggestions
            """,
            expand=False,
            border_style="cyan",
        )
    )

    # =====================================================
    # 👤 Candidate Overview
    # =====================================================

    console.print("\n[bold blue]👤 Candidate Overview[/bold blue]")

    candidate_table = Table(show_header=False, box=None)

    candidate_table.add_column("Field", style="cyan")

    candidate_table.add_column("Details")

    candidate_table.add_row("🧑 Name", report.candidate.candidate_name)

    candidate_table.add_row(
        "💼 Experience", f"{report.candidate.experience_years} years"
    )

    candidate_table.add_row("📝 Profile", report.candidate.profile_summary)

    console.print(candidate_table)

    # =====================================================
    # 🎯 ATS Evaluation
    # =====================================================

    console.print("\n[bold yellow]🎯 ATS Compatibility Score[/bold yellow]")

    ats_panel = f"""
[bold]Overall ATS Score[/bold]

{score_bar(report.ats_score)}


📌 Analysis:

{report.ats_summary}
"""

    console.print(Panel(ats_panel, border_style="yellow"))

    # =====================================================
    # 🛠 Skill Analysis
    # =====================================================

    console.print("\n[bold green]🛠 Skill Match Analysis[/bold green]")

    skill_table = Table(box=None)

    skill_table.add_column("Category", style="bold cyan")

    skill_table.add_column("Details")

    matched = (
        "\n".join(f"✅ {skill}" for skill in report.skill_analysis.matched_skills)
        if report.skill_analysis.matched_skills
        else "None"
    )

    missing = (
        "\n".join(f"❌ {skill}" for skill in report.skill_analysis.missing_skills)
        if report.skill_analysis.missing_skills
        else "None"
    )

    skill_table.add_row("✅ Matched Skills", matched)

    skill_table.add_row("⚠️ Missing Skills", missing)

    skill_table.add_row(
        "🔑 Keyword Match", score_bar(report.skill_analysis.keyword_match_score)
    )

    skill_table.add_row(
        "💼 Experience Match", score_bar(report.skill_analysis.experience_match_score)
    )

    skill_table.add_row(
        "🚀 Project Match", score_bar(report.skill_analysis.project_match_score)
    )

    console.print(skill_table)

    # =====================================================
    # 💪 Strengths
    # =====================================================

    console.print("\n[bold green]💪 Candidate Strengths[/bold green]")

    strengths = "\n".join(f"✨ {item}" for item in report.strengths)

    console.print(Panel(strengths, border_style="green"))

    # =====================================================
    # 🚧 Skill Gaps
    # =====================================================

    console.print("\n[bold red]🚧 Improvement Areas[/bold red]")

    gaps = "\n".join(f"🔻 {item}" for item in report.skill_gaps)

    console.print(Panel(gaps, border_style="red"))

    # =====================================================
    # 🚀 Recommendations
    # =====================================================

    console.print("\n[bold magenta]🚀 AI Recommendations[/bold magenta]")

    recommendation_table = Table()

    recommendation_table.add_column("Priority", style="yellow")

    recommendation_table.add_column("Recommendation")

    for recommendation in report.recommendations:

        recommendation_table.add_row("⭐", recommendation)

    console.print(recommendation_table)

    # =====================================================
    # 🧠 Final Assessment
    # =====================================================

    console.print("\n[bold cyan]🧠 Final Assessment[/bold cyan]")

    console.print(Panel(report.final_assessment, border_style="cyan"))

    # =====================================================
    # 🏆 Hiring Recommendation
    # =====================================================

    status = report.hiring_recommendation.upper()

    if status == "STRONG_MATCH":
        emoji = "🟢"
    elif status == "MODERATE_MATCH":
        emoji = "🟡"
    else:
        emoji = "🔴"

    console.print(
        Panel(
            f"""
{emoji} [bold]{status}[/bold]

Based on skills, experience,
projects and ATS compatibility.
""",
            title="🏆 Hiring Decision",
            border_style="blue",
        )
    )

    console.print("\n[bold green]✅ Report Generation Completed[/bold green]\n")
