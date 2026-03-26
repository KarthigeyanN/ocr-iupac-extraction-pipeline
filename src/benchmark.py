import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from .ocr_cleaning import clean_ocr_text
from .llm_correction import correct_text
from .iupac_extraction import extract_iupac
from .rdkit_validation import validate_structure


@dataclass
class BenchmarkSample:
    raw_ocr: str
    expected_name: Optional[str] = None


@dataclass
class BenchmarkResult:
    provider: str
    n_samples: int
    n_valid: int
    n_correct_name: int
    avg_latency_sec: float


def run_pipeline_on_sample(
    sample: BenchmarkSample,
    provider: str,
) -> Dict[str, Any]:
    t0 = time.time()

    cleaned = clean_ocr_text(sample.raw_ocr)
    corrected = correct_text(cleaned, provider=provider)
    name = extract_iupac(corrected)
    mol = validate_structure(name) if name else None

    latency = time.time() - t0

    is_valid = mol is not None
    is_correct = sample.expected_name is not None and name == sample.expected_name

    return {
        "latency": latency,
        "is_valid": is_valid,
        "is_correct": is_correct,
    }


def benchmark(
    samples: List[BenchmarkSample],
    providers: List[str],
) -> List[BenchmarkResult]:
    results: List[BenchmarkResult] = []

    for provider in providers:
        latencies = []
        n_valid = 0
        n_correct = 0

        for sample in samples:
            out = run_pipeline_on_sample(sample, provider)
            latencies.append(out["latency"])
            if out["is_valid"]:
                n_valid += 1
            if out["is_correct"]:
                n_correct += 1

        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

        results.append(
            BenchmarkResult(
                provider=provider,
                n_samples=len(samples),
                n_valid=n_valid,
                n_correct_name=n_correct,
                avg_latency_sec=avg_latency,
            )
        )

    return results


if __name__ == "__main__":
    # Tiny demo set
    demo_samples = [
        BenchmarkSample(raw_ocr="N,N-dimethy1tryptam1ne", expected_name="N,N-dimethyltryptamine"),
        BenchmarkSample(raw_ocr="benzene", expected_name="benzene"),
    ]

    providers = ["dummy"]  # extend later

    results = benchmark(demo_samples, providers)
    for r in results:
        print(
            f"Provider={r.provider} | n={r.n_samples} | "
            f"valid={r.n_valid} | correct={r.n_correct_name} | "
            f"avg_latency={r.avg_latency_sec:.4f}s"
        )
