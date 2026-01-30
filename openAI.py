import random
import csv
import os
from openai import OpenAI

# === STEP 1: Setup OpenAI API ===


# === STEP 2: Model Toggle ===
SELECTED_MODEL = "gpt-3.5-turbo"  # Change to "gpt-3.5-turbo" or "gpt-4" if needed

# === STEP 3: Prompt Templates & Placeholder Values ===
prompts = [
    "[IPL] 2025 kicked off with [specific update]—who’s your team?",
    "[Virat Kohli] scored [specific stat] in [match highlights]—impressed?",
    "[T20] saw [specific moment] this week—did you see it?",
    "[Sports news] reports [Indian cricket team] prepping for [event]—what’s your prediction?",
    "[Kabaddi] league announced [specific update]—do you follow it?",
    "[Football India] fans are buzzing after [specific update]—what’s your take?"
]

placeholder_values = {
    "specific update": [
        "a nail-biting Super Over", 
        "a record-breaking auction", 
        "a surprising team comeback",
        "a shocking trade deal", 
        "a last-second win", 
        "a major rule change"
    ],
    "specific stat": [
        "103 runs off 55 balls", 
        "his fastest century ever", 
        "a double hat-trick",
        "12 successful raids", 
        "3 super tackles", 
        "2 yellow cards in the final half"
    ],
    "match highlights": [
        "yesterday’s thriller between MI and CSK", 
        "last weekend's match", 
        "the recent El Clasico of IPL",
        "a PKL faceoff between Jaipur Pink Panthers and Patna Pirates",
        "a football derby between Kerala Blasters and Bengaluru FC"
    ],
    "specific moment": [
        "a last-ball six by Dhoni", 
        "a stunning hat-trick", 
        "a controversial run-out decision",
        "a last-minute penalty goal", 
        "a super raid that turned the game", 
        "a red card that changed momentum"
    ],
    "event": [
        "the 2025 World Cup", 
        "the Asia Cup", 
        "the historic England Test series",
        "the Kabaddi Nationals", 
        "the ISL Finals", 
        "the upcoming FIFA qualifiers"
    ]
}


# === STEP 4: Fill in placeholders ===
def fill_prompt(prompt):
    for placeholder, options in placeholder_values.items():
        prompt = prompt.replace(f"[{placeholder}]", random.choice(options))
    return prompt

selected_prompt = fill_prompt(random.choice(prompts))

# === STEP 5: Detect Community and Keywords ===
if "Kabaddi" in selected_prompt:
    keywords = ["Kabaddi", "Pro Kabaddi", "raiders", "defenders", "PKL"]
    community = "Kabaddi"
    instruction = "You are a Kabaddi sports news writer. Write only about Kabaddi-related topics. Avoid Cricket or Football."
elif "Football" in selected_prompt:
    keywords = ["football India", "ISL", "Sunil Chhetri", "Indian football team", "goalkeeper", "striker"]
    community = "Football"
    instruction = "You are a Football news writer. Keep the content focused on Indian football. Do not mention Cricket or Kabaddi."
else:
    keywords = ["Cricket", "IPL", "T20", "Indian cricket team", "Virat Kohli", "match highlights", "sports news", "M.S. Dhoni", "batsman", "bowler"]
    community = "Cricket"
    instruction = "You are a Cricket news writer. Stick to Cricket-related news. Avoid Football or Kabaddi references."

# === STEP 6: Final Prompt Assembly ===
final_prompt = f"""
{instruction}

Template: "{selected_prompt}"

Use these keywords naturally: {', '.join(keywords)}.
Tone should be conversational and engaging. Length: 500–600 words.
"""

# === STEP 7: OpenAI Request (New SDK Format) ===
response = client.chat.completions.create(
    model=SELECTED_MODEL,
    messages=[
        {"role": "system", "content": "You are a content generator for Indian sports posts."},
        {"role": "user", "content": final_prompt}
    ],
    temperature=0.7,
    max_tokens=1000
)

# === STEP 8: Extract Generated Text ===
text = response.choices[0].message.content.strip()

# === STEP 9: Token Estimates ===
input_tokens = len(final_prompt.split())
output_tokens = len(text.split())
total_tokens = input_tokens + output_tokens

# === STEP 10: Save to CSV ===
csv_file = "openai.csv"
header = ["Model", "Community", "Input prompt", "Response", "Input tokens", "Output tokens", "Total Token"]

write_header = not os.path.exists(csv_file)

with open(csv_file, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if write_header:
        writer.writerow(header)
    writer.writerow([SELECTED_MODEL, community, final_prompt.strip(), text, input_tokens, output_tokens, total_tokens])

print(f"✅ CSV updated using model: {SELECTED_MODEL}")
print("📝 Generated post:\n")
print(text)
