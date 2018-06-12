@ECHO OFF
setlocal DISABLEDELAYEDEXPANSION
SET BIN_TARGET=%~dp0/../google/cloud-tools/src/Utils/Flex/flex_exec
php "%BIN_TARGET%" %*
