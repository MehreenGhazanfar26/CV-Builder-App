import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

# ---------- Helpers ----------
def normalize_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return ""
    if u.startswith(("http://", "https://")):
        return u
    if u.startswith("www."):
        return "https://" + u
    return "https://" + u

def show_link(label: str, url: str):
    if not url:
        return
    if hasattr(st, "link_button"):
        st.link_button(label, url, use_container_width=True)
    else:
        st.markdown(f"[{label}]({url})")

# ---------- Sidebar inputs ----------
st.sidebar.header("Enter Your Details")

# Basic Info
name = st.sidebar.text_input("Full Name", "Your Name")
email = st.sidebar.text_input("Email", "youremail@example.com")
phone = st.sidebar.text_input("Phone", "+92-XXX-XXXXXXX")

# Optional fields
mailing_address = st.sidebar.text_input("Mailing Address (optional)", "")

github_raw = st.sidebar.text_input("GitHub URL", "github.com/yourusername")
linkedin_raw = st.sidebar.text_input("LinkedIn URL", "linkedin.com/in/yourprofile")
website_raw = st.sidebar.text_input("Personal Website", "")

# Normalize links
github = normalize_url(github_raw)
linkedin = normalize_url(linkedin_raw)
website = normalize_url(website_raw)

# Summary
summary = st.sidebar.text_area("Profile Summary", "Write a short professional summary...")

# Projects
projects = st.sidebar.text_area(
    "Projects (each project on new line)",
    "Sentiment Analysis App\nPython Learning App\nTitanic ML Model"
)
projects_list = [p.strip() for p in projects.split("\n") if p.strip()]

# 🆕 Demo links for projects
st.sidebar.markdown("### Demo Links for Each Project")
demo_links_raw = st.sidebar.text_area(
    "Enter demo links in the same order (each link on new line)",
    "\n".join(["" for _ in projects_list])  # placeholder lines
)
demo_links_list = [normalize_url(l.strip()) for l in demo_links_raw.split("\n") if l.strip()]

# Pair projects with demo links
projects_with_links = []
for i, proj in enumerate(projects_list):
    link = demo_links_list[i] if i < len(demo_links_list) else ""
    projects_with_links.append((proj, link))

# Education
education = st.sidebar.text_area(
    "Education (each degree on new line)",
    "Masters in Education, University A (2022)\n"
    "Bachelors in Computer Science, University B (2020)\n"
    "Intermediate in Science, College XYZ (2018)"
)
education_list = [e.strip() for e in education.split("\n") if e.strip()]

# Certifications
has_cert = st.sidebar.radio("Do you have Certifications?", ["No", "Yes"], index=0)
certifications_list = []
if has_cert == "Yes":
    certifications = st.sidebar.text_area(
        "Certifications (each on new line)",
        "AWS Certified Practitioner\nPython for Everybody - Coursera"
    )
    certifications_list = [c.strip() for c in certifications.split("\n") if c.strip()]

# Hackathons
has_hackathon = st.sidebar.radio("Have you attended Hackathons?", ["No", "Yes"], index=0)
hackathon_list = []
if has_hackathon == "Yes":
    hackathons = st.sidebar.text_area(
        "Hackathons (each on new line)",
        "AI Hackathon 2023\nData Science Bootcamp 2022"
    )
    hackathon_list = [h.strip() for h in hackathons.split("\n") if h.strip()]

# Skills
skills = st.sidebar.text_area(
    "Skills (each skill on new line)",
    "Python\nMachine Learning\nData Preprocessing\nStreamlit"
)
skills_list = [s.strip() for s in skills.split("\n") if s.strip()]

# Hobbies
hobbies = st.sidebar.text_area(
    "Hobbies (each hobby on new line)",
    "Reading\nCoding\nTraveling"
)
hobbies_list = [h.strip() for h in hobbies.split("\n") if h.strip()]

# Experience
experience = st.sidebar.text_area(
    "Experience / Personal Projects",
    "I have developed multiple ML and Python projects as a student, "
    "including Sentiment Analysis, Titanic Dataset training, and a Student Performance App."
)

