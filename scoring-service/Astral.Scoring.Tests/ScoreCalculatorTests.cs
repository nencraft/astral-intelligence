using Astral.Scoring.Api.Models;
using Astral.Scoring.Api.Services;

namespace Astral.Scoring.Tests;

public class ScoreCalculatorTests
{
    public static TheoryData<decimal, int> DiameterFactorCases => new()
    {
        { 0.01m, 2 },
        { 0.029999m, 2 },
        { 0.03m, 8 },
        { 0.064999m, 8 },
        { 0.065m, 15 },
        { 0.199999m, 15 },
        { 0.20m, 21 },
        { 0.599999m, 21 },
        { 0.60m, 25 },
    };

    public static TheoryData<decimal, int> DistanceFactorCases => new()
    {
        { 0m, 25 },
        { 999_999.999m, 25 },
        { 1_000_000m, 21 },
        { 19_999_999.999m, 21 },
        { 20_000_000m, 15 },
        { 36_999_999.999m, 15 },
        { 37_000_000m, 8 },
        { 57_000_000m, 8 },
        { 57_000_000.001m, 2 },
    };

    public static TheoryData<decimal, int> VelocityFactorCases => new()
    {
        { 0.000001m, 2 },
        { 7.999999m, 2 },
        { 8m, 6 },
        { 12.999999m, 6 },
        { 13m, 12 },
        { 17.999999m, 12 },
        { 18m, 16 },
        { 26.999999m, 16 },
        { 27m, 20 },
    };

    public static TheoryData<int, int> TimingFactorCases => new()
    {
        { -1, 0 },
        { 0, 15 },
        { 6, 15 },
        { 7, 12 },
        { 29, 12 },
        { 30, 9 },
        { 89, 9 },
        { 90, 5 },
        { 365, 5 },
        { 366, 1 },
    };

    public static TheoryData<int, string> CategoryCases => new()
    {
        { 0, "Low Interest" },
        { 24, "Low Interest" },
        { 25, "Moderate Interest" },
        { 49, "Moderate Interest" },
        { 50, "High Interest" },
        { 74, "High Interest" },
        { 75, "Critical Review" },
        { 100, "Critical Review" },
    };

    [Theory]
    [MemberData(nameof(DiameterFactorCases))]
    public void CalculateDiameterFactorReturnsExpectedPoints(
        decimal averageDiameterKm,
        int expectedPoints
    )
    {
        var calculator = new ScoreCalculator();

        var result = calculator.CalculateDiameterFactor(averageDiameterKm);

        Assert.Equal(expectedPoints, result);
    }

    [Theory]
    [MemberData(nameof(DistanceFactorCases))]
    public void CalculateDistanceFactorReturnsExpectedPoints(
        decimal missDistanceKm,
        int expectedPoints
    )
    {
        var calculator = new ScoreCalculator();

        var result = calculator.CalculateDistanceFactor(missDistanceKm);

        Assert.Equal(expectedPoints, result);
    }

    [Theory]
    [MemberData(nameof(VelocityFactorCases))]
    public void CalculateVelocityFactorReturnsExpectedPoints(
        decimal relativeVelocityKps,
        int expectedPoints
    )
    {
        var calculator = new ScoreCalculator();

        var result = calculator.CalculateVelocityFactor(relativeVelocityKps);

        Assert.Equal(expectedPoints, result);
    }

    [Theory]
    [MemberData(nameof(TimingFactorCases))]
    public void CalculateTimingFactorReturnsExpectedPoints(
        int daysUntilApproach,
        int expectedPoints
    )
    {
        var calculator = new ScoreCalculator();
        var currentDate = new DateOnly(2026, 7, 17);
        var closeApproachDate = currentDate.AddDays(daysUntilApproach);

        var result = calculator.CalculateTimingFactor(
            closeApproachDate,
            currentDate
        );

        Assert.Equal(expectedPoints, result);
    }

    [Fact]
    public void CalculateHazardFlagFactorReturnsZeroWhenFalse()
    {
        var calculator = new ScoreCalculator();

        var result = calculator.CalculateHazardFlagFactor(false);

        Assert.Equal(0, result);
    }

    [Fact]
    public void CalculateHazardFlagFactorReturnsFifteenWhenTrue()
    {
        var calculator = new ScoreCalculator();

        var result = calculator.CalculateHazardFlagFactor(true);

        Assert.Equal(15, result);
    }

    [Theory]
    [MemberData(nameof(CategoryCases))]
    public void DetermineCategoryReturnsExpectedCategory(
        int score,
        string expectedCategory
    )
    {
        var calculator = new ScoreCalculator();

        var result = calculator.DetermineCategory(score);

        Assert.Equal(expectedCategory, result);
    }

    [Fact]
    public void CalculateReturnsCompleteScoreResponse()
    {
        var calculator = new ScoreCalculator();
        var currentDate = new DateOnly(2026, 7, 17);
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0.20m,
            EstimatedDiameterMaxKm = 0.40m,
            MissDistanceKm = 10_000_000m,
            RelativeVelocityKps = 15m,
            IsPotentiallyHazardous = true,
            CloseApproachDate = currentDate.AddDays(20),
        };

        var result = calculator.Calculate(request, currentDate);

        Assert.Equal(81, result.Score);
        Assert.Equal("Critical Review", result.Category);
        Assert.Equal("APS-v1", result.ModelVersion);
        Assert.Equal(21, result.Factors.Diameter);
        Assert.Equal(21, result.Factors.Distance);
        Assert.Equal(12, result.Factors.Velocity);
        Assert.Equal(12, result.Factors.Timing);
        Assert.Equal(15, result.Factors.HazardFlag);
        Assert.NotEmpty(result.Explanation);
    }
}