# **AI-Powered Web Scraper**  

## **📌 Overview**  
This **AI-Powered Web Scraper** extracts information from websites using **BeautifulSoup** and **AI-based text parsing**. It scrapes web content, cleans the extracted text, and allows users to extract meaningful data using natural language queries. The scraper is built with **Streamlit** for an interactive UI and integrates **Ollama AI** for intelligent content extraction.  

## **✨ Features**  
### **1️⃣ Website Scraping**  
- Fetches the complete HTML structure of a webpage.  
- Extracts text content while removing scripts, styles, and unnecessary elements.  
- Splits large DOM content into manageable chunks for processing.  

### **2️⃣ AI-Powered Information Extraction**  
- Uses **Ollama AI** to analyze and extract relevant data from scraped content.  
- Allows users to specify extraction queries like:  
  - Extract product names and prices.  
  - Find contact details.  
  - Summarize the main content of an article.  
- Provides a **fallback parser** if AI is unavailable.  

### **3️⃣ Interactive UI with Streamlit**  
- User-friendly interface for entering URLs and extraction queries.  
- Live progress updates while scraping and analyzing data.  
- Download extracted data as a text file.  

### **4️⃣ Modular and Scalable**  
- Built with modular functions for easy customization.  
- Supports AI-based content parsing while offering a rule-based fallback method.  
- Can be extended for **structured data extraction (JSON, CSV, etc.)**.  

## **🛠️ How It Works**  
1. **User Inputs URL**: Enter a website URL into the Streamlit interface.  
2. **Scraping Process**: The scraper fetches and cleans webpage content.  
3. **AI Processing**: User specifies what information to extract, and **Ollama AI** processes the request.  
4. **Results Display**: Extracted data is shown in a structured format and can be downloaded.  

## **⚡ Why Use This Web Scraper?**  
- **AI-Powered Analysis** – Extracts structured information from unstructured web pages.  
- **Easy to Use** – No need for coding; just enter a URL and specify what to extract.  
- **Modular Design** – Easily customizable for different web scraping needs.  
- **Handles Large Content** – Automatically splits and processes large webpages.  

## **🚀 Installation & Setup**  
To install the required dependencies:  
```bash
pip install -r requirements.txt
```  
Then, start the Streamlit app:  
```bash
streamlit run main.py
```  

## **⚠️ Disclaimer**  
This tool is intended for ethical web scraping. Always check and comply with a website’s `robots.txt` policy before scraping. Unauthorized scraping may violate terms of service.  

---  

### 📌 Author: TIPU REHMAN  

- app link: https://ai-web-scrapper-9vwxh9fpyjfeljddctehyp.streamlit.app/
