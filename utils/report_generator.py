"""
Report Generator Module
Generates PDF and text analysis reports
"""

from datetime import datetime
from typing import Dict, List
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors


class ReportGenerator:
    """Generate analysis reports in PDF and text formats"""
    
    @staticmethod
    def generate_text_report(analysis_data: Dict, output_path: str = None) -> str:
        """
        Generate text format report
        
        Args:
            analysis_data: Dictionary with analysis results
            output_path: Path to save report (optional)
            
        Returns:
            Report text
        """
        report = []
        report.append("=" * 80)
        report.append("AI RESUME ANALYZER - ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Match Score
        if "match_score" in analysis_data:
            report.append("RESUME-JD MATCH ANALYSIS")
            report.append("-" * 40)
            match = analysis_data["match_score"]
            report.append(f"Overall Match Score: {match.get('overall_match_score', 0)}%")
            report.append(f"TF-IDF Score: {match.get('tfidf_score', 0)}%")
            report.append(f"Keyword Score: {match.get('keyword_score', 0)}%")
            report.append(f"Skill Match Score: {match.get('skill_match_score', 0)}%")
            report.append("")
        
        # ATS Score
        if "ats_score" in analysis_data:
            report.append("ATS COMPATIBILITY SCORE")
            report.append("-" * 40)
            ats = analysis_data["ats_score"]
            report.append(f"Overall ATS Score: {ats.get('overall_ats_score', 0)}/100")
            report.append(f"Contact Information: {ats.get('contact_information_score', 0)}/100")
            report.append(f"Formatting: {ats.get('formatting_score', 0)}/100")
            report.append(f"Keywords & Content: {ats.get('keyword_optimization_score', 0)}/100")
            report.append("")
        
        # Extracted Skills
        if "skills" in analysis_data:
            report.append("SKILLS ANALYSIS")
            report.append("-" * 40)
            skills = analysis_data["skills"]
            
            if "technical_skills" in skills and skills["technical_skills"]:
                report.append("Technical Skills:")
                for skill in skills["technical_skills"]:
                    report.append(f"  • {skill}")
            
            if "soft_skills" in skills and skills["soft_skills"]:
                report.append("\nSoft Skills:")
                for skill in skills["soft_skills"]:
                    report.append(f"  • {skill}")
            report.append("")
        
        # Missing Skills
        if "missing_skills" in analysis_data:
            report.append("MISSING SKILLS (from JD)")
            report.append("-" * 40)
            missing = analysis_data["missing_skills"]
            if missing:
                for skill in missing[:10]:  # Top 10
                    report.append(f"  ✗ {skill}")
            else:
                report.append("All skills are present!")
            report.append("")
        
        # Recommendations
        if "suggestions" in analysis_data:
            report.append("AI RECOMMENDATIONS")
            report.append("-" * 40)
            suggestions = analysis_data["suggestions"]
            for category, items in suggestions.items():
                report.append(f"\n{category.upper()}:")
                for item in items[:3]:  # Top 3 per category
                    report.append(f"  → {item}")
        
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        # Save to file if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
        
        return report_text
    
    @staticmethod
    def generate_pdf_report(analysis_data: Dict, output_path: str) -> None:
        """
        Generate PDF format report
        
        Args:
            analysis_data: Dictionary with analysis results
            output_path: Path to save PDF
        """
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=10,
                alignment=1  # Center
            )
            story.append(Paragraph("AI Resume Analyzer", title_style))
            story.append(Paragraph("Analysis Report", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Generated date
            date_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Match Score Section
            if "match_score" in analysis_data:
                story.append(Paragraph("Resume-JD Match Analysis", styles['Heading2']))
                match = analysis_data["match_score"]
                
                match_data = [
                    ["Metric", "Score"],
                    ["Overall Match", f"{match.get('overall_match_score', 0)}%"],
                    ["TF-IDF Score", f"{match.get('tfidf_score', 0)}%"],
                    ["Keyword Score", f"{match.get('keyword_score', 0)}%"],
                    ["Skill Match", f"{match.get('skill_match_score', 0)}%"],
                ]
                
                table = Table(match_data, colWidths=[3*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(table)
                story.append(Spacer(1, 20))
            
            # ATS Score Section
            if "ats_score" in analysis_data:
                story.append(Paragraph("ATS Compatibility Analysis", styles['Heading2']))
                ats = analysis_data["ats_score"]
                
                ats_data = [
                    ["Category", "Score"],
                    ["Overall ATS Score", f"{ats.get('overall_ats_score', 0)}/100"],
                    ["Contact Information", f"{ats.get('contact_information_score', 0)}/100"],
                    ["Formatting", f"{ats.get('formatting_score', 0)}/100"],
                    ["Keywords & Content", f"{ats.get('keyword_optimization_score', 0)}/100"],
                ]
                
                table = Table(ats_data, colWidths=[3*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(table)
                story.append(Spacer(1, 20))
            
            # Skills Section
            if "skills" in analysis_data:
                story.append(Paragraph("Skills Summary", styles['Heading2']))
                skills = analysis_data["skills"]
                
                tech_skills_text = ", ".join(
                    skills.get("technical_skills", [])[:10]
                ) or "None found"
                story.append(Paragraph(f"<b>Technical Skills:</b> {tech_skills_text}", styles['Normal']))
                story.append(Spacer(1, 12))
                
                soft_skills_text = ", ".join(
                    skills.get("soft_skills", [])[:5]
                ) or "None found"
                story.append(Paragraph(f"<b>Soft Skills:</b> {soft_skills_text}", styles['Normal']))
                story.append(Spacer(1, 20))
            
            doc.build(story)
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise
