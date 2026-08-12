using System.ComponentModel.DataAnnotations;

using Astral.Scoring.Api.Models;

namespace Astral.Scoring.Tests;

public class ScoreRequestValidationTests
{
    [Fact]
    public void ValidRequestHasNoValidationErrors()
    {
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0.04m,
            EstimatedDiameterMaxKm = 0.06m,
            MissDistanceKm = 1_000_000m,
            RelativeVelocityKps = 13m,
            IsPotentiallyHazardous = false,
            CloseApproachDate = new DateOnly(2026, 7, 1),
        };

        var results = Validate(request);

        Assert.Empty(results);
    }

    [Fact]
    public void MinimumDiameterGreaterThanMaximumHasValidationError()
    {
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0.08m,
            EstimatedDiameterMaxKm = 0.06m,
            MissDistanceKm = 1_000_000m,
            RelativeVelocityKps = 13m,
            IsPotentiallyHazardous = false,
            CloseApproachDate = new DateOnly(2026, 7, 1),
        };

        var results = Validate(request);

        var error = Assert.Single(results);

        Assert.Equal(
            "Estimated minimum diameter cannot exceed estimated maximum diameter.",
            error.ErrorMessage
        );
    }

    [Fact]
    public void EmptyRequestHasErrorsForAllRequiredFields()
    {
        var request = new ScoreRequest();

        var results = Validate(request);

        Assert.Equal(6, results.Count);
    }

    [Fact]
    public void ZeroMinimumDiameterHasValidationError()
    {
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0m,
            EstimatedDiameterMaxKm = 0.06m,
            MissDistanceKm = 1_000_000m,
            RelativeVelocityKps = 13m,
            IsPotentiallyHazardous = false,
            CloseApproachDate = new DateOnly(2026, 7, 1),
        };

        var results = Validate(request);

        var error = Assert.Single(results);

        Assert.Contains(
            nameof(ScoreRequest.EstimatedDiameterMinKm),
            error.MemberNames
        );
    }

    [Fact]
    public void ZeroRelativeVelocityHasValidationError()
    {
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0.03m,
            EstimatedDiameterMaxKm = 0.06m,
            MissDistanceKm = 1_000_000m,
            RelativeVelocityKps = 0m,
            IsPotentiallyHazardous = false,
            CloseApproachDate = new DateOnly(2026, 7, 1),
        };

        var results = Validate(request);

        var error = Assert.Single(results);

        Assert.Contains(
            nameof(ScoreRequest.RelativeVelocityKps),
            error.MemberNames
        );
    }

    [Fact]
    public void NegativeMissDistanceHasValidationError()
    {
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0.03m,
            EstimatedDiameterMaxKm = 0.06m,
            MissDistanceKm = -1m,
            RelativeVelocityKps = 13m,
            IsPotentiallyHazardous = false,
            CloseApproachDate = new DateOnly(2026, 7, 1),
        };

        var results = Validate(request);

        var error = Assert.Single(results);

        Assert.Contains(
            nameof(ScoreRequest.MissDistanceKm),
            error.MemberNames
        );
    }

    [Fact]
    public void BoundaryValuesHaveNoValidationErrors()
    {
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0.000001m,
            EstimatedDiameterMaxKm = 0.000001m,
            MissDistanceKm = 0m,
            RelativeVelocityKps = 0.000001m,
            IsPotentiallyHazardous = true,
            CloseApproachDate = new DateOnly(2026, 7, 1),
        };

        var results = Validate(request);

        Assert.Empty(results);
    }

    private static List<ValidationResult> Validate(ScoreRequest request)
    {
        var results = new List<ValidationResult>();

        Validator.TryValidateObject(
            request,
            new ValidationContext(request),
            results,
            validateAllProperties: true
        );

        return results;
    }
}