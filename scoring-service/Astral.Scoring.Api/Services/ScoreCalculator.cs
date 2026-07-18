using Astral.Scoring.Api.Models;

namespace Astral.Scoring.Api.Services;

public class ScoreCalculator
{
    public int CalculateDiameterFactor(decimal averageDiameterKm)
    {
        if (averageDiameterKm < 0.03m)
        {
            return 2;
        }

        if (averageDiameterKm < 0.065m)
        {
            return 8;
        }

        if (averageDiameterKm < 0.20m)
        {
            return 15;
        }

        if (averageDiameterKm < 0.60m)
        {
            return 21;
        }

        return 25;
    }

    public int CalculateDistanceFactor(decimal missDistanceKm)
    {
        if (missDistanceKm < 1_000_000m)
        {
            return 25;
        }

        if (missDistanceKm < 20_000_000m)
        {
            return 21;
        }

        if (missDistanceKm < 37_000_000m)
        {
            return 15;
        }

        if (missDistanceKm <= 57_000_000m)
        {
            return 8;
        }

        return 2;
    }

    public int CalculateVelocityFactor(decimal relativeVelocityKps)
    {
        if (relativeVelocityKps < 8m)
        {
            return 2;
        }

        if (relativeVelocityKps < 13m)
        {
            return 6;
        }

        if (relativeVelocityKps < 18m)
        {
            return 12;
        }

        if (relativeVelocityKps < 27m)
        {
            return 16;
        }

        return 20;
    }

    public int CalculateTimingFactor(
        DateOnly closeApproachDate,
        DateOnly currentDate
    )
    {
        var daysUntilApproach =
            closeApproachDate.DayNumber - currentDate.DayNumber;

        if (daysUntilApproach < 0)
        {
            return 0;
        }

        if (daysUntilApproach < 7)
        {
            return 15;
        }

        if (daysUntilApproach < 30)
        {
            return 12;
        }

        if (daysUntilApproach < 90)
        {
            return 9;
        }

        if (daysUntilApproach <= 365)
        {
            return 5;
        }

        return 1;
    }

    public int CalculateHazardFlagFactor(bool isPotentiallyHazardous)
    {
        return isPotentiallyHazardous ? 15 : 0;
    }

    public string DetermineCategory(int score)
    {
        if (score < 25)
        {
            return "Low Interest";
        }

        if (score < 50)
        {
            return "Moderate Interest";
        }

        if (score < 75)
        {
            return "High Interest";
        }

        return "Critical Review";
    }

    public ScoreResponse Calculate(
        ScoreRequest request,
        DateOnly currentDate
    )
    {
        var averageDiameterKm =
            (
                request.EstimatedDiameterMinKm!.Value +
                request.EstimatedDiameterMaxKm!.Value
            ) / 2m;

        var factors = new ScoreFactors(
            Diameter: CalculateDiameterFactor(averageDiameterKm),
            Distance: CalculateDistanceFactor(request.MissDistanceKm!.Value),
            Velocity: CalculateVelocityFactor(
                request.RelativeVelocityKps!.Value
            ),
            Timing: CalculateTimingFactor(
                request.CloseApproachDate!.Value,
                currentDate
            ),
            HazardFlag: CalculateHazardFlagFactor(
                request.IsPotentiallyHazardous!.Value
            )
        );

        var score =
            factors.Diameter +
            factors.Distance +
            factors.Velocity +
            factors.Timing +
            factors.HazardFlag;

        var category = DetermineCategory(score);

        return new ScoreResponse(
            Score: score,
            Category: category,
            ModelVersion: "APS-v1",
            Factors: factors,
            Explanation:
                $"{category} based on the APS-v1 size, distance, velocity, timing, and NASA hazardous-classification factors."
        );
    }
}