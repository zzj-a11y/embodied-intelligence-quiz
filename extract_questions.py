"""Extract 400 questions from pdf_full_text.txt into structured JSON."""
import re
import json
from collections import Counter

with open('pdf_full_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print(f'Original text length: {len(text)} chars')

# --- Step 1: Clean noise ---
# Replace complete page-header blocks with a single newline
text = re.sub(
    r'--- Page \d+ ---\n·广州市风扬信息科技有限公司\n\d+具身智能--多传感器融合应用赛\n',
    '\n', text
)
# Clean any stray remaining header elements
text = re.sub(r'--- Page \d+ ---\n?', '', text)
text = re.sub(r'·广州市风扬信息科技有限公司\n?', '', text)
text = re.sub(r'\d+具身智能--多传感器融合应用赛\n?', '', text)

# Remove everything before the first question
m = re.search(r'\n?(\d+\.)', text)
if m:
    idx = m.start(1)
    text = text[idx:]

# Remove trailing footer
text = re.sub(r'本题库仅供参考，如有疑问，请以权威资料为准。[\s\S]*$', '', text)

print(f'Cleaned text length: {len(text)} chars')

# --- Step 2: Split into blocks by question number ---
# Each block should start with "N. question text..."
blocks = re.split(r'\n(?=\d+\.)', text)
print(f'Number of blocks: {len(blocks)}')

# --- Step 3: Parse each block ---
questions = []

# Regex for parsing a single question block
block_pattern = re.compile(
    r'(\d+)\.\s*'              # question id
    r'(.+?)'                   # question text (lazy)
    r'\nA\.(.+?)\n'            # option A
    r'B\.(.+?)\n'              # option B
    r'C\.(.+?)\n'              # option C
    r'D\.(.+?)\n'              # option D
    r'.*?答案：\s*([A-D])\s*\n'  # answer
    r'.*?解析：(.+)',           # explanation (rest of block)
    re.DOTALL
)

failed = []
for block in blocks:
    block = block.strip()
    if not block:
        continue

    match = block_pattern.match(block)
    if not match:
        # Try alternate parsing for edge cases
        failed.append(block[:80])
        continue

    qid = int(match.group(1))
    qtext = match.group(2).strip()
    # Collapse internal newlines in question text
    qtext = re.sub(r'\s+', ' ', qtext).strip()

    opts = {
        'A': re.sub(r'\s+', ' ', match.group(3).strip()),
        'B': re.sub(r'\s+', ' ', match.group(4).strip()),
        'C': re.sub(r'\s+', ' ', match.group(5).strip()),
        'D': re.sub(r'\s+', ' ', match.group(6).strip()),
    }

    answer = match.group(7)

    explanation = match.group(8).strip()
    # Collapse whitespace in explanation
    explanation = re.sub(r'\s+', ' ', explanation)

    # Determine category by question id
    if 1 <= qid <= 100:
        category = 'Python基础'
    elif 101 <= qid <= 200:
        category = '机器学习'
    elif 201 <= qid <= 300:
        category = '深度学习'
    else:
        category = '计算机视觉'

    questions.append({
        'id': qid,
        'category': category,
        'question': qtext,
        'options': opts,
        'answer': answer,
        'explanation': explanation
    })

print(f'Extracted {len(questions)} questions')
if failed:
    print(f'Failed to parse {len(failed)} blocks:')
    for f in failed[:10]:
        print(f'  {f}...')

# --- Step 4: Verify ---
assert len(questions) == 400, f'Expected 400, got {len(questions)}'

# Check ID sequence is contiguous 1-400
ids = [q['id'] for q in questions]
assert ids == list(range(1, 401)), f'IDs not contiguous 1-400.'

# Check categories
cats = Counter(q['category'] for q in questions)
print(f'Categories: {dict(cats)}')
assert cats['Python基础'] == 100, f'Python基础: {cats["Python基础"]}'
assert cats['机器学习'] == 100, f'机器学习: {cats["机器学习"]}'
assert cats['深度学习'] == 100, f'深度学习: {cats["深度学习"]}'
assert cats['计算机视觉'] == 100, f'计算机视觉: {cats["计算机视觉"]}'

# Verify all required fields present and valid
for q in questions:
    assert all(k in q for k in ['id', 'category', 'question', 'options', 'answer', 'explanation'])
    assert set(q['options'].keys()) == {'A', 'B', 'C', 'D'}, f'Q{q["id"]}: bad options keys'
    assert q['answer'] in 'ABCD', f'Q{q["id"]}: bad answer {q["answer"]}'
    assert len(q['question']) > 0, f'Q{q["id"]}: empty question'
    assert len(q['explanation']) > 0, f'Q{q["id"]}: empty explanation'
    # Check options are not empty
    for k in 'ABCD':
        assert len(q['options'][k]) > 0, f'Q{q["id"]}: empty option {k}'

print('All validations passed!')

# --- Step 5: Save ---
with open('questions_structured.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print('Saved to questions_structured.json')

# --- Step 6: Print samples ---
print('\n--- Sample questions ---')
for q in questions[:3]:
    print(f"\n#{q['id']} [{q['category']}]")
    print(f"  Q: {q['question']}")
    print(f"  A: {q['options']['A']}")
    print(f"  B: {q['options']['B']}")
    print(f"  C: {q['options']['C']}")
    print(f"  D: {q['options']['D']}")
    print(f"  Answer: {q['answer']}")
    print(f"  Explanation: {q['explanation'][:120]}...")
