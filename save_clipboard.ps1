Add-Type -AssemblyName System.Windows.Forms
$img = [System.Windows.Forms.Clipboard]::GetImage()
if ($img -ne $null) {
    $img.Save($args[0], [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output "Image saved to $args[0]"
} else {
    Write-Output "No image found in clipboard"
}
