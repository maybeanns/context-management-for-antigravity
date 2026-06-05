export interface Rubric {
  criteria: string;
  maxScore: number;
}

export interface EvaluationResult {
  score: number;
  reasoning: string;
  passed: boolean;
}

export interface JudgePrompt {
  rubric: Rubric;
  candidateOutput: string;
  context: string;
}

export class LLMAsJudgeEvaluator {
  /**
   * Evaluates a candidate output against a rubric.
   */
  evaluateDirect(prompt: JudgePrompt): EvaluationResult {
    const { rubric, candidateOutput, context } = prompt;
    
    // Simulating LLM-as-a-Judge reasoning
    const cleanOutput = candidateOutput.toLowerCase();
    const cleanContext = context.toLowerCase();
    
    let score = rubric.maxScore;
    let reasons: string[] = [];

    // Simple heuristic-based evaluation logic mimicking model judgment
    const criteriaLower = rubric.criteria.toLowerCase();
    if (criteriaLower.includes("concise") && cleanOutput.length > 500) {
      score -= 2;
      reasons.push("Output is too verbose (exceeds 500 chars limit).");
    }
    
    if (criteriaLower.includes("factual") && cleanContext.length > 0) {
      // Check if candidate matches any context facts
      const contextWords = cleanContext.split(/\s+/);
      const outputWords = new Set(cleanOutput.split(/\s+/));
      const overlap = contextWords.filter(w => w.length > 4 && outputWords.has(w));
      if (overlap.length === 0) {
        score -= 3;
        reasons.push("Output contains no overlapping factual terms from the source context.");
      }
    }

    if (score < 0) score = 0;

    return {
      score,
      reasoning: reasons.length > 0 ? reasons.join(" ") : "Perfect score! Met all criteria.",
      passed: score >= rubric.maxScore * 0.7
    };
  }

  /**
   * Compares two outputs pairwise. Mitigates position bias by running comparison in both orders (A vs B, and B vs A).
   */
  comparePairwise(outputA: string, outputB: string, prompt: string): { winner: 'A' | 'B' | 'TIE'; confidence: number } {
    // Basic heuristics to determine winner
    // Order 1: A first, B second
    const score1 = this.mockCompare(outputA, outputB, prompt);
    // Order 2: B first, A second
    const score2 = this.mockCompare(outputB, outputA, prompt);

    // If both orders agree, return the agreed winner.
    // If they disagree (e.g., first option is always preferred), it's a position bias tie.
    if (score1 === 'A' && score2 === 'B') {
      return { winner: 'A', confidence: 0.9 };
    } else if (score1 === 'B' && score2 === 'A') {
      return { winner: 'B', confidence: 0.9 };
    } else {
      // Disagreement or tie
      return { winner: 'TIE', confidence: 0.5 };
    }
  }

  private mockCompare(first: string, second: string, prompt: string): 'A' | 'B' | 'TIE' {
    const fLen = first.length;
    const sLen = second.length;

    // Simple criteria: shorter length wins if prompt requests conciseness
    if (prompt.includes("concise")) {
      if (fLen < sLen - 20) return 'A'; // 'A' refers to first parameter
      if (sLen < fLen - 20) return 'B'; // 'B' refers to second parameter
    }
    return 'TIE';
  }
}
