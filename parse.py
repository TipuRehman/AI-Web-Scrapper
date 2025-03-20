import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_with_ollama(dom_chunks, parse_description):
    """
    Parse DOM content chunks, gracefully handling the case when Ollama is not available.
    
    Args:
        dom_chunks (list): List of DOM content chunks
        parse_description (str): Description of what to parse
        
    Returns:
        str: Parsed and formatted result
    """
    # Check if Ollama is installed
    try:
        import ollama
        use_ollama = True
    except ImportError:
        use_ollama = False
    
    # If Ollama is not available or the model isn't found, use the fallback implementation
    if not use_ollama:
        return fallback_parser(dom_chunks, parse_description)
    
    # Try to use Ollama if available
    try:
        # Process each chunk and collect results
        results = []
        
        for i, chunk in enumerate(dom_chunks):
            # Create a prompt for the AI
            prompt = f"""
            You are an AI web scraper assistant. Your task is to extract information from websites.
            
            USER REQUEST: {parse_description}
            
            WEBSITE CONTENT (CHUNK {i+1}/{len(dom_chunks)}):
            {chunk}
            
            Based ONLY on the content above, please extract the information requested.
            If you cannot find the requested information in this chunk, respond with "No relevant information found in this chunk."
            Format your response as plain text with appropriate structure.
            """
            
            # Get response from the model using ollama directly
            response = ollama.generate(model="llama2", prompt=prompt)
            result_text = response['response']
            
            # Only include meaningful responses
            if "No relevant information found in this chunk" not in result_text:
                results.append(result_text)
        
        # If no useful information was found
        if not results:
            return "No relevant information found on the website based on your request."
        
        # Combine and format results
        combined_result = "\n\n".join(results)
        
        # Create a final summary prompt
        final_prompt = f"""
        You are an AI web scraper assistant. Your task is to summarize the following information extracted from a website.
        
        USER REQUEST: {parse_description}
        
        EXTRACTED CONTENT:
        {combined_result}
        
        Please create a final, clean, well-formatted summary of the information above.
        Format your response as plain text with appropriate structure.
        """
        
        # Get final summary
        final_response = ollama.generate(model="llama2", prompt=final_prompt)
        final_summary = final_response['response']
        
        return final_summary
        
    except Exception as e:
        # If anything goes wrong with Ollama, use the fallback parser
        return fallback_parser(dom_chunks, parse_description, error=str(e))


def fallback_parser(dom_chunks, parse_description, error=None):
    """
    Fallback parser that extracts basic information without using AI.
    
    Args:
        dom_chunks (list): List of DOM content chunks
        parse_description (str): Description of what to parse
        error (str, optional): Error message if applicable
        
    Returns:
        str: Extracted information
    """
    # Extract key sentences from the content
    all_sentences = []
    for chunk in dom_chunks:
        # Split content into sentences (basic implementation)
        sentences = [s.strip() for s in chunk.replace('\n', ' ').split('.') if len(s.strip()) > 20]
        all_sentences.extend(sentences[:5])  # Take first 5 substantial sentences from each chunk
    
    # Format relevant keywords from the parse description
    keywords = [word.lower() for word in parse_description.split() if len(word) > 3]
    
    # Try to find sentences relevant to the keywords
    relevant_sentences = []
    for sentence in all_sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in keywords):
            relevant_sentences.append(sentence)
    
    # Format the response based on the parse description
    table_requested = "table" in parse_description.lower()
    
    if table_requested:
        # Create a simple markdown table with the extracted information
        table_content = "| Information | Content |\n| --- | --- |\n"
        
        for i, sentence in enumerate(relevant_sentences[:10]):  # Limit to 10 rows
            # Extract key-value pairs if possible
            if ":" in sentence:
                parts = sentence.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip()
                table_content += f"| {key} | {value} |\n"
            else:
                table_content += f"| Item {i+1} | {sentence} |\n"
        
        result = f"""
# Extracted Information

{table_content}

"""
    else:
        # Format as a simple list
        result = "# Extracted Information\n\n"
        for sentence in relevant_sentences[:15]:  # Limit to 15 items
            result += f"- {sentence}\n"
    
    # Add error message if applicable
    if error:
        result += f"\n\n> Note: AI-powered extraction failed with error: {error}\n"
        result += "> Using basic extraction instead. For better results, install Ollama and the llama2 model."
    
    return result


def parse_with_api(dom_chunks, parse_description, api_key=None):
    """
    Alternative parsing method using an external API (e.g., OpenAI).
    This is a fallback if Ollama is not available.
    
    Args:
        dom_chunks (list): List of DOM content chunks
        parse_description (str): Description of what to parse
        api_key (str, optional): API key for the service
        
    Returns:
        str: Parsed and formatted result
    """
    # This is just a placeholder function
    # Implement if you want to use an external API instead of Ollama
    return "API parsing not implemented. Please use Ollama parsing or the fallback parser."