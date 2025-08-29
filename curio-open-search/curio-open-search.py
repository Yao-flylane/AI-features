import streamlit as st
import requests
import json
import re

st.set_page_config(page_title="Curio AI Tutor", page_icon="🔍")
st.title("🔍 Curio AI Tutor")

def check_youtube_availability(url):
    """Check if a YouTube video is available and accessible"""
    import requests
    
    try:
        # Try to access the YouTube video page
        response = requests.head(url, timeout=5, allow_redirects=True)
        
        # Check if the response is successful
        if response.status_code == 200:
            return True
        else:
            return False
            
    except Exception as e:
        # If any error occurs (timeout, connection error, etc.), consider it unavailable
        return False

def convert_direct_links_to_embedded(text):
    """Convert direct YouTube and PDF links in text to embedded content"""

    # Find YouTube links
    youtube_pattern = r'https://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
    
    def replace_youtube(match):
        url = match.group(0)
        video_id = match.group(1)
        if len(video_id) == 11:  # Valid YouTube video ID
            return f'\n\n<iframe width="400" height="225" src="https://www.youtube.com/embed/{video_id}" title="YouTube video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n'
        else:
            # If YouTube embedding fails, show with emoji but no clickable link
            return f'\n\n🎥 {url}\n'
    
    # Find PDF links
    pdf_pattern = r'https://[^\s]+\.pdf'
    
    def replace_pdf(match):
        url = match.group(0)
        return f'\n\n📄 {url}\n'
    
    # Apply replacements
    text = re.sub(youtube_pattern, replace_youtube, text)
    text = re.sub(pdf_pattern, replace_pdf, text)
    
    return text

def replace_citations_with_content(text, search_results):
    """Make citations [1], [2], etc. clickable links to URLs"""
    if not search_results:
        return text
    
    import re
    citation_pattern = r'\[(\d+)\]'
    
    def replace_citation_with_link(match):
        citation_num = int(match.group(1))
        if citation_num <= len(search_results):
            result = search_results[citation_num - 1]  # Convert to 0-based index
            url = result.get('url', '')
            title = result.get('title', 'Resource')
            
            # Make citation clickable - keep the [1], [2] format but make it a link
            return f'[{citation_num}]({url} "{title}")'
        else:
            return match.group(0)  # Keep original if citation number is out of range
    
    # Replace all citations with clickable links
    text_with_links = re.sub(citation_pattern, replace_citation_with_link, text)
    
    return text_with_links

# Sidebar configuration
st.sidebar.header("🔧 Configuration")

# Perplexity API Key input
perplexity_api_key = st.sidebar.text_input("API Key", type="password")

# Model selection
model = st.sidebar.selectbox(
    "Model",
    ["sonar", "sonar-pro"],
    help="Choose the model to use"
)

# Temperature control
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Controls randomness in responses (0 = focused, 1 = creative)"
)

# Search recency filter
search_recency = st.sidebar.selectbox(
    "Search Recency",
    ["", "day", "week", "month", "year"],
    help="Filter search results by recency"
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Curio AI Tutor, tell me what would you like to learn today? I will recommend you the best resources to learn. With your grade level, I will personalize the resources for you!"}
    ]