# ---------- Styled PDF Generator ----------
def generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=18,
        textColor=colors.HexColor("#0d47a1"),
        spaceAfter=12
    )
    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#0d47a1"),
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6
    )
    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
    )
    link_style = ParagraphStyle(
        "LinkStyle",
        parent=styles["Normal"],
        textColor=colors.HexColor("#1565c0"),
        fontSize=11,
        leading=14,
    )

    story = []

    # Name
    story.append(Paragraph(f"{name}", title_style))
    story.append(Spacer(1, 8))

    # Contact
    story.append(Paragraph(f"Email: {email}", normal_style))
    story.append(Paragraph(f"Phone: {phone}", normal_style))
    if mailing_address:
        story.append(Paragraph(f"Address: {mailing_address}", normal_style))
    story.append(Spacer(1, 8))

    # Links
    if github:
        story.append(Paragraph(f"GitHub: <u>{github}</u>", link_style))
    if linkedin:
        story.append(Paragraph(f"LinkedIn: <u>{linkedin}</u>", link_style))
    if website:
        story.append(Paragraph(f"Website: <u>{website}</u>", link_style))
    story.append(Spacer(1, 10))

    # Summary
    story.append(Paragraph("Profile Summary", header_style))
    story.append(Paragraph(summary, normal_style))

    # Projects
    story.append(Paragraph("Projects", header_style))
    for proj, link in projects_with_links:
        if link:
            story.append(Paragraph(f"• {proj} — <u>{link}</u>", link_style))
        else:
            story.append(Paragraph(f"• {proj}", normal_style))

    # Education
    story.append(Paragraph("Education", header_style))
    for edu in education_list:
        story.append(Paragraph(f"• {edu}", normal_style))

    # Certifications
    if has_cert == "Yes" and certifications_list:
        story.append(Paragraph("Certifications", header_style))
        for cert in certifications_list:
            story.append(Paragraph(f"• {cert}", normal_style))

    # Hackathons
    if has_hackathon == "Yes" and hackathon_list:
        story.append(Paragraph("Hackathons", header_style))
        for hack in hackathon_list:
            story.append(Paragraph(f"• {hack}", normal_style))

    # Skills
    if skills_list:
        story.append(Paragraph("Skills", header_style))
        for skill in skills_list:
            story.append(Paragraph(f"• {skill}", normal_style))

    # Hobbies
    if hobbies_list:
        story.append(Paragraph("Hobbies", header_style))
        for hobby in hobbies_list:
            story.append(Paragraph(f"• {hobby}", normal_style))

    # Experience
    story.append(Paragraph("Experience / Personal Projects", header_style))
    story.append(Paragraph(experience, normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------- Layout ----------
col1, col2 = st.columns([1, 2])

# Left Column
with col1:
    st.markdown(
        f"""
        <div style="background-color:#0d47a1; padding:20px; border-radius:12px; color:white;">
            <h2 style="margin-bottom:5px;">{name}</h2>
            <p>{email}</p>
            <p>{phone}</p>
            {"<p>" + mailing_address + "</p>" if mailing_address else ""}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Links")
    show_link("GitHub", github)
    show_link("LinkedIn", linkedin)
    show_link("Website", website)

    st.subheader("Skills")
    for skill in skills_list:
        st.markdown(f"- {skill}")

    st.subheader("Hobbies")
    for hobby in hobbies_list:
        st.markdown(f"- {hobby}")

# Right Column
with col2:
    st.title("Curriculum Vitae")

    st.subheader("Profile Summary")
    st.write(summary)

    st.subheader("Projects")
    for proj, link in projects_with_links:
        st.markdown(f"- **{proj}**")
        if link:
            st.markdown(f"  🎥 [Demo Video]({link})")

    st.subheader("Education")
    for edu in education_list:
        st.markdown(f"- {edu}")

    if has_cert == "Yes" and certifications_list:
        st.subheader("Certifications")
        for cert in certifications_list:
            st.markdown(f"- {cert}")

    if has_hackathon == "Yes" and hackathon_list:
        st.subheader("Hackathons")
        for hack in hackathon_list:
            st.markdown(f"- {hack}")

    st.subheader("Experience / Personal Projects")
    st.write(experience)

    # Download Button at bottom of CV
    st.subheader("Download")
    st.download_button(
        label="📄 Download CV as PDF",
        data=generate_pdf(),
        file_name="CV.pdf",
        mime="application/pdf"
    )
