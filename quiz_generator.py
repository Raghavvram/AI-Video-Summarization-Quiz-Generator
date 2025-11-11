import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_quiz_prompt(transcript, num_questions=5, difficulty="medium", question_type="mcq"):
    """Create a prompt for quiz generation."""

    question_type_instructions = {
        "mcq": "multiple-choice questions with 4 options each (A, B, C, D). Mark the correct answer.",
        "true_false": "true/false questions with explanations.",
        "short_answer": "short answer questions that test understanding.",
        "mixed": "a mix of multiple-choice, true/false, and short answer questions."
    }

    difficulty_instructions = {
        "easy": "basic recall and understanding",
        "medium": "application and analysis",
        "hard": "synthesis and evaluation"
    }

    prompt = f"""You are an expert teacher creating educational assessments.

Based on the following transcript, create {num_questions} {question_type_instructions.get(question_type, question_type_instructions['mcq'])} 
at a {difficulty} difficulty level focusing on {difficulty_instructions.get(difficulty, difficulty_instructions['medium'])}.

Transcript:
"""{transcript}"""

Format your response as valid JSON with the following structure:
{{
    "quiz_title": "Quiz Title Based on Content",
    "questions": [
        {{
            "question_number": 1,
            "question_text": "Question text here?",
            "question_type": "mcq",
            "options": {{
                "A": "Option A text",
                "B": "Option B text",
                "C": "Option C text",
                "D": "Option D text"
            }},
            "correct_answer": "A",
            "explanation": "Brief explanation of why this is correct"
        }}
    ]
}}

Ensure questions are:
- Directly relevant to the transcript content
- Clear and unambiguous
- At the appropriate difficulty level
- Engaging and educational

Return ONLY the JSON object, no additional text."""

    return prompt

def generate_quiz(transcript, num_questions=5, difficulty="medium", question_type="mcq"):
    """Generate quiz questions from transcript using GPT-4."""
    try:
        prompt = create_quiz_prompt(transcript, num_questions, difficulty, question_type)

        # Truncate transcript if too long
        max_chars = 10000
        if len(prompt) > max_chars:
            transcript_truncated = transcript[:max_chars-2000]
            prompt = create_quiz_prompt(transcript_truncated, num_questions, difficulty, question_type)
            print(f"Warning: Transcript truncated to fit context window")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert educator creating high-quality assessment questions. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        quiz_json_str = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if quiz_json_str.startswith("```json"):
            quiz_json_str = quiz_json_str[7:]
        if quiz_json_str.startswith("```"):
            quiz_json_str = quiz_json_str[3:]
        if quiz_json_str.endswith("```"):
            quiz_json_str = quiz_json_str[:-3]

        quiz_data = json.loads(quiz_json_str.strip())
        return quiz_data

    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing quiz JSON: {str(e)}. Response: {quiz_json_str}")
    except Exception as e:
        raise Exception(f"Error generating quiz: {str(e)}")

def save_quiz(quiz_data, filename="quiz_output.json"):
    """Save quiz to JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        print(f"Quiz saved to {filename}")
        return filename
    except Exception as e:
        raise Exception(f"Error saving quiz: {str(e)}")

if __name__ == "__main__":
    # Test quiz generation
    sample_transcript = """
    Python is a high-level programming language known for its simplicity and readability.
    It supports multiple programming paradigms including procedural, object-oriented, and functional programming.
    Python is widely used in web development, data science, artificial intelligence, and automation.
    The language uses indentation for code blocks instead of curly braces.
    """

    print("Generating quiz...")
    quiz = generate_quiz(sample_transcript, num_questions=3, difficulty="easy")
    print(json.dumps(quiz, indent=2))
