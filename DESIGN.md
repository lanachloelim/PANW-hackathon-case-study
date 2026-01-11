# Finance Coach Application - Design Document

## Project Overview

This is an AI-powered personal finance coaching application built for the PANW Hackathon 2026. The project addresses the challenge of transforming raw transaction data into personalized insights that empower users to take control of their financial lives.

### Hackathon Case Study: Smart Financial Coach 💰

**Problem Statement**: Many people struggle with personal finance due to a lack of visibility and personalized, actionable advice. Manually tracking every expense is tedious, and generic budgeting apps often fail to inspire lasting behavioral change. As a result, people are often unaware of wasteful spending habits, miss opportunities to save, and feel anxious about their financial future.

**Solution**: An AI-powered financial coach that uses machine learning to provide intelligent spending insights, personalized goal forecasting, and subscription detection to help users build better financial habits.

**Target Audience**:
- Young adults and students looking to build good financial habits
- Freelancers and gig workers with variable incomes who need help with budgeting and saving  
- Anyone looking to gain a clear understanding of their spending and find actionable ways to save more effectively

## Architecture

### High-Level Architecture
```
┌─────────────────┐    HTTP API    ┌─────────────────┐
│   React Frontend │ ◄────────────► │  FastAPI Backend │
│   (Vite + TSX)   │                │   (Python)      │
└─────────────────┘                └─────────────────┘
                                          │
                                          ▼
                                ┌─────────────────┐
                                │   Data Storage  │
                                │  (JSON Files)   │
                                └─────────────────┘
```

### Technology Stack

#### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12+
- **Data Processing**: Pandas
#### AI/LLM: Together AI API
- **Model**: arcee-ai/trinity-mini - A robust, small, agile LLM optimized for conversational financial coaching
- **Purpose**: Provides personalized financial advice and insights based on user data
- **Server**: Uvicorn

#### Frontend
- **Framework**: React 18.3.1 with TypeScript
- **Build Tool**: Vite 6.3.5
- **UI Components**: 
  - Material-UI (@mui/material)
  - Radix UI components
  - Tailwind CSS for styling
- **Charts**: Recharts
- **State Management**: React hooks (local state)

## Data Models

### Transaction Data
- **Source**: Synthetic dataset derived from https://huggingface.co/datasets/mitulshah/transaction-categorization
- **User Profiles**: 3 unique user personas created to represent different financial archetypes:
  - **Student**: Young adult with limited income, focusing on essential expenses and learning financial habits
  - **Freelancer**: Variable income patterns, irregular cash flow, need for flexible budgeting
  - **Saver**: Stable income with focus on long-term financial goals and optimization
- **Schema**:
  - `date`: Transaction date
  - `amount`: Transaction amount (float)
  - `transaction_description`: Merchant description
  - `category`: Spending category
  - `user_id`: User identifier

### Goals Data
- **Storage**: JSON file (`goals.json`)
- **Schema**:
  ```json
  {
    "user_id": [
      {
        "description": "Goal description",
        "target_amount": 1000.0,
        "duration_months": 6
      }
    ]
  }
  ```

## AI Integration

### Core AI Capabilities

#### 1. Conversational Financial Coach
- **LLM Model**: arcee-ai/trinity-mini - Selected for its efficiency and effectiveness in financial coaching scenarios
- **Context-Aware Responses**: The AI receives real-time user financial data and goals to provide personalized advice
- **Natural Language Interface**: Users can ask questions in natural language and receive actionable financial guidance

#### 2. Intelligent Spending Analysis
- **Pattern Recognition**: AI identifies spending trends and anomalies across different categories
- **Personalized Insights**: Generates specific recommendations like "You've spent $120 on coffee this month. Brewing at home could save you over $1,000 a year!"
- **Behavioral Suggestions**: Provides non-judgmental advice to encourage positive financial habits

#### 3. Subscription & "Gray Charge" Detection
- **Machine Learning Algorithm**: Analyzes transaction history to identify recurring charges
- **Automatic Categorization**: Detects subscriptions, forgotten free trials, and other recurring expenses
- **Smart Alerts**: Notifies users about potential wasteful spending on unused services

#### 4. Goal Forecasting & Planning
- **Predictive Analytics**: AI analyzes income and spending patterns to forecast goal achievement
- **Adjustable Recommendations**: Suggests specific areas where users can cut back to reach financial goals
- **Progress Tracking**: Monitors progress towards goals and provides encouragement

### AI Implementation Architecture
```
User Query → Financial Data Retrieval → Context Building → LLM Prompt → AI Response → User Interface
```

