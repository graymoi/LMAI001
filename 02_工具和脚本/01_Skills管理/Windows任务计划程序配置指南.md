# Skills自动检查和更新 - Windows任务计划程序配置

## 📋 概述

本指南将帮助您配置Windows任务计划程序，实现Skills的**自动检查和更新**。

---

## 🔧 方法1: 使用批处理脚本（推荐，简单）

### 步骤1: 创建任务

1. **打开任务计划程序**
   - 按 `Win + R`，输入 `taskschd.msc`
   - 或：开始菜单 → Windows管理工具 → 任务计划程序

2. **创建基本任务**
   - 点击右侧"创建基本任务"
   - 名称：`Skills自动检查和更新`
   - 描述：`自动检查并更新npx skills`
   - 点击"下一步"

3. **触发器设置**
   - 选择"新建触发器"
   - 选择"按计划"
   - 设置：**每周** → **周日** → **凌晨2:00**
   - 点击"下一步"

4. **操作设置**
   - 选择"启动程序"
   - 程序或脚本：浏览到 `F:\AIlm\000项目管理\auto_update_skills.bat`
   - 起始于：`F:\AIlm\000项目管理`
   - 点击"下一步"

5. **完成**
   - 查看设置摘要
   - 勾选"当单击完成时，打开此任务属性的对话框"
   - 点击"完成"

6. **高级设置（可选）**
   - 在"条件"选项卡：
     - 勾选"只有在计算机使用交流网络连接时才启动此任务"
   - 在"设置"选项卡：
     - 如果任务运行时间超过：`30分钟`，停止任务
     - 如果任务失败，每隔：`1小时`重新启动
     - 最多重新启动次数：`3次`

### 步骤2: 测试任务

1. **手动运行测试**
   - 在任务计划程序中，找到"Skills自动检查和更新"任务
   - 右键点击 → 运行
   - 观察输出结果

2. **检查日志**
   - 查看桌面上的日志文件：`skills_update_log_YYYYMMDD.txt`
   - 确认脚本正常执行

### 步骤3: 启用任务

1. **启用任务**
   - 在任务计划程序中，找到任务
   - 右键点击 → 启用
   - 确认状态显示为"已启用"

2. **验证计划**
   - 查看任务属性中的"触发器"选项卡
   - 确认下次运行时间正确

---

## 🔧 方法2: 使用PowerShell脚本（高级）

### 步骤1: 创建PowerShell脚本

