import streamlit as st
from PIL import Image
import pandas as pd

def get_text(key):
    return translations[st.session_state.language][key]

translations = {
    "English": {
        "title": "PsyDraw: A Multi-Agent Multimodal System for Mental Health Detection in Left-Behind Children",
        "introduction": "Introduction of HTP Test",
        "introduction_content": "The House-Tree-Person (HTP) test is a projective psychological assessment tool applicable to both children and adults aged 3 and above. This test aims to provide insights into an individual's personality, emotions, and attitudes through the analysis of drawings. In the HTP test procedure, participants are instructed to draw a house, a tree, and a person. Researchers analyze HTP drawings to evaluate cognitive, emotional, and social functioning, interpreting depicted elements as reflections of hidden emotions, desires, and internal conflicts not easily discerned through direct methods.",
        "available_features": """
        We provide the necessary **API key** and **base URL** for **PsyDraw** in the ***supplementary materials***.
        
        **Available Features:**
        - **Batch Analysis**: Analyze multiple HTP drawings in bulk
        - **HTP Test**: Take the House-Tree-Person test online
        - **Online Board**: Use our digital drawing tool to create HTP drawings
        """,
        "batch_analysis": "Batch Analysis: Analyze multiple HTP drawings in bulk",
        "htp_test": "HTP Test: Take the House-Tree-Person test online",
        "online_board": "Online Board: Use our digital drawing tool to create HTP drawings",
        "contact_admin": "Please contact the administrator for access to these features.",
        "github_link": "Visit our GitHub repository for more information and updates.",
        "abstract": "Abstract",
        "abstract_content": """
    Left-behind children face severe mental health challenges due to parental migration for work. \
    The House-Tree-Person (HTP) test, a psychological assessment method with higher child participation and cooperation, requires expert interpretation, limiting its application in resource-scarce areas. \
    To address this, we propose **PsyDraw**, a multi-agent system based on Multimodal Large Language Models for automated analysis of HTP drawings and assessment of children's mental health status.  \
    The system's workflow comprises two main stages: feature extraction and analysis, and report generation, accomplished by multiple collaborative agents.  \
    We evaluate the system on HTP drawings from 290 primary school students, with the generated mental health reports evaluated by class teachers.  \
    Results show that 71.03% of the analyses are rated as **Match**, 26.21% as **Generally Match**, and only 2.41% as **Not Match**. \
    These findings demonstrate the potential of PsyDraw in automating HTP test analysis, offering an innovative solution to the shortage of professional personnel in mental health assessment for left-behind children.         
    """,
        "system_workflow": "The Workflow of PsyDraw",
        "key_features": "Key Features",
        "automated_analysis": "Automated Analysis",
        "multi_agent_system": "Multi-Agent System",
        "scalable_solution": "Scalable Solution",
        "evaluation_results": "Evaluation Results",
        "matching_rates": "Matching rates of results with teacher feedback.",
        "participants_note": "Note: All test participants were primary school students. This study was conducted with proper authorization from relevant personnel.",
        "limitations": "Limitations",
        "limitation_content": """
    PsyDraw is designed for early detection of mental health issues among left-behind children in resource-limited areas. However, it is not a substitute for professional medical advice. Key limitations include:

    1. Cultural context: Currently validated only with Chinese children.
    2. Data protection: Requires stringent mechanisms to ensure privacy and ethical compliance.
    3. Potential biases: As an MLLM-based tool, it may harbor inherent biases.
    4. Long-term effectiveness: Not yet confirmed through longitudinal studies.
    5. Subtle cues: May miss nuances that human professionals can identify in face-to-face interactions.
    6. Technological constraints: Efficacy may be limited by infrastructure and user capabilities.
    """,
        "case_study": "Case Study",
        "footer": "© 2024 PsyDraw. All rights reserved.",
    },
    "中文": {
        "title": "PsyDraw: A Multi-Agent Multimodal System for Mental Health Detection in Left-Behind Children",
        "introduction": "房树人介绍",
        "introduction_content": "房-树-人（HTP）测试是一种适用于3岁及以上儿童和成人的投射性心理评估工具。该测试旨在通过分析绘画来深入了解个体的人格、情感和态度。在HTP测试过程中，参与者被要求画一栋房子、一棵树和一个人。研究人员分析HTP绘画以评估认知、情感和社交功能，将所描绘的元素解读为难以通过直接方法察觉的隐藏情感、欲望和内部冲突的反映。",
        "available_features": """
        注意: 我们在***支撑材料***中提供了**PsyDraw**所需的**API密钥**和**BaseURL**。
        
        **可用功能：** 
        - **Batch**：批量分析多个HTP图纸 
        - **HTP Test**：在线进行房树人测试 
        - **Online Board**：使用我们的数字绘图工具创建HTP绘图
        """,
        "batch_analysis": "批量分析：批量分析多个HTP绘画",
        "htp_test": "HTP测试：在线进行房树人测试",
        "online_board": "在线画板：使用我们的数字绘图工具创建HTP绘画",
        "contact_admin": "请联系管理员以获取这些功能的访问权限。",
        "github_link": "访问我们的GitHub仓库以获取更多信息和更新。",
        "abstract": "摘要",
        "abstract_content": """
        留守儿童因父母外出务工而面临严重的心理健康挑战。房屋-树木-人物（HTP）测试是一种儿童参与度和配合度较高的心理评估方法，但需要专家解读，限制了其在资源匮乏地区的应用。 \
        为解决这一问题，我们提出了PsyDraw，一个基于多模态大型语言模型的多智能体系统，用于自动分析HTP绘画并评估儿童的心理健康状况。系统的工作流程包括两个主要阶段：特征提取和分析，以及报告生成，这些由多个协作智能体完成。 \
        我们对290名小学生的HTP绘画进行了系统评估，生成的心理健康报告由班主任进行评价。\
        结果显示，71.03%的分析被评为匹配，26.21%被评为基本匹配，仅有2.41%被评为不匹配。 \
        这些发现证明了PsyDraw在自动化HTP测试分析方面的潜力，为解决留守儿童心理健康评估专业人员短缺问题提供了一种创新解决方案。""",
        "system_workflow": "PsyDraw工作流程",
        "key_features": "主要特性",
        "automated_analysis": "自动化分析",
        "multi_agent_system": "多智能体系统",
        "scalable_solution": "可扩展解决方案",
        "evaluation_results": "评估结果",
        "matching_rates": "结果与教师反馈的匹配率。",
        "participants_note": "注：所有测试参与者均为小学生。本研究经过相关人员的适当授权进行。",
        "limitations": "局限性",
        "limitation_content": """
        PsyDraw旨在为资源有限地区的留守儿童提供心理健康问题的早期检测。然而，它不能替代专业的医疗建议。主要局限性包括：

        1. 文化背景：目前仅在中国儿童群体中得到验证。
        2. 数据保护：需要严格的机制来确保隐私和伦理合规。
        3. 潜在偏见：作为一个基于多模态大语言模型的工具，可能存在固有偏见。
        4. 长期有效性：尚未通过纵向研究确认。
        5. 细微线索：可能会忽略人类专业人员在面对面互动中能够识别的微妙细节。
        6. 技术限制：效果可能受到基础设施和用户能力的限制。
        """,
        "case_study": "案例研究",
        "footer": "© 2024 PsyDraw。保留所有权利。",
    }
}