### Data Privacy & Security
- **No Personal Data Storage**: Financial data is processed in real-time without persistent storage of sensitive information
- **Secure API Communication**: All communications with the LLM are encrypted and secure
- **User Consent**: AI only analyzes data with explicit user permission

## API Endpoints

### Health Check
- `GET /api/health`
- Returns: `{"status": "ok"}`

### Financial Summary
- `GET /api/financial-summary?user_id={user_id}`
- Returns comprehensive financial analysis including:
  - Income vs spending trends
  - Category breakdowns
  - Recent transactions
  - Detected subscription charges ("gray charges")
  - Monthly comparisons

### Chat Interface
- `POST /api/chat`
- Request body:
  ```json
  {
    "user_id": "string",
    "message": "string"
  }
  ```
- Returns:
  ```json
  {
    "reply": "AI coach response"
  }
  ```

## Core Components

### Backend Modules

#### `financial_analysis.py`
- **Purpose**: Analyze user spending patterns and generate insights
- **Key Functions**:
  - `get_user_financial_summary()`: Main analysis function
  - `detect_recent_gray_charges()`: Identify recurring subscriptions
  - `sort_and_round_categories()`: Data formatting helper

#### `chat_with_coach.py`
- **Purpose**: AI-powered financial coaching interface
- **Key Functions**:
  - `query_coach()`: Main chat interface
  - `build_system_prompt()`: Context-aware prompt generation
  - `format_goals_for_prompt()`: Goal data formatting

#### `goal_tracker.py`
- **Purpose**: Manage user savings goals
- **Key Functions**:
  - `get_user_goals()`: Retrieve user goals
  - `add_goal()`: Create new savings goal

#### `llm_client.py`
- **Purpose**: Interface with Together AI API
- **Key Functions**:
  - `query_llm()`: Send prompts to LLM and get responses

### Frontend Architecture

#### Main App Structure
- **Entry Point**: `src/main.tsx`
- **Root Component**: `src/app/App.tsx`
- **Component Library**: Extensive collection in `src/app/components/`

#### UI Component Categories
- **UI Components**: Reusable UI primitives (buttons, inputs, etc.)
- **Business Components**: Finance-specific components (charts, dashboards)
- **Layout Components**: Navigation, headers, sidebars

## Key Features

### 1. Intelligent Spending Insights Dashboard
- **AI-Powered Analysis**: Goes beyond simple categorization to identify trends and anomalies
- **Personalized Recommendations**: Friendly insights like, "You've spent $120 on coffee this month. Brewing at home could save you over $1,000 a year!"
- **Category Breakdowns**: Visual representation of spending across different categories
- **Monthly Comparisons**: Track spending changes over time

### 2. AI Finance Coach
- **Conversational Interface**: Natural language interaction with the AI coach
- **Context-Aware Responses**: Personalized advice based on user's financial data and goals
- **Real-Time Analysis**: Immediate responses to financial questions
- **Behavioral Guidance**: Non-judgmental suggestions for improving financial habits

### 3. Personalized Goal Forecasting
- **Goal Setting**: Users set financial goals (e.g., "Save $3,000 for a down payment in 10 months")
- **AI Forecasting**: Analyzes spending and income to predict goal achievement likelihood
- **Actionable Recommendations**: Specific suggestions on where to cut back to reach goals
- **Progress Tracking**: Visual progress indicators and milestone celebrations

### 4. Subscription & "Gray Charge" Detector
- **Automatic Detection**: AI scans transaction history for all recurring subscriptions
- **Forgotten Trials**: Identifies free trials that converted to paid services
- **Waste Identification**: Highlights potentially unwanted services for cancellation
- **Cost Impact Analysis**: Shows financial impact of recurring charges

### 5. Multi-Persona Support
- **Student Profile**: Tailored insights for young adults building financial habits
- **Freelancer Profile**: Adaptive guidance for variable income scenarios
- **Saver Profile**: Advanced optimization for goal-focused users

## Data Flow

### Financial Analysis Flow
1. User requests financial summary
2. Backend loads transaction data from CSV
3. Filters data by user_id and time period
4. Performs aggregations and calculations
5. Detects patterns (subscriptions, trends)
6. Returns structured JSON response

### Chat Flow
1. User sends message via frontend chat interface
2. Backend retrieves user's financial data and goals from JSON files
3. Builds context-aware system prompt with user's specific financial situation
4. Sends prompt to arcee-ai/trinity-mini LLM via Together AI
5. AI analyzes data and generates personalized financial advice
6. Returns AI response to frontend for display in chat interface
7. Frontend formats and presents response in conversational format

