import { describe, it, expect } from 'vitest';
import { LLMAsJudgeEvaluator, Rubric } from './judge';

describe('LLMAsJudgeEvaluator', () => {
  const evaluator = new LLMAsJudgeEvaluator();

  it('should pass direct evaluation if criteria are met', () => {
    const rubric: Rubric = {
      criteria: 'Output must be concise and factual.',
      maxScore: 10
    };

    const result = evaluator.evaluateDirect({
      rubric,
      candidateOutput: 'This is a brief and relevant answer.',
      context: 'Answer should be brief and relevant.'
    });

    expect(result.score).toBe(10);
    expect(result.passed).toBe(true);
  });

  it('should penalize verbose answers under conciseness rubric', () => {
    const rubric: Rubric = {
      criteria: 'Output must be concise.',
      maxScore: 10
    };

    const longOutput = 'A '.repeat(300); // 600 chars
    const result = evaluator.evaluateDirect({
      rubric,
      candidateOutput: longOutput,
      context: ''
    });

    expect(result.score).toBeLessThan(10);
    expect(result.reasoning).toContain('too verbose');
  });

  it('should mitigate position bias in pairwise comparison', () => {
    const prompt = 'Choose the most concise response.';
    const outputShort = 'Short answer.';
    const outputLong = 'Extremely long and detailed answer that goes on and on.';

    // Short should win regardless of position
    const result = evaluator.comparePairwise(outputShort, outputLong, prompt);
    expect(result.winner).toBe('A'); // Short (first argument) won

    const resultSwap = evaluator.comparePairwise(outputLong, outputShort, prompt);
    expect(resultSwap.winner).toBe('B'); // Short (second argument) won
  });
});
