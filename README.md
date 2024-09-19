## Week 1

# Content Moderation API:

This project implements a content moderation system using a Flask API that can classify text as toxic or non-toxic. The system uses a pre-trained BERT model for local inference and integrates with a LLM API for more advanced moderation tasks. Additionally, the API provides monitoring capabilities using Prometheus and visualizes metrics in Grafana.

## Features

- **Text Classification:** Detect whether a given text contains undesirable or toxic language.
- **Model Comparison:** Compare the performance of the local BERT model with the FastChat LLM API.
- **De-escalation:** Automatically return a cleaned version of flagged text, free of undesirable language.
- **Monitoring:** Track API metrics such as request counts and inference times using Prometheus.
- **Visualization:** Visualize real-time metrics in Grafana.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8+
- Flask
- PyTorch
- Transformers
- Prometheus
- Grafana

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://git.fim.uni-passau.de/ahmadima/ai-lab.git
   cd content-moderation-api
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download and set up Prometheus:**

   - Download Prometheus from [here](https://prometheus.io/download/).
   - Extract the file and navigate to the directory.
   - Update the `prometheus.yml` configuration file to scrape metrics from your Flask API:

     ```yaml
     scrape_configs:
       - job_name: 'flask_app'
         static_configs:
           - targets: ['localhost:5000']  # Adjust to match your Flask server address
     ```

   - Start Prometheus:

     ```bash
     ./prometheus --config.file=prometheus.yml
     ```

4. **Download and set up Grafana:**

   - Download Grafana from [here](https://grafana.com/grafana/download).
   - Extract the file and navigate to the directory.
   - Start Grafana:

     ```bash
     ./bin/grafana-server
     ```

   - Access Grafana at `http://localhost:3000` and add Prometheus as a data source.

## Usage

### Running the Flask API

1. **Train the BERT model (optional):**

   If you want to train the BERT model on your dataset:

   ```python
   python train_model.py
   ```

2. **Start the Flask server:**

   ```bash
   python app.py
   ```

3. **Access the API:**

   The API will be running on `http://localhost:5000`. You can interact with it using cURL, Postman, or any other HTTP client.

   Example request:

   ```bash
   curl -X POST http://localhost:5000/check-text \
   -H "Content-Type: application/json" \
   -d '{"text": "This is a toxic message", "model": "llm"}'
   ```

### Monitoring with Prometheus

Prometheus will scrape the `/metrics` endpoint exposed by the Flask app to collect metrics.

- **Metrics endpoint:** `http://localhost:5000/metrics`

### Visualization with Grafana

1. **Create a Dashboard:**

   - Log in to Grafana at `http://localhost:3000`.
   - Add Prometheus as a data source.
   - Create a new dashboard and add panels to visualize metrics such as `request_count` and `inference_time_seconds`.

## API Endpoints

- **POST /check-text**

  Checks the provided text for undesirable language.

  - **Request:**

    ```json
    {
      "text": "Your text here",
      "model": "bert"  // or "llm"
    }
    ```

  - **Response:**

    ```json
    {
      "original_text": "Your text here",
      "flagged": true,
      "probability": 0.85,
      "target": "unknown",
      "deescalated_text": "Cleaned text"
    }
    ```

- **GET /metrics**

  Exposes Prometheus metrics.



## Acknowledgments

- Hugging Face for the Transformers library.
- Prometheus for monitoring.
- Grafana for visualization.
- FastChat API for LLM capabilities.


## Week 2

### README for Story Generator App:

## Story Generator App

The Story Generator App is a web application built using Django that allows users to generate and manage personalized stories. The app includes functionalities such as user registration, authentication, profile management, and the ability to generate, view, and store stories with an audio playback feature.

### Features

#### 1. **User Authentication**
   - **Registration**: Users can sign up by providing their first name, last name, username, and password. The registration form includes validation to ensure the passwords match and meet security requirements.
   - **Login**: Registered users can log in using their username and password. The login page is designed to be user-friendly, with a clean and simple interface.
   - **Logout**: Users can securely log out of their accounts.
   - **Profile Management**: Authenticated users can view and update their profile information, including first name, last name, and password.

#### 2. **Story Generation**
   - **Story Input Form**: Users can generate a personalized story by providing their name, a friend’s name, and a story topic. The form is designed with user experience in mind, including labels, placeholders, and required fields for input validation.
   - **Story Display**: Once generated, the story is displayed on the page along with an audio playback feature. The story is also saved to the user’s profile, allowing for future retrieval.

#### 3. **Audio Playback**
   - **Audio Integration**: Each generated story is accompanied by an audio file that can be played directly on the website. The audio player is integrated into the story display and is responsive across devices.

#### 4. **User Profile**
   - **Profile Settings**: Users can update their profile details, including changing their password. The profile page is secured and only accessible to authenticated users.
   - **Story History**: Users can view a history of all stories they’ve generated. Each story is listed with the name, friend’s name, topic, and creation date, along with a link to read the full story and an audio playback option.

#### 5. **Responsive Design**
   - The entire application is designed to be responsive, ensuring a seamless experience on both desktop and mobile devices. Bootstrap is used extensively for layout management and styling.

### Installation

1. **Clone the Repository**:
   ```
   git clone https://git.fim.uni-passau.de/ahmadima/ai-lab.git
   cd story-generator-app
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```
   python manage.py runserver
   ```

7. **Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:8000/`.

### Usage

- **Register an Account**: Go to the registration page and create an account.
- **Log In**: Use your credentials to log in.
- **Generate a Story**: Navigate to the story generation page, fill in the details, and generate your story.
- **Listen to Audio**: After generating the story, use the built-in audio player to listen to the story.
- **Manage Profile**: Update your profile information and view your story history from the profile page.

### Folder Structure

- **`/story_app/`**: Contains the main Django project settings and URLs.
- **`/application/`**: Contains the core app logic, including models, views, and templates for story generation.
- **`/templates/`**: Includes the HTML files for various pages like login, registration, profile, and home.
- **`/static/`**: Contains static files like CSS, JS, and images used in the project.


## Week 3


# Django LLM-Powered Module Query Assistant

This Django application allows users to query university module information using a custom Large Language Model (LLM) API. The application extracts module data from a PDF, stores it in a vector store for efficient querying, and enhances responses with contextual information generated by the LLM.

## Features

- **Module Extraction**: Extracts and processes module information from a PDF file.
- **Vector Store**: Stores module descriptions as vectors for similarity-based querying.
- **LLM Integration**: Uses a custom LLM API to generate detailed, contextual responses.
- **Web Interface**: Provides a user-friendly web interface for submitting queries and viewing results.

## Requirements

- Python 3.7+
- Django 3.2+
- Pandas
- Scikit-learn
- Requests
- pdfplumber

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://git.fim.uni-passau.de/ahmadima/ai-lab.git
cd yourrepository
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, manually install the required packages:

```bash
pip install django pandas scikit-learn requests pdfplumber
```

### 3. Place the PDF File

Place the module catalog PDF file in the `static/pdf/` or `data/` directory (depending on your project structure):

```bash
mkdir -p passau_ai_assistant/static/pdf
mv /path/to/your/Module_Catalogue_M.Sc.AI-Engineering.pdf passau_ai_assistant/static/pdf/
```

### 4. Extract and Vectorize Modules

Run the following Django management commands to extract module information from the PDF and vectorize the module descriptions:

```bash
python manage.py extract_modules
python manage.py vectorize_modules
```

### 6. Run the Server

Start the Django development server:

```bash
python manage.py runserver
```

### 7. Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:8000/modules/query/
```

You should see a search form where you can input queries related to university modules.

## Usage

1. **Submit a Query**: Enter a query in the form (e.g., "deep learning") and submit.
2. **View Results**: The application will return the most relevant module information along with a similarity score and a detailed response generated by the LLM API.





