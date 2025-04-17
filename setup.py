from setuptools import setup, find_packages

setup(
    name="resume_ats_scorer",
    version="1.0.0",
    description="A Resume ATS Score Checker using CrewAI for multi-agent design",
    author="Resume ATS Scorer Team",
    author_email="deepualevoor3@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "crewai>=0.108.0",
        "pydantic>=2.11.0",
        "fastapi>=0.110.0",
        "uvicorn>=0.27.1",
        "python-multipart>=0.0.9",
        "PyPDF2>=3.0.1",
        "python-docx>=1.1.0",
        "beautifulsoup4>=4.12.3",
        "spacy>=3.7.2"
    ],
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)


