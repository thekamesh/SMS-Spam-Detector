# 📱 SMS Spam Detector

An **Machine Learning-based SMS Spam Detection System** that classifies SMS messages as **Spam** or **Ham (Not Spam)** using Natural Language Processing (NLP) and Machine Learning.

The application provides an interactive **Streamlit web interface** where users can enter an SMS message and instantly get the predicted result.

## 🚀 Live Demo

👉 **Try the deployed application:**  
[SMS Spam Detector – Live App](https://sms-spam-detector--bykamesh.streamlit.app/?utm_source=chatgpt.com)

## 💻 GitHub Repository

👉 **Source Code:**  
[SMS Spam Detector – GitHub Repository](https://github.com/thekamesh/SMS-Spam-Detector?utm_source=chatgpt.com)

---

## 📌 Project Overview

Spam messages are unwanted messages that may contain advertisements, fraudulent offers, fake rewards, or suspicious links.

This project uses **Natural Language Processing (NLP)** to process SMS text and a **Multinomial Naive Bayes** machine learning model to classify messages into:

- ✅ **HAM** – Normal / legitimate SMS
- 🚨 **SPAM** – Unwanted or suspicious SMS

---

## 🔄 Machine Learning Workflow

```text
SMS Message
     ↓
Text Preprocessing
     ↓
Tokenization
     ↓
Stopword Removal
     ↓
Stemming
     ↓
TF-IDF Vectorization
     ↓
Multinomial Naive Bayes
     ↓
HAM / SPAM Prediction
```

---

## 🧠 NLP Preprocessing

The SMS text is processed before sending it to the machine learning model.

The preprocessing pipeline includes:

1. Convert text to lowercase
2. Tokenize the text
3. Remove non-alphanumeric characters
4. Remove English stopwords
5. Apply Porter Stemming
6. Convert processed text into numerical features using **TF-IDF**

---

## 🤖 Machine Learning Model

The project uses:

**Multinomial Naive Bayes**

Naive Bayes is well suited for text classification problems because it performs efficiently with high-dimensional text features such as TF-IDF.

### Prediction Mapping

| Prediction | Meaning |
|---|---|
| `0` | HAM |
| `1` | SPAM |

---

## ✨ Features

- 📩 SMS message input
- 🤖 Machine Learning based prediction
- 🚨 Spam detection
- ✅ Ham detection
- 📊 Prediction probability
- 🔤 NLP preprocessing
- 📈 Message statistics
- 🌐 Interactive Streamlit interface
- ⚡ Fast prediction

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **NLTK**
- **TF-IDF**
- **Multinomial Naive Bayes**
- **Streamlit**
- **Pickle**

---

## 📂 Project Structure

```text
SMS-Spam-Detector/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── runtime.txt
└── README.md
```

### File Description

| File | Description |
|---|---|
| `app.py` | Streamlit application |
| `model.pkl` | Trained machine learning model |
| `vectorizer.pkl` | Saved TF-IDF vectorizer |
| `requirements.txt` | Required Python libraries |
| `runtime.txt` | Python runtime version |
| `README.md` | Project documentation |

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/thekamesh/SMS-Spam-Detector.git
```

### 2. Navigate to the project folder

```bash
cd SMS-Spam-Detector
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Example Predictions

### 🚨 Spam Example

```text
Congratulations! You have won a $1000 prize. Click here to claim now!
```

**Prediction:** SPAM

### ✅ Ham Example

```text
Hey bro, are you free tonight? Let's meet for dinner.
```

**Prediction:** HAM

---

## 📊 Model Output

The application displays:

- Predicted class
- Spam probability
- Ham probability
- Processed text
- Message character count
- Message word count

---

## 🌐 Deployment

The application is deployed using **Streamlit Community Cloud**.

### Live Application

[Open SMS Spam Detector](https://sms-spam-detector--bykamesh.streamlit.app/?utm_source=chatgpt.com)

---

## 🎯 Use Cases

This project can be used as a basic demonstration of:

- NLP text classification
- Spam message detection
- Machine Learning model deployment
- TF-IDF feature extraction
- Naive Bayes classification
- Streamlit application development

---

## 🔮 Future Improvements

Possible future improvements include:

- Improve model accuracy with larger datasets
- Compare multiple classification algorithms
- Add multilingual SMS detection
- Add batch SMS prediction through CSV upload
- Add model performance metrics
- Improve detection of phishing and scam messages
- Deploy an API using FastAPI

---

## 👨‍💻 Author

**Kamesh Gupta**

GitHub:  
[thekamesh on GitHub]

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