# Reset chat history button
if st.sidebar.button("Reset chat history"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Curio AI Tutor, tell me what would you like to learn today? I will recommend you the best resources to learn. With your grade level, I will personalize the resources for you!"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Display message content directly (citations will be converted to embedded URLs)
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input(placeholder="Tell me what would you like to learn today and your grade level?"):
    system_prompt = """
    You are a specialized AI learning guide. Your goal is to help users learn any subject or topic 
    by curating high-quality free learning resources (YouTube videos and PDF documents).

    Workflow:
    1. When the user provides a subject or topic:
    - If a grade level or skill level is provided, personalize the resources accordingly.
    - If not provided, politely ask for their grade level (e.g., high school, college, beginner, advanced).

    2. Provide a curated set of resources in two sections:
    - ***PDFs***: Direct links to free PDF resources (must end with .pdf).
    - ***YouTube***: Direct links to single YouTube videos (not playlists unless explicitly requested).

    3. After presenting resources, ask the user what they would like to do next. Options include:
    - Narrow down the subject (suggest a list of subtopics/subfields they can choose from).
    - Ask follow-up questions (clarifications, related subjects, etc.).
    - Regenerate a new/different set of resources.
    - Provide their grade/level if not already specified.
    - Or say they are satisfied and want to stop.

    4. If the user narrows/refines, regenerate with the new focus.
    5. If the user regenerates, produce different resources than before.
    6. Continue until the user explicitly says they are happy or wants to stop.

    Important:
    - Always provide citations with the resource links.
    - Never recommend paid, login-gated, or irrelevant resources.
    - Never recommend resources for users to search for.
    - Only provide working YouTube video links (https://www.youtube.com/watch?v=...).
    - Only provide direct .pdf links that are publicly accessible.
    - Never invent or guess links. Only suggest real, existing URLs.
    """

    st.chat_message("user").write(prompt)

    if not perplexity_api_key:
        st.info("Please add your Perplexity API key to continue.")
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build messages for API call
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history (excluding the current user message we just added)
    for message in st.session_state.messages[1:]:  # Exclude the last message we just added
        if message["role"] in ["assistant"]:
            messages.append({"role": message["role"], "content": message["content"]})
        elif message["role"] in ["user"]:
            messages.append({"role": message["role"], "content": message["content"]+". I want youtube videos and pdfs resources, make sure all urls are working and available"})
    
    with st.chat_message("assistant"):
        # Create a placeholder for streaming content
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream with requests and collect metadata
        try:
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {perplexity_api_key}",
                "Content-Type": "application/json"
            }
            # Build payload with user message and system context
            payload = {
                "model": model,
                "messages": messages,
                "stream": True
            }
            
            # Add search recency filter if selected
            if search_recency:
                payload["search_recency_filter"] = search_recency
            
            st.sidebar.write("🔄 Streaming response and collecting metadata...")
            
            # Stream the response
            response = requests.post(url, headers=headers, json=payload, stream=True, timeout=300)
            response.raise_for_status()
            
            content = ""
            metadata = {}
            message_placeholder = st.empty()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data_str)
                            
                            # Process content
                            if 'choices' in chunk and chunk['choices'][0]['delta'].get('content'):
                                content_piece = chunk['choices'][0]['delta']['content']
                                content += content_piece
                                
                                # Display with streaming cursor
                                streaming_display = content + "▌"
                                message_placeholder.markdown(streaming_display, unsafe_allow_html=True)
                            
                            # Collect metadata
                            for key in ['search_results', 'usage']:
                                if key in chunk:
                                    metadata[key] = chunk[key]
                                    
                        except json.JSONDecodeError:
                            continue
            st.sidebar.write(f"📤 {content}")
            # Remove cursor and add search results if available
            enhanced_response = content
            
            if 'search_results' in metadata and metadata['search_results']:
                search_results = metadata['search_results']
                st.sidebar.write(f"✅ Found {len(search_results)} search results")
                
                # Replace citations with basic content from search results
                # enhanced_response = replace_citations_with_content(enhanced_response, search_results)
                
                # Convert direct links to embedded content
                enhanced_response = convert_direct_links_to_embedded(enhanced_response)
            else:
                st.sidebar.write("❌ No search results found")
                enhanced_response += "\n\n**🔍 No search results found**\n"
                enhanced_response += "This might be due to the query type or API configuration."
                
                # Convert direct links to embedded content
                enhanced_response = convert_direct_links_to_embedded(enhanced_response)
            
            # Display final enhanced response with embedded content
            message_placeholder.markdown(enhanced_response, unsafe_allow_html=True)
            
            # Add CSS styling for embedded content
            st.markdown("""
            <style>
            .stMarkdown iframe {
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                margin: 10px 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Add enhanced response to chat history
            st.session_state.messages.append({"role": "assistant", "content": enhanced_response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}"})