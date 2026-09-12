"""
Generate synthetic denial letter PDFs for AegisHealth-KG Phase 0.

Creates 3 realistic-looking denial letters in data/synthetic/denial_letters/
"""

from fpdf import FPDF
from pathlib import Path
import os


OUTPUT_DIR = Path(__file__).parent.parent / "data" / "synthetic" / "denial_letters"


class DenialLetterPDF(FPDF):
    """Custom PDF class for generating denial letters."""

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "AcmeCare Health Insurance", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "", 9)
        self.cell(0, 5, "Claims Processing Division", new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(0, 5, "P.O. Box 94120, Phoenix, AZ 85070-4120", new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(0, 5, "Phone: 1-800-555-ACME (2263)  |  Fax: 1-800-555-2264", new_x="LMARGIN", new_y="NEXT", align="C")
        self.line(10, self.get_y() + 3, 200, self.get_y() + 3)
        self.ln(8)

    def footer(self):
        self.set_y(-25)
        self.set_font("Helvetica", "I", 7)
        self.cell(0, 4, "This is not a bill. This is an Explanation of Benefits (EOB) for your records.", new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(0, 4, "If you disagree with this determination, you have the right to appeal within 180 days of this notice.", new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(0, 4, f"Page {self.page_no()}/{{nb}}", new_x="LMARGIN", new_y="NEXT", align="C")

    def add_section_header(self, text: str):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {text}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(3)

    def add_field(self, label: str, value: str):
        self.set_font("Helvetica", "B", 9)
        self.cell(55, 6, label + ":")
        self.set_font("Helvetica", "", 9)
        self.cell(0, 6, value, new_x="LMARGIN", new_y="NEXT")

    def add_paragraph(self, text: str):
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, text)
        self.ln(2)


def generate_scenario_1():
    """Scenario 1: Type 2 Diabetes -> CGM  -  Step Therapy denial."""
    pdf = DenialLetterPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Date and recipient
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "Date of Notice: August 28, 2024", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.add_paragraph(
        "Maria Gonzalez\n"
        "1420 Riverside Drive, Apt 3B\n"
        "Austin, TX 78741"
    )
    pdf.ln(2)

    # Claim information section
    pdf.add_section_header("CLAIM INFORMATION")
    pdf.add_field("Member Name", "Maria Gonzalez")
    pdf.add_field("Member ID", "ACM-8827451-01")
    pdf.add_field("Group Number", "GRP-20240-TX")
    pdf.add_field("Claim Number", "CLM-2024-0815-001")
    pdf.add_field("Date of Service", "August 15, 2024")
    pdf.add_field("Date Claim Received", "August 20, 2024")
    pdf.add_field("Plan Name", "AcmeCare Preferred PPO")
    pdf.ln(2)

    # Provider information
    pdf.add_section_header("PROVIDER INFORMATION")
    pdf.add_field("Rendering Provider", "Dr. Priya Sharma, MD  -  Endocrinology")
    pdf.add_field("Provider NPI", "1234567890")
    pdf.add_field("Practice", "Capital Endocrine Associates")
    pdf.add_field("Practice Address", "4200 Medical Parkway, Suite 310, Austin, TX 78756")
    pdf.ln(2)

    # Service details
    pdf.add_section_header("SERVICE DETAILS")
    pdf.add_field("Procedure Code", "CPT 95251  -  Continuous Glucose Monitoring, interpretation and report")
    pdf.add_field("Diagnosis Code", "E11.9  -  Type 2 Diabetes Mellitus without complications")
    pdf.add_field("Billed Amount", "$450.00")
    pdf.add_field("Allowed Amount", "$0.00")
    pdf.add_field("Patient Responsibility", "$450.00")
    pdf.ln(2)

    # Determination
    pdf.add_section_header("CLAIM DETERMINATION")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 8, "STATUS: DENIED", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    pdf.add_field("Denial Reason Code", "CO-167")
    pdf.add_field("Denial Category", "Step Therapy Requirement")
    pdf.ln(2)

    pdf.add_paragraph(
        "REASON FOR DENIAL:\n\n"
        "Your claim for Continuous Glucose Monitoring (CPT 95251) has been denied. "
        "Under AcmeCare Policy ACME-CGM-2024-001, authorization for Continuous Glucose "
        "Monitoring requires documented completion of step therapy protocol. Specifically, "
        "the patient must have documented trials of both a first-line oral medication "
        "(Metformin) and a second-line oral medication (sulfonylurea class agent) with "
        "evidence of inadequate glycemic control or documented contraindication before "
        "CGM may be authorized.\n\n"
        "Based on our review, adequate documentation of step therapy completion was not "
        "found in the submitted materials. The claim is denied under Claim Adjustment "
        "Reason Code CO-167."
    )
    pdf.ln(3)

    # Appeal rights
    pdf.add_section_header("YOUR RIGHT TO APPEAL")
    pdf.add_paragraph(
        "If you disagree with this determination, you or your authorized representative "
        "may file an appeal within 180 calendar days from the date of this notice. To file "
        "an appeal, please submit the following to AcmeCare Appeals Department:\n\n"
        "1. A written statement explaining why you believe this claim should be approved\n"
        "2. Any additional medical records or documentation supporting your request\n"
        "3. A copy of this Explanation of Benefits\n\n"
        "Submit appeals to:\n"
        "AcmeCare Health Insurance  -  Appeals Department\n"
        "P.O. Box 94200, Phoenix, AZ 85070-4200\n"
        "Fax: 1-800-555-2265\n"
        "Email: appeals@acmecare-mock.example.com"
    )

    output_path = OUTPUT_DIR / "scenario_1_denial.pdf"
    pdf.output(str(output_path))
    print(f"Generated: {output_path}")


def generate_scenario_2():
    """Scenario 2: Knee Pain -> MRI  -  Prior Authorization Missing."""
    pdf = DenialLetterPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "Date of Notice: July 22, 2024", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.add_paragraph(
        "James Chen\n"
        "2850 Middlefield Road, Unit 12\n"
        "Palo Alto, CA 94306"
    )
    pdf.ln(2)

    pdf.add_section_header("CLAIM INFORMATION")
    pdf.add_field("Member Name", "James Chen")
    pdf.add_field("Member ID", "ACM-3314982-02")
    pdf.add_field("Group Number", "GRP-20240-CA")
    pdf.add_field("Claim Number", "CLM-2024-0712-002")
    pdf.add_field("Date of Service", "July 12, 2024")
    pdf.add_field("Date Claim Received", "July 15, 2024")
    pdf.add_field("Plan Name", "AcmeCare Preferred PPO")
    pdf.ln(2)

    pdf.add_section_header("PROVIDER INFORMATION")
    pdf.add_field("Rendering Provider", "Dr. Michael Torres, MD  -  Orthopedic Surgery")
    pdf.add_field("Provider NPI", "9876543210")
    pdf.add_field("Practice", "Bay Area Orthopedics & Sports Medicine")
    pdf.add_field("Practice Address", "1800 El Camino Real, Suite 220, Palo Alto, CA 94306")
    pdf.ln(2)

    pdf.add_section_header("SERVICE DETAILS")
    pdf.add_field("Procedure Code", "CPT 73721  -  MRI, lower extremity joint, without contrast")
    pdf.add_field("Diagnosis Code", "M25.561  -  Pain in right knee")
    pdf.add_field("Billed Amount", "$1,250.00")
    pdf.add_field("Allowed Amount", "$0.00")
    pdf.add_field("Patient Responsibility", "$1,250.00")
    pdf.ln(2)

    pdf.add_section_header("CLAIM DETERMINATION")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 8, "STATUS: DENIED", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    pdf.add_field("Denial Reason Code", "CO-197")
    pdf.add_field("Denial Category", "Prior Authorization/Precertification Absent")
    pdf.ln(2)

    pdf.add_paragraph(
        "REASON FOR DENIAL:\n\n"
        "Your claim for Magnetic Resonance Imaging of the right knee (CPT 73721) has "
        "been denied. Under AcmeCare Policy ACME-MRI-2024-002, all non-emergency lower "
        "extremity MRI requests require prior authorization from AcmeCare Utilization "
        "Review before the imaging study is performed.\n\n"
        "Our records indicate that no Prior Authorization Request (Form PA-200) was "
        "submitted for this service prior to the date of service. Clinical notes were "
        "received from the provider's office; however, submission of clinical notes alone "
        "does not constitute a prior authorization request.\n\n"
        "Additionally, AcmeCare policy requires documentation of a minimum 6 weeks (42 days) "
        "of conservative physical therapy prior to authorization of diagnostic imaging for "
        "knee pain. The submitted documentation indicates a physical therapy course of "
        "approximately 5 weeks and 5 sessions, which does not meet the minimum requirement.\n\n"
        "The claim is denied under Claim Adjustment Reason Code CO-197: "
        "Precertification/authorization/notification absent."
    )
    pdf.ln(3)

    pdf.add_section_header("YOUR RIGHT TO APPEAL")
    pdf.add_paragraph(
        "If you disagree with this determination, you or your authorized representative "
        "may file an appeal within 180 calendar days from the date of this notice. To file "
        "an appeal, please submit the following to AcmeCare Appeals Department:\n\n"
        "1. A written statement explaining why you believe this claim should be approved\n"
        "2. Completed Prior Authorization Request Form PA-200 (available at acmecare-mock.example.com)\n"
        "3. Any additional medical records or documentation supporting your request\n"
        "4. A copy of this Explanation of Benefits\n\n"
        "Submit appeals to:\n"
        "AcmeCare Health Insurance  -  Appeals Department\n"
        "P.O. Box 94200, Phoenix, AZ 85070-4200\n"
        "Fax: 1-800-555-2265\n"
        "Email: appeals@acmecare-mock.example.com"
    )

    output_path = OUTPUT_DIR / "scenario_2_denial.pdf"
    pdf.output(str(output_path))
    print(f"Generated: {output_path}")


def generate_scenario_3():
    """Scenario 3: Major Depressive Disorder -> Outpatient Therapy  -  Medical Necessity."""
    pdf = DenialLetterPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "Date of Notice: September 18, 2024", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.add_paragraph(
        "Aisha Williams\n"
        "300 West 135th Street, Apt 5C\n"
        "New York, NY 10030"
    )
    pdf.ln(2)

    pdf.add_section_header("CLAIM INFORMATION")
    pdf.add_field("Member Name", "Aisha Williams")
    pdf.add_field("Member ID", "ACM-5567123-03")
    pdf.add_field("Group Number", "GRP-20240-NY")
    pdf.add_field("Claim Number", "CLM-2024-0910-003")
    pdf.add_field("Date of Service", "September 10, 2024")
    pdf.add_field("Date Claim Received", "September 12, 2024")
    pdf.add_field("Plan Name", "AcmeCare Preferred PPO")
    pdf.ln(2)

    pdf.add_section_header("PROVIDER INFORMATION")
    pdf.add_field("Rendering Provider", "Dr. Rebecca Liu, MD  -  Psychiatry")
    pdf.add_field("Provider NPI", "5551234567")
    pdf.add_field("Practice", "Manhattan Behavioral Health Associates")
    pdf.add_field("Practice Address", "300 East 56th Street, Suite 1400, New York, NY 10022")
    pdf.ln(2)

    pdf.add_section_header("SERVICE DETAILS")
    pdf.add_field("Procedure Code", "CPT 90837  -  Psychotherapy, 53 minutes or more")
    pdf.add_field("Diagnosis Code", "F33.1  -  Major Depressive Disorder, recurrent, moderate")
    pdf.add_field("Session Number", "21 of calendar year 2024")
    pdf.add_field("Billed Amount", "$200.00")
    pdf.add_field("Allowed Amount", "$0.00")
    pdf.add_field("Patient Responsibility", "$200.00")
    pdf.ln(2)

    pdf.add_section_header("CLAIM DETERMINATION")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 8, "STATUS: DENIED", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    pdf.add_field("Denial Reason Code", "CO-50")
    pdf.add_field("Denial Category", "Medical Necessity Not Established")
    pdf.ln(2)

    pdf.add_paragraph(
        "REASON FOR DENIAL:\n\n"
        "Your claim for Psychotherapy (CPT 90837), session 21 of calendar year 2024, has "
        "been denied. Under AcmeCare Policy ACME-MH-2024-003, outpatient psychotherapy "
        "sessions 1 through 20 per calendar year are authorized without additional clinical "
        "review. Sessions beyond 20 per calendar year require documented medical necessity "
        "justification submitted for clinical review.\n\n"
        "A medical necessity justification package was received from your provider on "
        "September 10, 2024. After clinical review, AcmeCare's Utilization Review Committee "
        "has determined that the submitted documentation does not establish sufficient "
        "medical necessity for continuation of psychotherapy services beyond the standard "
        "20-session annual benefit.\n\n"
        "The claim is denied under Claim Adjustment Reason Code CO-50: These are non-covered "
        "services because this is not deemed a 'medical necessity' by the payer."
    )
    pdf.ln(3)

    pdf.add_section_header("CLINICAL REVIEW NOTES")
    pdf.add_paragraph(
        "The Utilization Review Committee notes the following:\n\n"
        "- The patient's most recent PHQ-9 score of 12 indicates moderate depression, which "
        "represents improvement from the baseline score of 18.\n"
        "- The committee acknowledges the patient's progress but notes that the current "
        "PHQ-9 score is close to the mild range (score < 10) and questions whether "
        "continued intensive psychotherapy is necessary versus alternative lower-intensity "
        "interventions.\n"
        "- The standard 20-session benefit is designed to provide an adequate course of "
        "acute-phase treatment for most patients."
    )
    pdf.ln(2)

    pdf.add_section_header("YOUR RIGHT TO APPEAL")
    pdf.add_paragraph(
        "If you disagree with this determination, you or your authorized representative "
        "may file an appeal within 180 calendar days from the date of this notice. "
        "For behavioral health denials based on medical necessity, your appeal may include:\n\n"
        "1. A written statement explaining why continued treatment is medically necessary\n"
        "2. Updated clinical documentation including recent symptom assessments\n"
        "3. Peer-reviewed literature supporting the clinical rationale for continued treatment\n"
        "4. Any information relevant to the Mental Health Parity and Addiction Equity Act "
        "(MHPAEA) if you believe this denial involves a treatment limitation that is more "
        "restrictive than limitations applied to comparable medical/surgical benefits\n"
        "5. A copy of this Explanation of Benefits\n\n"
        "Submit appeals to:\n"
        "AcmeCare Health Insurance  -  Appeals Department\n"
        "P.O. Box 94200, Phoenix, AZ 85070-4200\n"
        "Fax: 1-800-555-2265\n"
        "Email: appeals@acmecare-mock.example.com"
    )

    output_path = OUTPUT_DIR / "scenario_3_denial.pdf"
    pdf.output(str(output_path))
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating synthetic denial letter PDFs...")
    generate_scenario_1()
    generate_scenario_2()
    generate_scenario_3()
    print("\nAll denial letters generated successfully.")
