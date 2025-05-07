from rouge_score import rouge_scorer

# Read reference and hypothesis from files
with open("test_instruction_result.txt", "r", encoding="utf-8") as ref_file:
    reference = ref_file.read().strip()

with open("generated_by_LLM.txt", "r", encoding="utf-8") as hyp_file:
    hypothesis = hyp_file.read().strip()

# Initialize scorer and compute ROUGE-1
scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
score = scorer.score(reference, hypothesis)

# Print the result
print("ROUGE-1 Score:")
print(score['rouge1'])
