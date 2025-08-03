# Growthzi AI Social Media Manager

A web application for generating, previewing, scheduling, and publishing social media posts powered by AI. Connects to a Facebook page (simulated) and leverages Groq LLM API for content generation, allowing users to automate social media marketing workflows from business profile extraction and industry news to scheduled posts publishing.

## Table of Contents

- [Features](#features)  
- [Demo](#demo)  
- [Tech Stack](#tech-stack)  
- [Architecture & Flow](#architecture--flow)  
- [Setup and Installation](#setup-and-installation)  
- [Usage](#usage)  
- [API Endpoints](#api-endpoints)  
- [Project Structure](#project-structure)  
- [Key Components](#key-components)  
- [Future Improvements](#future-improvements)  
- [Known Limitations](#known-limitations)  
- [License](#license)

## Features

- Connect and simulate Facebook page linkage with mock access tokens  
- Fetch business profile details (name, industry, services, tone) from any business website URL using web scraping and Groq LLM inference  
- Retrieve relevant current industry news for the business  
- AI-powered generation of multiple social media posts based on business profile and trending news, customizable by tone and post type  
- Preview, edit, and delete generated posts before scheduling  
- Create a weekly post schedule with preferred posting days and frequency  
- Edit scheduled posts, delete posts, and reset schedules  
- Simulated publishing of scheduled posts to connected Facebook page with mock Facebook post links  
- Clear React frontend UI with intuitive flow and status/error messages

## Demo

*(Optional: Add screenshots or link to a live demo if available. Place here the screenshots of the UI components such as the Business Profile display, Generated Posts preview, Scheduler table, Publish confirmation, etc.)*

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS  
- **Frontend:** React, JavaScript, HTML, CSS  
- **AI Service:** Groq LLM API (llama-3.1-8b-instant model)  
- **Other:** BeautifulSoup (web scraping), Requests

## Architecture & Flow

1. User connects a Facebook page (simulated) via a connect button.  
2. User enters a business website URL → backend scrapes and analyzes the website to extract the business profile using Groq LLM.  
3. Based on extracted industry information, backend fetches relevant current news headlines.  
4. User selects preferences and triggers AI-generated post creation powered by Groq API.  
5. Generated posts are shown with edit and delete options for fine-tuning.  
6. User schedules posts on preferred days and frequency using the weekly planner.  
7. The schedule can be edited or reset.  
8. User publishes posts to the connected Facebook page using a simulation endpoint, which provides a mock Facebook post link.

## Setup and Installation

### Backend Setup

1. **Clone the repository:**

```
git clone 
cd 
```

2. **Create a Python virtual environment:**

```
python -m venv venv
source venv/bin/activate   # Unix/macOS
venv\Scripts\activate      # Windows
```

3. **Install dependencies:**

```
pip install -r requirements.txt
```

4. **Create a `.env` file in the root project directory with your API keys:**

```
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the Flask backend:**

```
python run.py
```

This will start the backend server on `http://localhost:5000`.

### Frontend Setup

1. Navigate to the React app folder (e.g., `frontend/` or root if combined):  

```
cd frontend
```

2. Install packages:

```
npm install
```

3. Start the React development server:

```
npm start
```

The React app will run on `http://localhost:3000` by default.

Make sure the backend API URL configured in `SocialMediaManager.jsx` matches your backend location (`http://localhost:5000/api`).

## Usage

1. Open the React frontend in your browser (`http://localhost:3000`).
2. Click **Connect Facebook** to simulate linking a Facebook page.
3. Enter the **Business Website URL** and click **Generate Posts (Full Flow)**. This triggers profile retrieval, news fetch, and AI post generation.
4. Preview, edit, or delete generated posts.
5. Set your preferred post frequency and days, then click **Generate Weekly Schedule**.
6. Edit or delete scheduled posts as needed.
7. Publish posts to the connected Facebook page; view the simulated Facebook post link below the publish confirmation.

## API Endpoints

| Endpoint                     | Method  | Description                                    |
|-----------------------------|---------|------------------------------------------------|
| `/api/facebook/connect`      | POST    | Simulates Facebook page connection              |
| `/api/facebook/publish`      | POST    | Simulate publishing a post, returns mock post URL |
| `/api/business/profile`      | POST    | Extract business profile from website URL       |
| `/api/news/industry-news`    | POST    | Fetch current industry news based on industry   |
| `/api/content/generate-posts`| POST    | Generate AI social media posts                   |
| `/api/weekly-planner/`       | POST    | Generate a weekly post schedule                   |
| `/api/weekly-planner/`       | GET     | Get current weekly post schedule                  |
| `/api/weekly-planner/`  | PUT     | Update post content for a day                      |
| `/api/weekly-planner/`  | DELETE  | Delete scheduled post for a day                    |
| `/api/weekly-planner/reset`  | DELETE  | Reset entire weekly schedule                       |

## Project Structure


/app
  /routes
    business.py
    news.py
    content.py
    planner.py
    facebook.py
  /services
    facebook.py
    generator.py
    scraper.py
    scheduler.py
frontend/
  src/
    SocialMediaManager.jsx
    index.css
.env
requirements.txt
run.py
.gitignore
```

## Key Components

### Backend

- **Flask API** handles scraping, AI generation, scheduling, Facebook simulation.
- **Groq API usage** for generating text content based on scraped profiles and news.
- **WeeklyScheduler** manages post scheduling saved in a JSON file.
- **Facebook simulation** mocks page connect and post publishing.

### Frontend

- **React component `SocialMediaManager.jsx`** provides UI for Facebook connection, profile/news fetch, generating posts, scheduling, preview/edit/delete, and publishing.
- Input validation, loading states, and error messages.
- Editable post previews before scheduling.
- Display of simulated Facebook post links after publishing.

## Future Improvements

- Integrate real Facebook Graph API for publishing to live pages.
- Add authentication and Facebook OAuth login.
- Improve UI/UX for scheduling calendar and drag-drop posts.
- Support multi-platform posting (Twitter, Instagram, LinkedIn).
- Add analytics dashboard for post engagement metrics.
- Use persistent database instead of JSON files.

## Known Limitations

- Facebook page connection and publishing are simulated only.
- Post links point to mock URLs, not live Facebook posts.
- Industry news fetched may be limited to simple APIs or mock data.
- Scheduler uses JSON files, not scalable for production.
- Basic UI without advanced scheduling/calendar views.
