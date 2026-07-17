namespace Astral.Scoring.Api.Models;

public record ScoreResponse(
    int Score,
    string Category,
    string ModelVersion,
    ScoreFactors Factors,
    string Explanation
);