FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build

WORKDIR /src

COPY Astral.Scoring.Api/Astral.Scoring.Api.csproj Astral.Scoring.Api/
RUN dotnet restore Astral.Scoring.Api/Astral.Scoring.Api.csproj

COPY . .

WORKDIR /src/Astral.Scoring.Api
RUN dotnet publish \
    Astral.Scoring.Api.csproj \
    --configuration Release \
    --output /app/publish \
    --no-restore \
    /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final

WORKDIR /app

ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

COPY --from=build /app/publish .

USER app

ENTRYPOINT ["dotnet", "Astral.Scoring.Api.dll"]