def sidebar():  
# 侧边栏
    with st.sidebar:
        st.image("assets/logo2.png", use_column_width=True)
        st.title("House-Tree-Person Test")

        st.write("## Language / 语言")
        language = st.selectbox("Choose a language / 选择语言", ["English", "中文"], key="language_selector")
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
            
        st.subheader(get_text("introduction"))
        st.write(get_text("introduction_content"))

def main_page():
    st.title(get_text('title'))

    st.info(get_text('available_features'))

    st.write(f"## {get_text('abstract')}")
    st.write(get_text('abstract_content'))

    st.write(f"## {get_text('system_workflow')}")
    st.image("assets/workflow.png", use_column_width=True)

    st.write(f"## {get_text('evaluation_results')}")
    results_data = {
        "Category": ["Matching", "Generally Matching", "Not Matching"],
        "Total (%)": [71.03, 26.21, 2.41],
        "Warn. (%)": [58.89, 35.56, 4.44],
        "Obs. (%)": [76.50, 22.00, 1.50]
    }
    df = pd.DataFrame(results_data)
    st.table(df)
    st.caption("Table: Matching rates of results with teacher feedback.")
    st.write(get_text('participants_note'))
    
    st.write(f"## {get_text('limitations')}")
    st.write(get_text('limitation_content'))

    st.write(f"## {get_text('case_study')}")
    col1, col2 = st.columns(2)
    with col1:
        case1 = Image.open("assets/case_study1.png")
        st.image(case1, use_column_width=True)
    with col2:
        case2 = Image.open("assets/case_study2.png")
        st.image(case2, use_column_width=True)

    # 页脚
    st.markdown("---")
    st.write(get_text('footer'))

def main() -> None:
    # 页面配置
    st.set_page_config(page_title="PsyDraw", page_icon=":house::evergreen_tree:", layout="wide")

    if 'language' not in st.session_state:
        st.session_state.language = "English"
        
    sidebar()
    main_page()

if __name__ == "__main__":
    main()
    