创建 `auto_update_skills.ps1`:
```powershell
# Skills自动检查和更新PowerShell脚本
# 作者: AI Assistant
# 日期: 2025-02-28

# 设置错误处理
$ErrorActionPreference = "Stop"

# 配置日志
$LogFile = "$env:USERPROFILE\Desktop\skills_update_log_$(Get-Date -Format 'yyyyMMdd').txt"
$Timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Add-Content -Path $LogFile -Value $LogEntry
    Write-Host $LogEntry
}

function Write-Success {
    param([string]$Message)
    Write-Log -Message $Message -Level "SUCCESS"
}

function Write-Error {
    param([string]$Message)
    Write-Log -Message $Message -Level "ERROR"
}

function Write-Warning {
    param([string]$Message)
    Write-Log -Message $Message -Level "WARNING"
}

function Write-Info {
    param([string]$Message)
    Write-Log -Message $Message -Level "INFO"
}

# 主函数
function Main {
    Write-Log "========================================"
    Write-Log "    Skills自动检查和更新"
    Write-Log "========================================"
    Write-Log ""
    
    try {
        # 检查npx是否可用
        Write-Info "检查npx是否可用..."
        $npxPath = Get-Command npx -ErrorAction SilentlyContinue
        
        if (-not $npxPath) {
            Write-Error "npx未找到，请先安装Node.js和npm"
            Write-Info "请访问 https://nodejs.org/ 安装Node.js"
            Write-Info "安装后，npx会自动可用"
            return
        }
        
        Write-Success "npx已找到"
        Write-Log ""
        
        # 检查已安装的skills
        Write-Log "========================================"
        Write-Log "步骤1: 检查已安装的skills"
        Write-Log "========================================"
        Write-Log ""
        
        $listOutput = npx skills list 2>&1
        Add-Content -Path $LogFile -Value $listOutput
        Write-Success "已安装skills列表已保存"
        Write-Log ""
        
        # 检查更新
        Write-Log "========================================"
        Write-Log "步骤2: 检查skills更新"
        Write-Log "========================================"
        Write-Log ""
        
        Write-Info "开始检查更新..."
        $checkOutput = npx skills check 2>&1
        Add-Content -Path $LogFile -Value $checkOutput
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "检查完成，无错误"
        } else {
            Write-Warning "检查过程中出现错误，退出代码: $LASTEXITCODE"
        }
        Write-Log ""
        
        # 自动更新
        Write-Log "========================================"
        Write-Log "步骤3: 自动更新skills"
        Write-Log "========================================"
        Write-Log ""
        
        Write-Info "开始更新所有skills..."
        $updateOutput = npx skills update 2>&1
        Add-Content -Path $LogFile -Value $updateOutput
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "所有skills已更新到最新版本"
        } else {
            Write-Error "更新过程中出现错误，退出代码: $LASTEXITCODE"
        }
        Write-Log ""
        
    } catch {
        Write-Error "发生未预期的错误: $_"
        Write-Log "异常详情: $($_.Exception.Message)"
    } finally {
        Write-Log "========================================"
        Write-Log "总结"
        Write-Log "========================================"
        Write-Log "日志文件: $LogFile"
        Write-Log ""
        Write-Success "脚本执行完成"
        Write-Log ""
    }
}

# 执行主函数
Main
```

### 步骤2: 配置PowerShell执行策略

1. **打开PowerShell执行策略**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **验证策略**
   ```powershell
   Get-ExecutionPolicy -List
   ```

### 步骤3: 创建任务计划程序任务

1. **打开任务计划程序**
   - 按 `Win + R`，输入 `taskschd.msc`

2. **创建基本任务**
   - 名称：`Skills自动检查和更新（PowerShell）`
   - 点击"下一步"

3. **触发器设置**
   - 每周 → 周日 → 凌晨2:00
   - 点击"下一步"

4. **操作设置**
   - 启动程序：`powershell.exe`
   - 添加参数：`-ExecutionPolicy Bypass -File "F:\AIlm\000项目管理\auto_update_skills.ps1"`
   - 起始于：`F:\AIlm\000项目管理`
   - 点击"下一步"

5. **完成并启用**

---

## 🔧 方法3: 使用Windows任务计划程序XML导入（最简单）

### 步骤1: 创建XML配置文件

创建 `skills_auto_update.xml`:
```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2025-02-28T00:00:00</Date>
    <Author>AI Assistant</Author>
    <Version>1.0</Version>
    <Description>自动检查并更新npx skills</Description>
    <URI>\</URI>
  </RegistrationInfo>
  
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-03-01T02:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Sunday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  
  <Principals>
    <Principal id="Author">
      <UserId>Administrator</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <Duration>PT10M</Duration>
      <WaitTimeout>PT1H</WaitTimeout>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
    <WakeToRun>false</WakeToRun>
    
    <ExecutionTimeLimit>PT30M</ExecutionTimeLimit>
    
    <Settings>
      <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
      <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
      <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
      <AllowHardTerminate>true</AllowHardTerminate>
      <StartWhenAvailable>false</StartWhenAvailable>
      <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
      
      <IdleSettings>
        <Duration>PT10M</Duration>
        <WaitTimeout>PT1H</WaitTimeout>
        <StopOnIdleEnd>true</StopOnIdleEnd>
        <RestartOnIdle>false</RestartOnIdle>
      </IdleSettings>
      
      <AllowStartOnDemand>true</AllowStartOnDemand>
      <Enabled>true</Enabled>
      <Hidden>false</Hidden>
      <RunOnlyIfIdle>false</RunOnlyIfIdle>
      <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
      <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
      <WakeToRun>false</WakeToRun>
      
      <Priority>7</Priority>
    </Settings>
    
    <Actions Context="Author">
      <Exec>
        <Command>cmd.exe</Command>
        <Arguments>/c "F:\AIlm\000项目管理\auto_update_skills.bat"</Arguments>
        <WorkingDirectory>F:\AIlm\000项目管理</WorkingDirectory>
      </Exec>
    </Actions>
  </Settings>
</Task>
```

