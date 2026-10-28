param([string]$Path = (Get-Location).Path)

# 檢查 Markdown 筆記：相對連結、anchor、圖片位置與引用
$root = (Resolve-Path $Path).Path
$files = Get-ChildItem -Path $root -Recurse -Filter *.md

function Get-Slugs($file) {
  $slugs = @{}; $inCode = $false
  foreach ($line in [IO.File]::ReadAllLines($file, [Text.Encoding]::UTF8)) {
    if ($line -match '^\s*```') { $inCode = -not $inCode; continue }
    if ($inCode) { continue }
    if ($line -match '^#{1,6}\s+(.+?)\s*$') {
      $t = [regex]::Replace($matches[1].ToLowerInvariant(), '[^\p{L}\p{Nd}\s\-_]', '') -replace ' ', '-'
      $s = $t; $i = 1
      while ($slugs.ContainsKey($s)) { $s = "$t-$i"; $i++ }
      $slugs[$s] = $true
    }
  }
  $slugs
}

$problems = @()
$allText = ''
foreach ($f in $files) {
  $text = [IO.File]::ReadAllText($f.FullName, [Text.Encoding]::UTF8)
  $allText += "`n" + $text
  $text = [regex]::Replace($text, '(?s)```.*?```', '')
  foreach ($m in [regex]::Matches($text, '\]\(([^)\s]+)\)')) {
    $link = $m.Groups[1].Value
    if ($link -match '^(https?:|mailto:)') { continue }
    $parts = $link -split '#', 2
    $target = if ($parts[0]) { [IO.Path]::GetFullPath((Join-Path $f.DirectoryName ([uri]::UnescapeDataString($parts[0])))) } else { $f.FullName }
    $rel = $f.FullName.Replace($root, '')
    if (-not (Test-Path $target)) { $problems += "MISSING   $rel -> $link"; continue }
    if ($parts.Count -gt 1 -and $parts[1] -and $target -like '*.md') {
      if (-not (Get-Slugs $target).ContainsKey($parts[1])) { $problems += "ANCHOR    $rel -> $link" }
    }
  }
}

foreach ($img in Get-ChildItem -Path $root -Recurse -Include *.png, *.jpg, *.jpeg, *.gif, *.svg) {
  $rel = $img.FullName.Replace($root, '')
  if ($img.Directory.Name -ne 'src') { $problems += "NOT-IN-SRC $rel" }
  if ($allText -notmatch [regex]::Escape($img.Name)) { $problems += "UNUSED    $rel" }
}

"Checked $($files.Count) files"
$problems
