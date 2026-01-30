import csv
import os
from openai import OpenAI

# === OpenAI setup ===
model = "gpt-4o"
num_prompts = 5

# === CLI input ===
community = input("🧠 Enter the community/keyword: ").strip()
extra_rules = input("🧾 Enter any extra instructions (optional): ").strip()
csv_file = f"generated_posts_{community.lower().replace(' ', '_')}.csv"

# === Prompt generation agent ===
base_instruction = f"""
You are a prompt engineer. Generate {num_prompts} unique, engaging prompt ideas for social media posts 
about the community or topic "{community}".
Each prompt should be relevant to the community/keyword provided, and formatted as a hook or question to drive engagement.
Avoid repetitions. Do not include explanations or hashtags. Output only a numbered list.
"""

if extra_rules:
    full_instruction = f"{base_instruction}\n\nFollow these additional rules: {extra_rules}"
else:
    full_instruction = base_instruction

print(f"\n🔁 Generating {num_prompts} prompts for '{community}' with rules: {extra_rules or 'None'}")

prompt_response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You generate engaging social media prompts for content creators."},
        {"role": "user", "content": full_instruction}
    ],
    temperature=0.5,
    max_tokens=400
)

# === Parse generated prompts ===
raw = prompt_response.choices[0].message.content.strip().split("\n")
prompts = [line.split(". ", 1)[1] if ". " in line else line for line in raw if line.strip()]

# === Content generation agent ===
results = []

for prompt in prompts:
    content_instruction = f"You are a social media content writer creating a post related to the topic '{community}'."
    if extra_rules:
        content_instruction += f" Follow these extra guidelines: {extra_rules}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": content_instruction},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    content = response.choices[0].message.content.strip()

    input_tokens = len(prompt.split())
    output_tokens = len(content.split())
    total_tokens = input_tokens + output_tokens

    results.append([community, prompt, content, extra_rules, input_tokens, output_tokens, total_tokens])

# === Save to CSV ===
header = ["Community", "Prompt", "Generated Content", "Extra Rules", "Input Tokens", "Output Tokens", "Total Tokens"]
write_header = not os.path.exists(csv_file)

with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(header)
    writer.writerows(results)

print(f"\n✅ All {num_prompts} posts generated and saved to '{csv_file}' 🎯")