### 步骤2: 导入任务

1. **打开任务计划程序**
   - 按 `Win + R`，输入 `taskschd.msc`

2. **导入任务**
   - 右侧点击"导入任务"
   - 选择 `skills_auto_update.xml`
   - 点击"打开"

3. **验证导入**
   - 查看任务列表
   - 确认"Skills自动检查和更新"任务已创建
   - 检查触发器和操作设置

---

## 📊 监控和管理

### 查看任务历史

1. **打开任务计划程序**
   - 找到"Skills自动检查和更新"任务
   - 右键点击 → 属性

2. **查看历史记录**
   - 切换到"历史记录"选项卡
   - 查看所有执行历史
   - 查看成功/失败状态

### 查看日志文件

**日志位置**: `%USERPROFILE%\Desktop\skills_update_log_YYYYMMDD.txt`

**日志格式**:
```
[2025-02-28 02:00:00] [INFO] 开始Skills检查和更新...
[2025-02-28 02:00:05] [SUCCESS] npx已找到
[2025-02-28 02:00:10] [INFO] 已安装skills列表已保存
[2025-02-28 02:00:15] [SUCCESS] 检查完成，无错误
[2025-02-28 02:00:20] [INFO] 开始更新所有skills...
[2025-02-28 02:00:45] [SUCCESS] 所有skills已更新到最新版本
[2025-02-28 02:00:46] [SUCCESS] 脚本执行完成
```

### 故障排除

**问题1: 任务未运行**
- 检查任务是否已启用
- 检查触发器设置是否正确
- 检查计算机是否在指定时间开机

**问题2: 脚本执行失败**
- 查看日志文件中的错误信息
- 手动运行脚本测试：`auto_update_skills.bat`
- 检查npx是否正确安装

**问题3: 网络连接问题**
- 确保任务设置中勾选了"只有在计算机使用交流网络连接时才启动此任务"
- 检查防火墙设置

---

## 🎯 推荐配置

### 最佳实践

1. **运行时间**: 每周日凌晨2:00（系统负载低）
2. **执行时间限制**: 30分钟（避免长时间运行）
3. **网络要求**: 只在网络连接时运行
4. **日志记录**: 保存到桌面便于查看
5. **错误处理**: 失败后1小时重试，最多3次

### 高级选项

1. **发送邮件通知**
   - 在任务属性中，添加"发送电子邮件"操作
   - 配置SMTP服务器和收件人

2. **显示消息**
   - 添加"显示消息"操作
   - 任务完成时弹出通知

3. **运行其他程序**
   - 在更新前/后运行其他脚本
   - 例如：备份、清理临时文件

---

## 📝 总结

### 三种方法对比

| 方法 | 复杂度 | 灵活性 | 推荐度 |
|------|---------|---------|---------|
| **批处理脚本** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **PowerShell脚本** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **XML导入** | ⭐ | ⭐⭐ | ⭐⭐ |

### 推荐方案

**对于大多数用户**: 使用**方法1（批处理脚本）**
- 简单易用
- 功能完整
- 易于维护

**对于高级用户**: 使用**方法2（PowerShell脚本）**
- 更强大的错误处理
- 更好的日志记录
- 更灵活的配置

**对于快速部署**: 使用**方法3（XML导入）**
- 一键导入
- 标准化配置
- 易于批量部署

---

**文档创建时间**: 2025-02-28
**适用系统**: Windows 10/11
**工具版本**: 任务计划程序