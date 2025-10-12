# Job-tracker-agent
AI-powered job application tracker that automatically extracts job details from URLs and saves them to Google Sheets using LangGraph and OpenAI.


## Requirements

Before running the app, you'll need to set up the following:

### 1. OpenAI API Key

### 2. Google Cloud Service Account (for Google Sheets)

**What:** Service account credentials to write to Google Sheets programmatically.

**How to get it:**

#### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "Job Tracker")
3. Wait for project creation to complete

#### Step 2: Enable APIs
1. In the search bar, type "Google Sheets API"
2. Click on it and click "Enable"
3. Search for "Google Drive API"
4. Click on it and click "Enable"

#### Step 3: Create Service Account
1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name it (e.g., "job-tracker-bot")
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

#### Step 4: Create Key
1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON"
5. Click "Create" - a JSON file will download
6. **Rename it to `credentials.json`** and save it in your project root

#### Step 5: Get Service Account Email
1. Open the `credentials.json` file
2. Find the `client_email` field to add it to Google Sheets as an editor.
3. Copy this email (looks like: `job-tracker-bot@your-project.iam.gserviceaccount.com`)

### 3. Google Sheet Setup

**What:** A Google Sheet to store your job applications.

**How to set it up:**

1. **Create a new Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com)
   - Click "Blank" to create a new sheet
   - Name it "Job Tracker"

2. **Add column headers** (first row)
