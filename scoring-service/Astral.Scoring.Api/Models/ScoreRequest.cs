using System.ComponentModel.DataAnnotations;

namespace Astral.Scoring.Api.Models;

public class ScoreRequest : IValidatableObject
{
    [Required]
    [Range(0.000001, double.MaxValue)]
    public decimal? EstimatedDiameterMinKm { get; init; }

    [Required]
    [Range(0.000001, double.MaxValue)]
    public decimal? EstimatedDiameterMaxKm { get; init; }

    [Required]
    [Range(0, double.MaxValue)]
    public decimal? MissDistanceKm { get; init; }

    [Required]
    [Range(0.000001, double.MaxValue)]
    public decimal? RelativeVelocityKps { get; init; }

    [Required]
    public bool? IsPotentiallyHazardous { get; init; }

    [Required]
    public DateOnly? CloseApproachDate { get; init; }

    public IEnumerable<ValidationResult> Validate(
        ValidationContext validationContext
    )
    {
        if (
            EstimatedDiameterMaxKm.HasValue &&
            EstimatedDiameterMinKm.HasValue &&
            EstimatedDiameterMinKm.Value > EstimatedDiameterMaxKm.Value
        )
        {
            yield return new ValidationResult(
                "Estimated minimum diameter cannot exceed estimated maximum diameter.",
                new[]
                {
                    nameof(EstimatedDiameterMinKm),
                    nameof(EstimatedDiameterMaxKm),
                }
            );
        }
    }
}