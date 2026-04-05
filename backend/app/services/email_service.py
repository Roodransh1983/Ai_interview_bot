"""
Email service — sends interview reports via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from app.config import settings


class EmailService:
    """Handles sending interview reports via email"""

    def send_report(self, to_email: str, report: Dict, user_name: str = "Candidate") -> bool:
        """
        Send an interview report to the user's email.

        Args:
            to_email: Recipient email address
            report: Report dictionary from scoring engine
            user_name: Name of the candidate

        Returns:
            True if email was sent successfully, False otherwise
        """
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            print("⚠️ Email not configured — skipping send")
            return False

        try:
            # Build HTML email
            html_content = self._build_html_report(report, user_name)

            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"📊 Your AI Interview Report — Score: {report.get('total_score', 0)}/100"
            msg["From"] = settings.SMTP_USER
            msg["To"] = to_email

            # Attach HTML part
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            # Send via SMTP
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            print(f"✅ Report email sent to {to_email}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

    def _build_html_report(self, report: Dict, user_name: str) -> str:
        """Build a nice HTML email for the report"""
        total_score = report.get("total_score", 0)
        grade = report.get("grade", "F")
        category_scores = report.get("category_scores", {})
        strengths = report.get("strengths", [])
        weaknesses = report.get("weaknesses", [])
        suggestions = report.get("suggestions", [])
        breakdown = report.get("breakdown", [])

        # Score color
        if total_score >= 80:
            score_color = "#22c55e"  # green
        elif total_score >= 60:
            score_color = "#eab308"  # yellow
        else:
            score_color = "#ef4444"  # red

        breakdown_rows = ""
        for item in breakdown:
            breakdown_rows += f"""
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 12px; font-weight: bold;">Q{item['question_number']}</td>
                <td style="padding: 12px;">{item.get('category', 'N/A')}</td>
                <td style="padding: 12px; max-width: 300px; font-size: 13px;">{item.get('user_answer', '')[:150]}...</td>
                <td style="padding: 12px; font-weight: bold; color: {score_color if item['score'] >= 60 else '#ef4444'};">{item['score']}</td>
                <td style="padding: 12px;">{item.get('feedback', '')[:100]}</td>
            </tr>
            """

        strengths_html = "".join(
            f'<span style="background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 16px; margin: 4px; display: inline-block;">✅ {s}</span>'
            for s in strengths
        ) if strengths else '<span style="color: #6b7280;">N/A</span>'

        weaknesses_html = "".join(
            f'<span style="background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 16px; margin: 4px; display: inline-block;">⚠️ {w}</span>'
            for w in weaknesses
        ) if weaknesses else '<span style="color: #6b7280;">N/A</span>'

        suggestions_html = "".join(
            f'<li style="margin-bottom: 8px;">💡 {s}</li>'
            for s in suggestions
        ) if suggestions else '<li>N/A</li>'

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9fafb; color: #1f2937;">
            <div style="background: white; border-radius: 16px; padding: 32px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <!-- Header -->
                <div style="text-align: center; margin-bottom: 32px;">
                    <h1 style="font-size: 24px; margin-bottom: 8px;">🎯 AI Interview Report</h1>
                    <p style="color: #6b7280; margin: 0;">Hi {user_name}, here are your interview results!</p>
                </div>

                <!-- Score Card -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 32px; text-align: center; color: white; margin-bottom: 32px;">
                    <div style="font-size: 64px; font-weight: bold;">{total_score}<span style="font-size: 32px;">/100</span></div>
                    <div style="font-size: 24px; margin-top: 8px;">Grade: {grade}</div>
                    <p style="opacity: 0.9; margin-top: 12px;">Average Answer Score: {report.get('average_answer_score', 0)} | Average Confidence: {report.get('average_confidence', 0)}</p>
                </div>

                <!-- Category Scores -->
                <div style="margin-bottom: 32px;">
                    <h2 style="font-size: 18px; margin-bottom: 16px;">📈 Category Breakdown</h2>
                    <div style="display: flex; flex-wrap: wrap; gap: 12px;">
                        {"".join(
                            f'<div style="background: #f3f4f6; padding: 12px 16px; border-radius: 8px; min-width: 120px;">'
                            f'<div style="font-weight: bold; color: #4f46e5;">{cat}</div>'
                            f'<div style="font-size: 20px; font-weight: bold;">{score}%</div>'
                            f'</div>'
                            for cat, score in category_scores.items()
                        )}
                    </div>
                </div>

                <!-- Strengths & Weaknesses -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px;">
                    <div>
                        <h2 style="font-size: 18px; margin-bottom: 12px;">💪 Strengths</h2>
                        {strengths_html}
                    </div>
                    <div>
                        <h2 style="font-size: 18px; margin-bottom: 12px;">📚 Areas to Improve</h2>
                        {weaknesses_html}
                    </div>
                </div>

                <!-- Suggestions -->
                <div style="margin-bottom: 32px;">
                    <h2 style="font-size: 18px; margin-bottom: 12px;">💡 Personalized Suggestions</h2>
                    <ul style="background: #eff6ff; padding: 16px 16px 16px 36px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                        {suggestions_html}
                    </ul>
                </div>

                <!-- Question Breakdown -->
                <div>
                    <h2 style="font-size: 18px; margin-bottom: 16px;">📝 Answer Details</h2>
                    <table style="width: 100%; border-collapse: collapse; background: white;">
                        <thead>
                            <tr style="background: #f9fafb; text-align: left;">
                                <th style="padding: 12px; border-bottom: 2px solid #e5e7eb;">#</th>
                                <th style="padding: 12px; border-bottom: 2px solid #e5e7eb;">Category</th>
                                <th style="padding: 12px; border-bottom: 2px solid #e5e7eb;">Your Answer</th>
                                <th style="padding: 12px; border-bottom: 2px solid #e5e7eb;">Score</th>
                                <th style="padding: 12px; border-bottom: 2px solid #e5e7eb;">Feedback</th>
                            </tr>
                        </thead>
                        <tbody>
                            {breakdown_rows}
                        </tbody>
                    </table>
                </div>

                <!-- Footer -->
                <div style="text-align: center; margin-top: 32px; padding-top: 24px; border-top: 1px solid #e5e7eb;">
                    <p style="color: #6b7280; font-size: 14px; margin: 0;">
                        Keep practicing and improving! 🚀<br>
                        — Your AI Interview Bot
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
