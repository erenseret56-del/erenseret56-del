# Rebuild the terminal hero using Windows' built-in drawing library.
# Optional input: assets/toji-hero.png (transparent full-body artwork preferred).
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$assetDir = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../assets'))
[IO.Directory]::CreateDirectory($assetDir) | Out-Null
$canvas = New-Object Drawing.Bitmap 1440,850
$g = [Drawing.Graphics]::FromImage($canvas)
$g.SmoothingMode = [Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [Drawing.Text.TextRenderingHint]::AntiAliasGridFit
function Color($hex) { [Drawing.ColorTranslator]::FromHtml($hex) }
function Box($x,$y,$w,$h,$hex) {
    $b = New-Object Drawing.SolidBrush (Color $hex)
    $g.FillRectangle($b,$x,$y,$w,$h)
    $b.Dispose()
}
function Line($x,$y,$xx,$yy,$hex,$width=1) {
    $p = New-Object Drawing.Pen (Color $hex),$width
    $g.DrawLine($p,$x,$y,$xx,$yy)
    $p.Dispose()
}
function Label($text,$x,$y,$size,$hex,$family='Consolas') {
    $f = New-Object Drawing.Font $family,$size,([Drawing.FontStyle]::Regular),([Drawing.GraphicsUnit]::Pixel)
    $b = New-Object Drawing.SolidBrush (Color $hex)
    $g.DrawString($text,$f,$b,$x,$y)
    $b.Dispose()
    $f.Dispose()
}
try {
    $bg = New-Object Drawing.Drawing2D.LinearGradientBrush ([Drawing.Rectangle]::new(0,0,1440,850)),(Color '#04080E'),(Color '#0C192A'),25
    $g.FillRectangle($bg,0,0,1440,850)
    $bg.Dispose()
    for ($x=32; $x -lt 1440; $x+=48) { Line $x 72 $x 790 '#101D2B' }
    for ($y=96; $y -lt 800; $y+=48) { Line 32 $y 1408 $y '#101D2B' }
    Box 0 0 1440 68 '#0D1724'
    Line 0 68 1440 68 '#284052'
    foreach ($dot in @(@(34,'#64EDB4'),@(58,'#55ADFF'),@(82,'#405269'))) {
        $b = New-Object Drawing.SolidBrush (Color $dot[1])
        $g.FillEllipse($b,[int]$dot[0],27,12,12)
        $b.Dispose()
    }
    Label 'RUTHVIK / PERSONAL OPERATING SYSTEM' 120 22 21 '#B9C9DC'
    Label 'PROFILE.SYS  /  01' 1120 24 18 '#64EDB4'

    Box 48 122 234 36 '#12372E'
    Label 'DEVELOPER EDITION' 62 128 20 '#64EDB4'
    Label '> boot identity' 48 190 24 '#55ADFF'
    Label 'SAI RUTHVIK' 44 235 79 '#F0F6FC' 'Segoe UI'
    Label 'REDDY' 44 320 91 '#64EDB4' 'Segoe UI'
    Line 52 442 174 442 '#64EDB4' 4
    Label 'FULL STACK DEVELOPER' 48 476 29 '#E5EDF7'
    Label 'UI/UX ENTHUSIAST  /  BUILDER' 48 520 23 '#9FB3CA'
    Label 'Build with intent.' 48 602 30 '#E5EDF7'
    Label 'Hyderabad, India' 48 656 22 '#8EA7C1'
    Label '@erenseret56-del' 48 694 22 '#55ADFF'

    Box 804 112 586 628 '#07121E'
    # Cinematic diagonal rim lights; the artwork remains entirely within its frame.
    for ($i=0; $i -lt 7; $i++) {
        Line (896+$i*16) 124 (820+$i*16) 728 '#123D37' 8
        Line (1336+$i*7) 124 (1216+$i*7) 728 '#102D49' 3
    }
    Line 804 112 866 112 '#64EDB4' 3
    Line 804 112 804 174 '#64EDB4' 3
    Line 1328 740 1390 740 '#55ADFF' 3
    Line 1390 678 1390 740 '#55ADFF' 3
    $artPath = Join-Path $assetDir 'toji-hero.png'
    if (Test-Path -LiteralPath $artPath) {
        $art = [Drawing.Image]::FromFile($artPath)
        try {
            $ratio = [Math]::Min(558.0/$art.Width,590.0/$art.Height)
            $w = [int]($art.Width*$ratio)
            $h = [int]($art.Height*$ratio)
            $g.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $g.DrawImage($art,[int](1097-$w/2),[int](424-$h/2),$w,$h)
        } finally { $art.Dispose() }
    } else {
        Label 'ASSET / 001' 846 158 20 '#64EDB4'
        Label 'TOJI' 846 267 72 '#E5EDF7' 'Segoe UI'
        Label 'FUSHIGURO' 846 352 45 '#9FB3CA' 'Segoe UI'
        Box 846 450 400 44 '#13332E'
        Label 'ARTWORK PLACEHOLDER' 862 458 23 '#64EDB4'
        Label 'Full-body / katana' 846 540 23 '#B9C9DC'
        Label 'Emerald rim / blue shadows' 846 579 21 '#8EA7C1'
        Label 'assets/toji-hero.png' 846 672 22 '#55ADFF'
    }
    Box 0 788 1440 62 '#0B1522'
    Line 0 788 1440 788 '#284052'
    Label '01 / IDENTITY' 48 808 19 '#64EDB4'
    Label '02 / TOOLKIT' 328 808 19 '#8EA7C1'
    Label '03 / BUILDS' 608 808 19 '#8EA7C1'
    Label 'FOCUS > FRICTION' 1140 808 19 '#55ADFF'
    $canvas.Save((Join-Path $assetDir 'hero.png'),[Drawing.Imaging.ImageFormat]::Png)
} finally {
    $g.Dispose()
    $canvas.Dispose()
}
Write-Output 'Generated assets/hero.png'
