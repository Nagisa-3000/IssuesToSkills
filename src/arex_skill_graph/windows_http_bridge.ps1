# HTTP bridge for WSL hosts whose Linux resolver cannot reach a provider.
# Request/credential arrive only on stdin. Never emit stderr or request headers.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
try {
    [Console]::InputEncoding = [Text.UTF8Encoding]::new($false)
    $taskInput = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $taskUri = [Uri]$taskInput.endpoint
    if ($taskUri.Scheme -ne 'https' -or $taskUri.UserInfo -ne '') { throw 'Invalid endpoint' }
    Add-Type -AssemblyName System.Net.Http
    $taskClient = [System.Net.Http.HttpClient]::new()
    $taskClient.Timeout = [TimeSpan]::FromSeconds([double]$taskInput.timeout_seconds)
    $taskClient.DefaultRequestHeaders.Authorization = [System.Net.Http.Headers.AuthenticationHeaderValue]::new('Bearer', [string]$taskInput.credential)
    $taskBody = $taskInput.body | ConvertTo-Json -Depth 100 -Compress
    $taskContent = [System.Net.Http.StringContent]::new($taskBody, [Text.Encoding]::UTF8, 'application/json')
    $taskResponse = $taskClient.PostAsync($taskUri, $taskContent).GetAwaiter().GetResult()
    $taskText = $taskResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    $taskResult = @{status=[int]$taskResponse.StatusCode; body=$taskText}
    [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
    [Console]::Out.Write(($taskResult | ConvertTo-Json -Depth 100 -Compress))
    $taskClient.Dispose()
} catch {
    [Console]::Out.Write('{"status":0,"body":"","bridge_error":"transport-failed"}')
    exit 1
} finally {
    $taskInput = $null
    $taskBody = $null
    $taskText = $null
}
