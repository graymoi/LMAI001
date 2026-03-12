@echo off
chcp 65001 >nul
title Skills自动检查和更新工具
color 0A

echo.
echo ========================================
echo    Skills自动检查和更新工具
echo ========================================
echo.

REM 设置日志文件
set LOG_FILE=%USERPROFILE%\Desktop\skills_update_log_%date:~0,4%%date:~5,2%%date:~8,2%.txt
set TIMESTAMP=%date% %time%

echo [%TIMESTAMP%] 开始Skills检查和更新... > "%LOG_FILE%"

REM 检查npx skills是否可用
where npx >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] npx未找到，请先安装Node.js和npm
    echo [%TIMESTAMP%] 错误: npx未找到 >> "%LOG_FILE%"
    echo.
    echo 请访问 https://nodejs.org/ 安装Node.js
    echo 安装后，npx会自动可用
    echo.
    pause
    exit /b 1
)

echo [信息] npx已找到，开始检查skills...
echo [%TIMESTAMP%] npx已找到 >> "%LOG_FILE%"
echo.

REM 检查已安装的skills
echo ========================================
echo 步骤1: 检查已安装的skills
echo ========================================
echo.
npx skills list >> "%LOG_FILE%" 2>&1
echo.
echo [%TIMESTAMP%] 已安装skills列表已保存 >> "%LOG_FILE%"

REM 检查更新
echo ========================================
echo 步骤2: 检查skills更新
echo ========================================
echo.
echo [%TIMESTAMP%] 开始检查更新... >> "%LOG_FILE%"
npx skills check >> "%LOG_FILE%" 2>&1
set CHECK_RESULT=%ERRORLEVEL%
echo.
if %CHECK_RESULT% EQU 0 (
    echo [成功] 检查完成
    echo [%TIMESTAMP%] 检查完成，无错误 >> "%LOG_FILE%"
) else (
    echo [警告] 检查过程中出现错误
    echo [%TIMESTAMP%] 检查错误，代码: %CHECK_RESULT% >> "%LOG_FILE%"
)
echo.

REM 询问是否更新
echo ========================================
echo 步骤3: 更新skills
echo ========================================
echo.
set /p UPDATE_CHOICE=是否立即更新所有skills？ (Y/N): 
if /i "%UPDATE_CHOICE%"=="Y" (
    echo [%TIMESTAMP%] 用户选择更新skills >> "%LOG_FILE%"
    echo.
    echo [信息] 开始更新所有skills...
    npx skills update >> "%LOG_FILE%" 2>&1
    set UPDATE_RESULT=%ERRORLEVEL%
    echo.
    if %UPDATE_RESULT% EQU 0 (
        echo [成功] 所有skills已更新到最新版本
        echo [%TIMESTAMP%] 更新成功 >> "%LOG_FILE%"
    ) else (
        echo [错误] 更新过程中出现错误
        echo [%TIMESTAMP%] 更新错误，代码: %UPDATE_RESULT% >> "%LOG_FILE%"
    )
) else (
    echo [%TIMESTAMP%] 用户选择不更新 >> "%LOG_FILE%"
    echo [信息] 跳过更新步骤
)
echo.

REM 显示总结
echo ========================================
echo    总结
echo ========================================
echo.
echo 日志文件: %LOG_FILE%
echo.
echo [%TIMESTAMP%] 脚本执行完成 >> "%LOG_FILE%"
echo.
echo 按任意键退出...
pause >nul