namespace Astral.Scoring.Api.Models;

public record ScoreFactors(
    int Diameter,
    int Distance,
    int Velocity,
    int Timing,
    int HazardFlag
);