<p align="center">
  <img src="assets/logo2.png" alt="PsyDraw Logo" width="200"/>
</p>

<h1 align="center">PsyDraw: A Multi-Agent Multimodal System for Mental Health Screening in Left-Behind Children</h1>

<p align="center">
  <a href="README.md">
    <img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge" alt="English">
  </a>
  <a href="README_CN.md">
    <img src="https://img.shields.io/badge/语言-中文-blue?style=for-the-badge" alt="中文">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-GPL%203.0-green?style=for-the-badge" alt="License">
  </a>
  <a href="https://arxiv.org/abs/2412.14769">
    <img src="https://img.shields.io/badge/Paper-arXiv-red?style=for-the-badge" alt="Paper">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/⚠️%20Professional%20Use%20Only-FF0000?style=for-the-badge" alt="Professional Use Only">
</p>

## ⚠️ Important Ethical Notice and Professional Use Guidelines

**CRITICAL: This system is strictly designed as a professional screening aid tool.**

This repository contains only the code structure of our project due to ethical considerations in mental health assessment. The system's prompts and analytical components are not open-sourced to prevent misuse and ensure proper application.

### Professional Use Only
- This tool is exclusively designed to assist qualified mental health professionals (psychiatrists, psychological counselors, and school counselors) in preliminary screening.
- It MUST NOT be used for self-assessment or peer assessment by individuals without professional qualifications.
- All results require interpretation and validation by qualified mental health professionals.

### Access to Full System
For research or clinical purposes requiring access to the complete system (including prompts), please contact us at: [project.htp@lyi.ai]. Access will only be granted after:
1. Verification of professional credentials
2. Review of intended use case
3. Agreement to ethical guidelines and usage terms

### Risk Prevention
- Misuse of psychological assessment tools can lead to incorrect interpretations and potentially harmful outcomes
- The system should only be deployed in professional settings under qualified supervision
- All implementations must comply with relevant ethical guidelines and regulations in mental health assessment

## Project Overview
Left-behind children (LBC) face severe mental health challenges due to parental migration for work. The House-Tree-Person (HTP) test, a psychological assessment method with higher child participation and cooperation, requires expert interpretation, limiting its application in resource-scarce areas. To address this, we propose **PsyDraw**, a multi-agent system based on Multimodal Large Language Models for automated analysis of HTP drawings and assessment of LBC's mental health status. The system's workflow comprises two main stages: feature analysis and report generation, accomplished by multiple collaborative agents. We evaluate the system on HTP drawings from 290 primary school students, with the generated mental health reports evaluated by class teachers. Results show that 71.03\% of the analyses are rated as **Matching**, 26.21\% as **Generally Matching**, and only 2.41\% as **Not Matching**. These findings demonstrate the potential of PsyDraw in supporting professional mental health assessment for LBC.

<p align="center">
  <img src="assets/workflow.png" alt="PsyDraw Workflow"/>
  <br>
  <em>Figure 1: The workflow of PsyDraw</em>
</p>

## ✨ Key Features

<p align="center">
  <img src="https://img.shields.io/badge/HTP%20Analysis-Professional%20Grade-blue?style=for-the-badge" alt="HTP Analysis">
  <img src="https://img.shields.io/badge/Languages-EN%20%7C%20中文-blue?style=for-the-badge" alt="Languages">
  <img src="https://img.shields.io/badge/API-Professional%20Healthcare-blue?style=for-the-badge" alt="API">
  <img src="https://img.shields.io/badge/Web%20Tool-Supervised%20Assessment-blue?style=for-the-badge" alt="Web Tool">
</p>

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LYiHub/psydraw.git
cd PsyDraw
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env_example` file and rename to `.env`
- Fill in your API key and base URL

### Usage Methods

<p align="center">
  <img src="https://img.shields.io/badge/1-Direct%20Invocation-orange?style=for-the-badge" alt="Direct">
  <img src="https://img.shields.io/badge/2-API%20Integration-orange?style=for-the-badge" alt="API">
  <img src="https://img.shields.io/badge/3-Web%20Demo-orange?style=for-the-badge" alt="Web">
  <img src="https://img.shields.io/badge/4-Package%20App-orange?style=for-the-badge" alt="Package">
</p>

#### 1. Direct Invocation
```bash
bash run.sh
# or
python run.py --image_file example/example1.png --save_path example/example1_result.json --language en
```

#### 2. API Integration
```bash
python deploy.py --port 9557
```
Service runs on `http://127.0.0.1:9557`

#### 3. Web Demo
```bash
bash web_demo.sh
# or
streamlit run src/main.py
```

#### 4. Package Application
```bash
pyinstaller htp_analyzer.spec
```

## 📊 Case Studies
<p align="center">
  <img src="assets/case_study1.png" width="45%" />
  <img src="assets/case_study2.png" width="45%" /> 
</p>

## ⚖️ License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

PsyDraw is strictly a professional screening aid tool. It must not be used as a standalone diagnostic tool or a substitute for professional medical evaluation. The system is designed to support, not replace, the expertise of qualified mental health professionals. Any implementation or use of this system must be under professional supervision.

## 📚 Citation

If you find this work helpful, please cite our paper:

```bibtex
@misc{zhang2024psydrawmultiagentmultimodalmental,
      title={PsyDraw: A Multi-Agent Multimodal System for Mental Health Screening in Left-Behind Children}, 
      author={Yiqun Zhang and Xiaocui Yang and Xiaobai Li and Siyuan Yu and Yi Luan and Shi Feng and Daling Wang and Yifei Zhang},
      year={2024},
      eprint={2412.14769},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.14769}, 
}
```