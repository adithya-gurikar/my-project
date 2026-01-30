# import random
# import csv
# import google.generativeai as genai

# # STEP 1: API Setup
# genai.configure(api_key="")  # replace with your real key

# # STEP 2: Choose a supported model
# model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# # STEP 3: Your prompt templates & placeholders
# prompts = [
#     "[IPL] 2025 kicked off with [specific update]—who’s your team?",
#     "[Virat Kohli] scored [specific stat] in [match highlights]—impressed?",
#     "[T20] saw [specific moment] this week—did you see it?",
#     "[Sports news] reports [Indian cricket team] prepping for [event]—what’s your prediction?",
#     "[Kabaddi] league announced [specific update]—do you follow it?"
# ]

# keywords = [
#     "Cricket", "IPL", "T20", "Indian cricket team", "Virat Kohli",
#     "match highlights", "sports news", "football India", "kabaddi"
# ]

# placeholder_values = {
#     "specific update": ["a nail-biting Super Over", "a record-breaking auction", "a surprising team comeback"],
#     "specific stat": ["103 runs off 55 balls", "his fastest century ever", "a double hat-trick"],
#     "match highlights": ["yesterday’s thriller between MI and CSK", "last weekend's match", "the recent El Clasico of IPL"],
#     "specific moment": ["a last-ball six by Dhoni", "a stunning hat-trick", "a controversial run-out decision"],
#     "event": ["the 2025 World Cup", "the Asia Cup", "the historic England Test series"]
# }

# def fill_prompt(prompt):
#     for placeholder, options in placeholder_values.items():
#         prompt = prompt.replace(f"[{placeholder}]", random.choice(options))
#     return prompt

# selected_prompt = fill_prompt(random.choice(prompts))

# final_prompt = f"""
# You are an Indian sports news writer. Create a short, fun, clickbaiting and relevant post using the following template:

# "{selected_prompt}"

# Use these keywords naturally: {', '.join(keywords)}.
# Tone should be conversational and engaging. Length: 500-600 words.
# """

# # STEP 4: Generate response
# response = model.generate_content([final_prompt])
# text = response.text.strip()

# # Estimate token counts (since metadata may be limited)
# input_tokens = len(final_prompt.split())
# output_tokens = len(text.split())
# total_tokens = input_tokens + output_tokens

# # STEP 5: Save to CSV
# csv_file = "generated_posts.csv"
# header = ["Input prompt", "Response", "Input tokens", "Output tokens", "Total Token"]

# write_header = False
# try:
#     with open(csv_file, 'r') as f:
#         pass
# except FileNotFoundError:
#     write_header = True

# with open(csv_file, 'a', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     if write_header:
#         writer.writerow(header)
#     writer.writerow([final_prompt.strip(), text, input_tokens, output_tokens, total_tokens])

# print("✅ CSV file updated! Generated post:\n")
# print(text)



import random
import csv
import google.generativeai as genai

# STEP 1: API Setup```` # replace with your actual key

# STEP 2: Choose a supported model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# STEP 3: Prompt templates & placeholder values
prompts = [
    "[IPL] 2025 kicked off with [specific update]—who’s your team?",
    "[Virat Kohli] scored [specific stat] in [match highlights]—impressed?",
    "[T20] saw [specific moment] this week—did you see it?",
    "[Sports news] reports [Indian cricket team] prepping for [event]—what’s your prediction?",
    "[Kabaddi] league announced [specific update]—do you follow it?",
    "[Football India] fans are buzzing after [specific update]—what’s your take?"
]

placeholder_values = {
    "specific update": ["a nail-biting Super Over", "a record-breaking auction", "a surprising team comeback"],
    "specific stat": ["103 runs off 55 balls", "his fastest century ever", "a double hat-trick"],
    "match highlights": ["yesterday’s thriller between MI and CSK", "last weekend's match", "the recent El Clasico of IPL"],
    "specific moment": ["a last-ball six by Dhoni", "a stunning hat-trick", "a controversial run-out decision"],
    "event": ["the 2025 World Cup", "the Asia Cup", "the historic England Test series"]
}

# STEP 4: Fill in a random prompt with dynamic data``
def fill_prompt(prompt):
    for placeholder, options in placeholder_values.items():
        prompt = prompt.replace(f"[{placeholder}]", random.choice(options))
    return prompt

selected_prompt = fill_prompt(random.choice(prompts))

# STEP 5: Detect context and build prompt accordingly
if "Kabaddi" in selected_prompt:
    keywords = ["Kabaddi", "Pro Kabaddi", "raiders", "defenders", "PKL"]
    community = "Kabaddi"
    instruction = f"You are a Kabaddi sports news writer. Write only about Kabaddi-related topics. Avoid Cricket or Football."
elif "Football" in selected_prompt:
    keywords = ["football India", "ISL", "Sunil Chhetri", "Indian football team", "goalkeeper", "striker"]
    community = "Football"
    instruction = f"You are a Football news writer. Keep the content focused on Indian football. Do not mention Cricket or Kabaddi."
else:  # Default to Cricket
    keywords = ["Cricket", "IPL", "T20", "Indian cricket team", "Virat Kohli", "match highlights", "sports news", "M.S. Dhoni", "batsman", "bowler"]
    community = "Cricket"
    instruction = f"You are a Cricket news writer. Stick to Cricket-related news. Avoid Football or Kabaddi references."

# STEP 6: Final prompt
final_prompt = f"""
{instruction}

Template: "{selected_prompt}"

Use these keywords naturally: {', '.join(keywords)}.
Tone should be conversational and engaging. Length: 500–600 words.
"""

# STEP 7: Generate response
response = model.generate_content([final_prompt])
text = response.text.strip()

# STEP 8: Estimate token counts
input_tokens = len(final_prompt.split())
output_tokens = len(text.split())
total_tokens = input_tokens + output_tokens

# STEP 9: Save to CSV
csv_file = "gemini.csv"
header = ["Input prompt", "Response", "Input tokens", "Output tokens", "Total Token"]

write_header = False
try:
    with open(csv_file, 'r') as f:
        pass
except FileNotFoundError:
    write_header = True

with open(csv_file, 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if write_header:
        writer.writerow(header)
    writer.writerow([final_prompt.strip(), text, input_tokens, output_tokens, total_tokens])

print("✅ CSV file updated! Generated post:\n")
print(text)
