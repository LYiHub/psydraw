<p align="center">
  <img src="assets/logo2.png" alt="PsyDraw Logo" width="200"/>
</p>

<h1 align="center">PsyDraw: 面向留守儿童心理健康检测的多智能体多模态系统</h1>

<p align="center">
  <a href="README.md">
    <img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge" alt="English">
  </a>
  <a href="README_CN.md">
    <img src="https://img.shields.io/badge/语言-中文-blue?style=for-the-badge" alt="中文">
  </a>
  <a href="https://psysraw.zeabur.app/HTP_Test">
    <img src="https://img.shields.io/badge/演示-在线网站-blue?style=for-the-badge" alt="在线演示">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/许可证-GPL%203.0-green?style=for-the-badge" alt="许可证">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/⚠️%20仅供专业人士使用-FF0000?style=for-the-badge" alt="仅供专业人士使用">
</p>

## ⚠️ 重要伦理声明及专业使用指南

**重要提示：本系统严格设计为专业筛查辅助工具**

出于心理健康评估的伦理考虑，本仓库仅包含项目的代码结构。为防止滥用并确保正确应用，系统的提示词和分析组件并未开源。

### 仅供专业人士使用
- 本工具专门设计用于协助合格的心理健康专业人员（精神科医生、心理咨询师和学校心理辅导员）进行初步筛查
- 严禁未经专业培训的个人用于自我评估或互相评估
- 所有结果必须由具有资质的心理健康专业人员解释和验证

### 完整系统访问
如需出于研究或临床目的访问完整系统（包括提示词），请联系我们：[project.htp@lyi.ai]。访问权限将仅在满足以下条件后授予：
1. 专业资质验证
2. 使用目的审核
3. 同意伦理准则和使用条款

### 风险防范
- 心理评估工具的滥用可能导致错误解读和潜在危害
- 系统应仅在专业人员监督下的专业环境中部署
- 所有实施必须遵守心理健康评估相关的伦理准则和法规

## 项目概述
留守儿童由于父母外出务工面临严重的心理健康挑战。房树人测验（HTP）是一种心理评估方法，具有较高的儿童参与度和配合度，但需要专业解释，限制了其在资源匮乏地区的应用。为解决这一问题，我们提出了**PsyDraw**，一个基于多模态大语言模型的多智能体系统，用于辅助分析HTP绘画并评估留守儿童的心理健康状况。系统工作流程包括特征分析和报告生成两个主要阶段，由多个协作智能体完成。我们对290名小学生的HTP绘画进行了系统评估，生成的心理健康报告由班主任评价。结果显示，71.03%的分析被评为**匹配**，26.21%被评为**基本匹配**，仅2.41%被评为**不匹配**。这些发现展示了PsyDraw在辅助专业人员进行HTP测试分析方面的潜力。

<p align="center">
  <img src="assets/workflow.png" alt="PsyDraw工作流程"/>
  <br>
  <em>图1: PsyDraw的工作流程</em>
</p>

## ✨ 主要特点

<p align="center">
  <img src="https://img.shields.io/badge/HTP分析-专业级辅助-blue?style=for-the-badge" alt="HTP分析">
  <img src="https://img.shields.io/badge/语言支持-EN%20%7C%20中文-blue?style=for-the-badge" alt="语言">
  <img src="https://img.shields.io/badge/API-专业医疗集成-blue?style=for-the-badge" alt="API">
  <img src="https://img.shields.io/badge/网页工具-专业监督评估-blue?style=for-the-badge" alt="网页工具">
</p>

## 🚀 快速开始

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/LYiHub/psydraw.git
cd PsyDraw
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量：
- 复制 `.env_example` 文件并重命名为 `.env`
- 填写您的API密钥和基础URL

### 使用方法

<p align="center">
  <img src="https://img.shields.io/badge/1-直接调用-orange?style=for-the-badge" alt="直接调用">
  <img src="https://img.shields.io/badge/2-API集成-orange?style=for-the-badge" alt="API">
  <img src="https://img.shields.io/badge/3-网页演示-orange?style=for-the-badge" alt="网页">
  <img src="https://img.shields.io/badge/4-打包应用-orange?style=for-the-badge" alt="打包">
</p>

#### 1. 直接调用
```bash
bash run.sh
# 或
python run.py --image_file example/example1.png --save_path example/example1_result.json --language zh
```

#### 2. API集成
```bash
python deploy.py --port 9557
```
服务运行于 `http://127.0.0.1:9557`

#### 3. 网页演示
```bash
bash web_demo.sh
# 或
streamlit run src/main.py
```

#### 4. 打包应用
```bash
pyinstaller htp_analyzer.spec
```

## 📊 案例研究
<p align="center">
  <img src="assets/case_study1.png" width="45%" />
  <img src="assets/case_study2.png" width="45%" /> 
</p>

## ⚖️ 许可证

本项目采用GPL-3.0许可证。详情请参见[LICENSE](LICENSE)文件。

## ⚠️ 免责声明

PsyDraw严格作为专业筛查辅助工具。它不得作为独立的诊断工具或替代专业医疗评估。该系统旨在支持而非取代合格心理健康专业人员的专业知识。任何系统的实施或使用都必须在专业监督下进行。 