## Development Setup

### Backend Development
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Set API key
export TOGETHER_API_KEY="your_key_here"

# Run development server
cd backend && python server.py
```

### Frontend Development
```bash
# Install dependencies
cd dashboard-ui && npm install

# Run development server
npm run dev
```

## Success Metrics & Evaluation

### Behavioral Change Metrics
- **User Engagement**: Frequency of AI coach interactions and dashboard visits
- **Goal Achievement Rate**: Percentage of users who successfully meet their financial goals
- **Spending Pattern Changes**: Measurable reductions in wasteful spending categories
- **Subscription Cancellations**: Number of "gray charges" identified and cancelled

### Financial Visibility Metrics
- **Data Comprehension**: User understanding of their spending patterns
- **Insight Actionability**: Percentage of AI recommendations that users act upon
- **Dashboard Usage**: Time spent reviewing financial analytics
- **Category Awareness**: User knowledge of spending breakdowns

### Trust and Security Metrics
- **Data Privacy Perception**: User confidence in financial data security
- **AI Trust Level**: User trust in AI-generated financial advice
- **Transparency Score**: Clarity of AI decision-making processes
- **User Retention**: Continued usage over time

### AI Application Effectiveness
- **Response Relevance**: Accuracy and helpfulness of AI coach responses
- **Pattern Detection Success**: Rate of correct subscription and anomaly identification
- **Forecasting Accuracy**: Precision of goal achievement predictions
- **Personalization Quality**: Degree of tailored advice based on user profiles

### Code Quality Assessment
- **Architecture Quality**: Clean separation of concerns and modular design
- **Error Handling**: Robust exception handling and user feedback
- **Performance**: Response times and system efficiency
- **Maintainability**: Code documentation and testing coverage

## Submission Requirements

### Working Prototype/Demo
- ✅ Functional application demonstrating all core features
- ✅ AI-powered financial coaching interface
- ✅ Interactive dashboard with real-time data visualization
- ✅ Multi-persona support (student, freelancer, saver)

### Presentation (5-7 minutes)
- **Problem Introduction**: Clear explanation of the financial coaching challenge
- **Solution Demo**: Live demonstration of AI-powered features
- **Technical Implementation**: Overview of architecture and AI integration
- **Key Learnings**: Insights gained during development and testing

### Design Documentation
- ✅ Comprehensive design outline (this document)
- ✅ Technical stack details and architecture decisions
- ✅ Future enhancement roadmap
- ✅ AI integration strategy and implementation details

## Security Considerations

### Current Implementation
- CORS configured for local development
- No authentication system (hackathon scope)
- API key stored in environment variable

### Production Recommendations
- Implement user authentication
- Add API rate limiting
- Secure API key management
- Input validation and sanitization
- HTTPS enforcement
- Input validation and sanitization
- HTTPS enforcement

## Performance Considerations

### Data Processing
- CSV loading happens on-demand (could be optimized)
- Pandas operations for data aggregation
- No database indexing (JSON file storage)

### Frontend Performance
- React 18 with concurrent features
- Component lazy loading opportunities
- Chart rendering optimization potential

## Future Enhancements

### Backend Improvements
- Database integration (PostgreSQL/MongoDB)
- Real-time data synchronization
- Advanced analytics and ML models
- Webhook integrations for bank APIs

### Frontend Enhancements
- Mobile-responsive design improvements
- Progressive Web App (PWA) features
- Advanced charting capabilities
- Offline functionality

### Feature Additions
- Budget creation and tracking
- Investment portfolio management
- Bill payment reminders
- Financial goal gamification
- Multi-user household support

## Deployment Architecture

### Development Environment
- Frontend: Vite dev server (localhost:5173)
- Backend: Uvicorn (localhost:8000)
- Data: Local file system

### Production Recommendations
- Frontend: Static hosting (Vercel, Netlify)
- Backend: Containerized deployment (Docker)
- Database: Managed database service
- Load balancing and auto-scaling
- CDN for static assets

## Monitoring and Observability

### Current State
- Basic health check endpoint
- Console logging
- No structured monitoring

### Production Needs
- Application performance monitoring
- Error tracking and alerting
- User analytics and usage metrics
- System health dashboards
- Log aggregation and analysis

---

**Last Updated**: January 11, 2026
**Version**: 1.0
**Hackathon**: PANW Hackathon 2026
