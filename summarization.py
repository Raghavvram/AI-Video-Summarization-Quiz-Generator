import os
from openai import OpenAI
from langchain.prompts import PromptTemplate

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_summary_prompt(transcript, length="medium"):
    """Create a prompt for summarization based on desired length."""
    length_instructions = {
        "short": "3-5 concise bullet points",
        "medium": "a comprehensive paragraph of 150-200 words",
        "long": "a detailed summary with multiple paragraphs (300-400 words)"
    }

    prompt = f"""You are an expert at summarizing educational video content. 

Your task is to analyze the following video transcript and create {length_instructions.get(length, length_instructions['medium'])}.

Focus on:
- Main topics and key concepts
- Important explanations or definitions
- Critical insights or conclusions
- Any actionable information

Transcript:
"""{transcript}"""

Provide a clear, well-structured summary that captures the essence of the video content."""

    return prompt

def summarize_transcript(transcript, length="medium"):
    """Summarize transcript using GPT-4."""
    try:
        prompt = create_summary_prompt(transcript, length)

        # Truncate if transcript is too long (GPT-4 context limit)
        max_chars = 12000
        if len(prompt) > max_chars:
            transcript_truncated = transcript[:max_chars-1000]
            prompt = create_summary_prompt(transcript_truncated, length)
            print(f"Warning: Transcript truncated to {max_chars} characters")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert educational content summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")

def extract_key_concepts(transcript, num_concepts=5):
    """Extract key concepts from the transcript."""
    try:
        prompt = f"""Extract the {num_concepts} most important concepts or topics from this transcript. 
        List them as a numbered list.

        Transcript: {transcript[:8000]}

        Key Concepts:"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Error extracting key concepts: {str(e)}")

if __name__ == "__main__":
    # Test summarization
    sample_transcript = """
    Artificial intelligence has revolutionized many industries. Machine learning, a subset of AI,
    enables computers to learn from data without explicit programming. Deep learning uses neural
    networks to process complex patterns. These technologies are used in applications like image
    recognition, natural language processing, and autonomous vehicles.
    """

    print("Testing summarization...")
    summary = summarize_transcript(sample_transcript, length="short")
    print(f"Summary:\n{summary}")
