@echo off
REM scripts/build_lambda.bat

echo Building Lambda package...

REM Variables
set BUILD_DIR=build
set LAYER_DIR=%BUILD_DIR%\layer\python
set FUNCTION_DIR=%BUILD_DIR%\function

REM Clean previous builds
echo Cleaning previous builds...
if exist %BUILD_DIR% rmdir /s /q %BUILD_DIR%
if exist lambda_function.zip del lambda_function.zip
if exist lambda_layer.zip del lambda_layer.zip

REM Create directories
mkdir %LAYER_DIR%
mkdir %FUNCTION_DIR%

REM Install dependencies to layer
echo Installing dependencies for Lambda layer...
pip install -r requirements.txt -t %LAYER_DIR% --upgrade

REM Clean up layer
echo Cleaning up layer...
cd %BUILD_DIR%\layer\python
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (tests) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (*.dist-info) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
cd ..\..\..

REM Create layer zip
echo Creating Lambda layer zip...
cd %BUILD_DIR%\layer
powershell Compress-Archive -Path * -DestinationPath ..\..\lambda_layer.zip -Force
cd ..\..

REM Copy application code
echo Copying application code...
xcopy /E /I /Y app %FUNCTION_DIR%\app

REM Create function zip
echo Creating Lambda function zip...
cd %FUNCTION_DIR%
powershell Compress-Archive -Path * -DestinationPath ..\..\lambda_function.zip -Force
cd ..\..

echo Build complete!
echo Lambda layer:    lambda_layer.zip
echo Lambda function: lambda_function.zip