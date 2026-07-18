using Astral.Scoring.Api.Models;
using Astral.Scoring.Api.Services;

using Microsoft.AspNetCore.Mvc;

namespace Astral.Scoring.Api.Controllers;

[ApiController]
[Route("api/scores")]
public class ScoresController : ControllerBase
{
    private readonly ScoreCalculator _calculator;

    public ScoresController(ScoreCalculator calculator)
    {
        _calculator = calculator;
    }

    [HttpPost]
    public ActionResult<ScoreResponse> CreateScore(ScoreRequest request)
    {
        var currentDate = DateOnly.FromDateTime(DateTime.UtcNow);
        var response = _calculator.Calculate(request, currentDate);

        return Ok(response);
    }
}