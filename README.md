# Medical Symptom Analyzer

A Streamlit application that uses AI to analyze medical symptoms and recommend appropriate doctors based on the analysis.

![Medical Symptom Analyzer](https://i.imgur.com/your-image-upload-id.png)
<!-- Note: You'll need to upload this screenshot to an image hosting service and replace the URL above with the actual image URL -->

## 📋 Features

- Interactive symptom analysis through an AI-powered chatbot.
- Display of possible medical conditions with likelihood indicators
- Specialist doctor recommendations based on symptoms
- Comprehensive doctor directory with search and filter capabilities
- Detailed doctor profiles including specialization, experience, hospital, availability, languages, and more
- User-friendly interface with helpful guidance
- Secure API key management

## 🔧 Technology Stack

- **Streamlit**: For the web application interface
- **Groq API**: For AI-powered symptom analysis
- **Python**: Core programming language
- **Pandas**: For data handling and CSV processing
- **dotenv**: For environment variable management

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CzPhantom10/Medical_chatbot.git
   cd MEDICAL CHATBOT
   ```

2. Create a virtual environment:
   ```bash
   python -m venv myenv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project directory with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. Make sure the `doctors_database.csv` file is in the project directory.

## 🚀 Usage

1. Run the application:
   ```bash
   streamlit run chatbot.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Use the application:
   - Enter your symptoms in the text area
   - Click "Analyze Symptoms"
   - Review the analysis results and doctor recommendations
   - Use the "Find a Doctor" page to search and filter the doctor database

## 📌 Important Notes

- This application is for informational purposes only and is not a substitute for professional medical advice
- Always consult with qualified healthcare professionals for proper diagnosis and treatment
- Keep your API key secure and never commit your `.env` file to version control

## 🔒 Environment Variables

Create a `.env` file in the project root with the following variables:

```
GROQ_API_KEY=your_groq_api_key_here
```

## 📁 Project Structure

```
medical-symptom-analyzer/
├── app.py               # Main Streamlit application file
├── doctors_database.csv # Database of doctors with their details
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not tracked in Git)
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 🛠️ Customization

### Editing the Doctor Database

You can modify the doctor database by editing the `doctors_database.csv` file. Each doctor entry includes:

- name: The doctor's full name
- specialization: The doctor's medical specialty
- experience: Years of experience
- contact: Contact phone number
- address: Office address
- hospital: Associated hospital or medical center
- availability: Working hours
- languages: Languages spoken
- education: Educational background and training
- rating: Patient satisfaction rating (decimal number)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request