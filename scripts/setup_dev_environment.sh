## 2. scripts/setup_dev_environment.sh - Development Environment Setup
#!/bin/bash
"""
Development Environment Setup Script
Sets up the complete development environment for the Patent Research Agent
"""

set -e

echo "🚀 Setting up Patent Research Agent Development Environment"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -e ".[dev]"

# Set up pre-commit hooks
echo "🔗 Setting up pre-commit hooks..."
pre-commit install

# Create environment file
echo "📄 Creating environment file..."
if [ ! -f .env ]; then
    cat > .env << EOF
# Development Environment Variables
DEBUG=true
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/patent_agent_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (replace with actual keys)
CLAUDE_API_KEY=your_claude_api_key_here
GOOGLE_PATENTS_API_KEY=your_google_patents_key_here
USPTO_API_KEY=your_uspto_key_here

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here

# External Services
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key_here

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=3600
EOF
    echo "✅ Created .env file. Please update with your actual API keys."
else
    echo "✅ .env file already exists."
fi

# Set up database
echo "🗄️ Setting up database..."
createdb patent_agent_dev 2>/dev/null || echo "Database already exists"

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Install frontend dependencies
if [ -d "frontend" ]; then
    echo "🎨 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Update .env file with your API keys"
echo "3. Start development server: uvicorn app.main:app --reload"
