param(
    [Parameter(Mandatory=$true)][string]$ModelId,
    [Parameter(Mandatory=$true)][string]$Revision,
    [Parameter(Mandatory=$true)][string]$OutputDir
)
# Public pinned weights only; never read or persist provider/Hugging Face credentials.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
try {
    if ($ModelId -notmatch '^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$' -or $Revision -notmatch '^[a-f0-9]{40}$') {
        throw 'Invalid pinned model identity'
    }
    Add-Type -AssemblyName System.Net.Http
    $taskClient = [Net.Http.HttpClient]::new()
    $taskClient.Timeout = [TimeSpan]::FromSeconds(300)
    $taskApi = "https://huggingface.co/api/models/$ModelId/tree/${Revision}?recursive=false"
    $taskTree = $taskClient.GetStringAsync($taskApi).GetAwaiter().GetResult() | ConvertFrom-Json
    $taskAllowed = @('config.json','model.safetensors','tokenizer.json','tokenizer_config.json','special_tokens_map.json','vocab.txt')
    $taskFiles = @($taskTree | Where-Object { $_.path -in $taskAllowed })
    if ($taskFiles.Count -ne $taskAllowed.Count) { throw 'Required local model files are missing' }
    $taskOutput = [IO.Path]::GetFullPath($OutputDir)
    [IO.Directory]::CreateDirectory($taskOutput) | Out-Null
    $taskRecords = @()
    foreach ($taskFile in $taskFiles) {
        $taskDestination = [IO.Path]::Combine($taskOutput, $taskFile.path)
        if ([IO.File]::Exists($taskDestination)) {
            $taskBytes = [IO.File]::ReadAllBytes($taskDestination)
        } else {
            $taskUri = "https://huggingface.co/$ModelId/resolve/$Revision/$($taskFile.path)"
            $taskBytes = $taskClient.GetByteArrayAsync($taskUri).GetAwaiter().GetResult()
        }
        if ($taskBytes.LongLength -ne $taskFile.size) { throw 'Pinned file size differs' }
        $taskSha256 = [BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($taskBytes)).Replace('-','').ToLowerInvariant()
        if ($null -ne $taskFile.lfs) {
            if ($taskSha256 -ne $taskFile.lfs.oid) { throw 'Pinned LFS content hash differs' }
            $taskBasis = 'registered-lfs-sha256'
        } else {
            $taskHeader = [Text.Encoding]::UTF8.GetBytes("blob $($taskBytes.LongLength)`0")
            $taskGitSha = [BitConverter]::ToString([Security.Cryptography.SHA1]::Create().ComputeHash([byte[]]($taskHeader + $taskBytes))).Replace('-','').ToLowerInvariant()
            if ($taskGitSha -ne $taskFile.oid) { throw 'Pinned Git blob identity differs' }
            $taskBasis = 'pinned-git-blob-sha1'
        }
        if (-not [IO.File]::Exists($taskDestination)) { [IO.File]::WriteAllBytes($taskDestination,$taskBytes) }
        $taskRecords += @{file=$taskFile.path; bytes=$taskBytes.LongLength; sha256=$taskSha256; verification_basis=$taskBasis}
        $taskBytes = $null
    }
    $taskManifest = @{schema='pinned-public-transformer-v1'; model=$ModelId; revision=$Revision; files=$taskRecords; remote_code_used=$false; credentials_used=$false}
    $taskManifestPath = [IO.Path]::Combine($taskOutput,'model-source.json')
    $taskEncoded = $taskManifest | ConvertTo-Json -Depth 10
    if ([IO.File]::Exists($taskManifestPath)) {
        if ([IO.File]::ReadAllText($taskManifestPath) -ne $taskEncoded) { throw 'Model source inventory differs' }
    } else {
        [IO.File]::WriteAllText($taskManifestPath,$taskEncoded,[Text.UTF8Encoding]::new($false))
    }
    [Console]::Out.Write(($taskManifest | ConvertTo-Json -Depth 10 -Compress))
    $taskClient.Dispose()
} catch {
    [Console]::Out.Write('{"status":"failed","reason":"pinned-model-fetch-or-integrity-failed","native_output_suppressed":true}')
    exit 1
}
