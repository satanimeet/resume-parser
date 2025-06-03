# Resume Parser

A powerful resume parsing application built with Streamlit and Hugging Face Transformers that extracts key information from resumes.

## Features

- Extract personal information (name, email, phone)
- Parse education details with dates and institutions
- Identify skills and categorize them
- Extract social media profiles (LinkedIn, GitHub)
- Modern and user-friendly interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-parser.git
cd resume-parser
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Technologies Used

- Python
- Streamlit
- Hugging Face Transformers
- spaCy
- BERT (dslim/bert-base-NER)

## Project Structure

- `app.py`: Main Streamlit application
- `model.py`: Core parsing logic and model integration
- `requirements.txt`: Project dependencies

## License

MIT License 