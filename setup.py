## 1. setup.py - Package Setup Script
#!/usr/bin/env python3
"""
Patent Research & Application Agent
Setup script for development environment
"""

from setuptools import setup, find_packages

setup(
    name="patent-research-agent",
    version="0.1.0",
    description="AI-powered patent research and application agent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/sotirisspyrou-uk/patent-research-agent",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "anthropic>=0.7.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.13.0",
        "psycopg2-binary>=2.9.0",
        "redis>=5.0.0",
        "elasticsearch>=8.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "python-multipart>=0.0.6",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "stripe>=7.0.0",
        "celery>=5.3.0",
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "mypy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=4.1.0",
            "pre-commit>=3.5.0",
            "bandit>=1.7.5",
            "safety>=2.3.0",
            "isort>=5.12.0",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "prometheus-client>=0.19.0",
            "sentry-sdk>=1.38.0",
        ]
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
