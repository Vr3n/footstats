
param (
    [string[]]$DockerArgs
)

function CtrlC {
    Write-Host "Gracefully shutting down containers ..."
    docker compose --profile dev down --volumes
}

try {
    docker compose --profile dev up $DockerArgs
} finally {
    CtrlC
}
