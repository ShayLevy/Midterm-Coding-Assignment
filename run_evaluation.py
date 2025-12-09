"""
Evaluation Runner
Runs the complete test suite and evaluates system performance using LLM-as-a-judge

Uses Anthropic Claude as judge (requires ANTHROPIC_API_KEY in .env)
Uses OpenAI GPT-4 for generation (requires OPENAI_API_KEY in .env)
"""

import json
from pathlib import Path
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
# Ensures both OPENAI_API_KEY and ANTHROPIC_API_KEY are available
load_dotenv()

from main import InsuranceClaimSystem
from src.evaluation.judge import LLMJudge
from src.evaluation.test_queries import TestSuite

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EvaluationRunner:
    """
    Runs evaluation suite and generates reports
    """

    def __init__(self, system: InsuranceClaimSystem, output_dir: str = "./evaluation_results"):
        """
        Initialize evaluation runner

        Args:
            system: Initialized InsuranceClaimSystem
            output_dir: Directory to save results

        Note: Uses Anthropic Claude as judge (separate from OpenAI GPT-4 used for generation)
        """
        self.system = system
        # Use Claude as judge (default: claude-sonnet-4-20250514) - separate from GPT-4 used for generation
        self.judge = LLMJudge(temperature=0)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        logger.info("EvaluationRunner initialized with Claude judge (separate from GPT-4 generation)")

    def run_full_evaluation(self) -> dict:
        """
        Run complete evaluation on all test queries

        Returns:
            Dictionary with all results
        """
        logger.info("=" * 70)
        logger.info("STARTING FULL EVALUATION")
        logger.info("=" * 70)

        test_queries = TestSuite.get_test_queries()
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_queries": len(test_queries),
            "query_results": [],
            "aggregate_scores": {}
        }

        for i, test_case in enumerate(test_queries, 1):
            logger.info(f"\n{'=' * 70}")
            logger.info(f"Evaluating Query {i}/{len(test_queries)}: {test_case['id']}")
            logger.info(f"{'=' * 70}")

            result = self.evaluate_query(test_case)
            results["query_results"].append(result)

            # Print summary for this query
            self._print_query_summary(result)

        # Calculate aggregate scores
        results["aggregate_scores"] = self._calculate_aggregate_scores(results["query_results"])

        # Save results
        self._save_results(results)

        # Print final summary
        self._print_final_summary(results)

        return results

    def evaluate_query(self, test_case: dict) -> dict:
        """
        Evaluate a single test query

        Args:
            test_case: Test case dictionary

        Returns:
            Evaluation result
        """
        query = test_case["query"]
        query_id = test_case["id"]

        logger.info(f"Query: {query}")

        # Run query through system
        try:
            system_response = self.system.query(query, use_manager=True)
            answer = system_response.get("output", "")
            success = system_response.get("success", False)

            # Extract retrieved context (if available)
            retrieved_context = ""
            if system_response.get("intermediate_steps"):
                for step in system_response["intermediate_steps"]:
                    if len(step) >= 2:
                        retrieved_context += str(step[1]) + "\n\n"

            # Perform evaluation
            eval_result = self.judge.evaluate_full(
                query=query,
                answer=answer,
                ground_truth=test_case["ground_truth"],
                retrieved_context=retrieved_context if retrieved_context else answer,
                expected_chunks=test_case.get("expected_chunks", []),
                retrieved_chunks=[retrieved_context] if retrieved_context else []
            )

            return {
                "query_id": query_id,
                "query": query,
                "query_type": test_case["type"],
                "system_answer": answer,
                "ground_truth": test_case["ground_truth"],
                "system_success": success,
                "evaluation": eval_result,
                "correctness_score": eval_result["correctness"]["score"],
                "relevancy_score": eval_result["relevancy"]["score"],
                "recall_score": eval_result.get("recall", {}).get("score", "N/A"),
                "average_score": eval_result["average_score"]
            }

        except Exception as e:
            logger.error(f"Error evaluating query {query_id}: {e}")
            return {
                "query_id": query_id,
                "query": query,
                "error": str(e),
                "system_success": False
            }

    def _calculate_aggregate_scores(self, query_results: list) -> dict:
        """Calculate aggregate scores across all queries"""
        correctness_scores = []
        relevancy_scores = []
        recall_scores = []
        average_scores = []

        for result in query_results:
            if "correctness_score" in result:
                correctness_scores.append(result["correctness_score"])
                relevancy_scores.append(result["relevancy_score"])

                recall = result.get("recall_score")
                if recall != "N/A":
                    recall_scores.append(recall)

                average_scores.append(result["average_score"])

        return {
            "avg_correctness": sum(correctness_scores) / len(correctness_scores) if correctness_scores else 0,
            "avg_relevancy": sum(relevancy_scores) / len(relevancy_scores) if relevancy_scores else 0,
            "avg_recall": sum(recall_scores) / len(recall_scores) if recall_scores else 0,
            "overall_average": sum(average_scores) / len(average_scores) if average_scores else 0,
            "total_evaluated": len(query_results),
            "successful_queries": sum(1 for r in query_results if r.get("system_success"))
        }

    def _save_results(self, results: dict):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"evaluation_results_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"\n✅ Results saved to: {filename}")

    def _print_query_summary(self, result: dict):
        """Print summary for a single query"""
        print(f"\n{'─' * 70}")
        print(f"Query ID: {result['query_id']}")
        print(f"Type: {result.get('query_type', 'N/A')}")
        print(f"{'─' * 70}")
        print(f"Correctness: {result.get('correctness_score', 'N/A')}/5")
        print(f"Relevancy: {result.get('relevancy_score', 'N/A')}/5")
        print(f"Recall: {result.get('recall_score', 'N/A')}/5")
        print(f"Average: {result.get('average_score', 'N/A'):.2f}/5")

    def _print_final_summary(self, results: dict):
        """Print final evaluation summary"""
        agg = results["aggregate_scores"]

        print("\n" + "=" * 70)
        print("FINAL EVALUATION SUMMARY")
        print("=" * 70)
        print(f"\nTotal Queries Evaluated: {agg['total_evaluated']}")
        print(f"Successful Queries: {agg['successful_queries']}")
        print(f"\n{'─' * 70}")
        print("AVERAGE SCORES (out of 5)")
        print(f"{'─' * 70}")
        print(f"Correctness:      {agg['avg_correctness']:.2f}")
        print(f"Relevancy:        {agg['avg_relevancy']:.2f}")
        print(f"Recall:           {agg['avg_recall']:.2f}")
        print(f"{'─' * 70}")
        print(f"OVERALL AVERAGE:  {agg['overall_average']:.2f}/5.00")
        print("=" * 70)

        # Performance interpretation
        overall = agg['overall_average']
        if overall >= 4.5:
            grade = "A (Excellent)"
        elif overall >= 4.0:
            grade = "B (Very Good)"
        elif overall >= 3.0:
            grade = "C (Good)"
        elif overall >= 2.0:
            grade = "D (Fair)"
        else:
            grade = "F (Needs Improvement)"

        print(f"\nPerformance Grade: {grade}")
        print("=" * 70 + "\n")


def main():
    """Main evaluation entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         INSURANCE CLAIM SYSTEM - EVALUATION SUITE        ║
    ║              LLM-as-a-Judge Evaluation                    ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Initialize system
    logger.info("Initializing system...")
    system = InsuranceClaimSystem(
        data_dir="./data",
        chroma_dir="./chroma_db",
        rebuild_indexes=False
    )

    # Run evaluation
    runner = EvaluationRunner(system)
    results = runner.run_full_evaluation()

    print("\n✅ Evaluation complete! Check ./evaluation_results/ for detailed results.\n")


if __name__ == "__main__":
    main()
