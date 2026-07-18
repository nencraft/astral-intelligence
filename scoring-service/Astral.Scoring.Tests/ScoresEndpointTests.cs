using System.Net;
using System.Net.Http.Json;

using Astral.Scoring.Api.Models;

using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Testing;

namespace Astral.Scoring.Tests;

public class ScoresEndpointTests :
    IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ScoresEndpointTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task PostScoresReturnsCalculatedScore()
    {
        var currentDate = DateOnly.FromDateTime(DateTime.UtcNow);
        var request = new ScoreRequest
        {
            EstimatedDiameterMinKm = 0.20m,
            EstimatedDiameterMaxKm = 0.40m,
            MissDistanceKm = 10_000_000m,
            RelativeVelocityKps = 15m,
            IsPotentiallyHazardous = true,
            CloseApproachDate = currentDate.AddDays(20),
        };

        var response = await _client.PostAsJsonAsync(
            "/api/scores",
            request
        );

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var body =
            await response.Content.ReadFromJsonAsync<ScoreResponse>();

        Assert.NotNull(body);
        Assert.Equal(81, body.Score);
        Assert.Equal("Critical Review", body.Category);
        Assert.Equal("APS-v1", body.ModelVersion);
        Assert.Equal(21, body.Factors.Diameter);
        Assert.Equal(21, body.Factors.Distance);
        Assert.Equal(12, body.Factors.Velocity);
        Assert.Equal(12, body.Factors.Timing);
        Assert.Equal(15, body.Factors.HazardFlag);
        Assert.NotEmpty(body.Explanation);
    }

    [Fact]
    public async Task PostScoresReturnsBadRequestForMissingFields()
    {
        var response = await _client.PostAsJsonAsync(
            "/api/scores",
            new { }
        );

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);

        var body =
            await response.Content
                .ReadFromJsonAsync<ValidationProblemDetails>();

        Assert.NotNull(body);
        Assert.Contains(
            nameof(ScoreRequest.EstimatedDiameterMinKm),
            body.Errors.Keys
        );
        Assert.Contains(
            nameof(ScoreRequest.EstimatedDiameterMaxKm),
            body.Errors.Keys
        );
        Assert.Contains(
            nameof(ScoreRequest.MissDistanceKm),
            body.Errors.Keys
        );
        Assert.Contains(
            nameof(ScoreRequest.RelativeVelocityKps),
            body.Errors.Keys
        );
        Assert.Contains(
            nameof(ScoreRequest.IsPotentiallyHazardous),
            body.Errors.Keys
        );
        Assert.Contains(
            nameof(ScoreRequest.CloseApproachDate),
            body.Errors.Keys
        );
    }
}