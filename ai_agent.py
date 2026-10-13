import os
import feedparser
from google import genai

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Fetch Latest Science News from Google News RSS Feed
def get_science_news():
    rss_url = "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    headlines = []
    for entry in feed.entries[:5]: 
        headlines.append({"title": entry.title, "link": entry.link})
    return headlines

# Generate Sanolines Posts
def generate_daily_posts():
    news_items = get_science_news()
    print(f"Fetched {len(news_items)} fresh science headlines...\n")
    
    prompt = f"""
    You are the social media manager for 'Sanolines' (a science & knowledge channel).
    Based on these 5 latest Google News headlines: {news_items}
    
    For EACH headline, create a distinct post matching this exact style:
    1. Caption: 1 intriguing sentence summarizing the story with hashtags.
    2. Image Title Text: 3-4 bold words in ALL CAPS (e.g. "EARTH'S TIME PROBLEM").
    3. Image Subtitle: 3-5 explanatory words (e.g. "Leap Seconds May Change").
    4. Image Visual Concept: Detailed cinematic graphic prompt for Gemini Imagen.
    
    Make sure all 5 posts are completely unique and different from each other.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    return response.text

if __name__ == "__main__":
    content = generate_daily_posts()
    print("=== DAILY AUTOMATED SANOLINES CONTENT ===")
    print(content)
    
    with open("today_posts.txt", "w", encoding="utf-8") as f:
        f.write(content)
