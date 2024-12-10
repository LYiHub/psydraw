import base64
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

import openai
from langchain_community.cache import SQLiteCache
from langchain_community.callbacks import get_openai_callback
from langchain_core.globals import set_llm_cache
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_base64_or_path(input_string):
    # 移除可能的前缀（如 "data:image/jpeg;base64,"）
    stripped_string = re.sub(r'^data:image/.+;base64,', '', input_string)
    
    # 检查是否是有效的文件路径
    if os.path.exists(input_string):
        return "path"
    
    # 检查是否可能是 base64
    try:
        # 尝试解码
        base64.b64decode(stripped_string)
        # 检查是否只包含 base64 字符
        if re.match(r'^[A-Za-z0-9+/]+={0,2}$', stripped_string):
            return "base64"
    except:
        pass
    # 如果既不是有效路径也不是 base64，返回 "unknown"
    return "unknown"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

class ClfResult(BaseModel):
    """Classification result."""
    result: bool = Field(description="true or flase, classification result.")

FIX_SIGNAL_EN="""### Assessment Opinion:
Warning

⚠️ IMPORTANT NOTICE ⚠️

The analysis has detected unusually intense negative emotions in the drawing. 
This has triggered a safety mechanism in our system.

We strongly recommend seeking immediate assistance from a qualified mental health professional. 
Your well-being is paramount, and a trained expert can provide the support you may need at this time.

Remember, it's okay to ask for help. You're not alone in this. """

FIX_SIGNAL_ZH="""### 评估意见:
预警

⚠️ 重要提示 ⚠️

分析检测到绘画中存在异常强烈的负面情绪。
这触发了我们的安全机制。

我们强烈建议您立即寻求合格的心理健康专业人士的帮助。
您的健康至关重要，训练有素的专家能够在此时为您提供所需的支持。

请记住，寻求帮助是可以的。您并不孤单。"""

class HTPModel(object):
    def __init__(self, text_model: ChatOpenAI, multimodal_model: Optional[ChatOpenAI] = None, language: str = "zh", use_cache: bool = True):
        self.text_model = text_model
        self.multimodal_model = multimodal_model if multimodal_model else text_model
        # set language
        assert language in ["zh", "en"], "Language should be either 'zh' or 'en'."
        self.language = language
        logger.info(f"HTPModel initialized with text model: {self.text_model.model_name}, multimodal model: {self.multimodal_model.model_name}, language: {language}")
        # set cache
        if use_cache:
            set_llm_cache(SQLiteCache("cache.db"))
            logger.info("Cache enabled.")
        # init token usage
        self.usage = {
            "total": 0,
            "prompt": 0,
            "completion": 0
        }
    
    def refresh_usage(self):
        self.usage = {
            "total": 0,
            "prompt": 0,
            "completion": 0
        }
    
    def update_usage(self, cb):
        self.usage["total"] += cb.total_tokens
        self.usage["prompt"] += cb.prompt_tokens
        self.usage["completion"] += cb.completion_tokens
        
    def get_prompt(self, stage: str):
        assert stage in ["overall", "house", "tree", "person"], "Stage should be either 'overall', 'house', 'tree', or 'person'."

        if stage == "overall":
            feature_prompt = open(f"src/prompt/{self.language}/overall_feature.txt", "r", encoding="utf-8").read()
            analysis_prompt = open(f"src/prompt/{self.language}/overall_analysis.txt", "r", encoding="utf-8").read()
        elif stage == "house":
            feature_prompt = open(f"src/prompt/{self.language}/house_feature.txt", "r", encoding="utf-8").read()
            analysis_prompt = open(f"src/prompt/{self.language}/house_analysis.txt", "r", encoding="utf-8").read()
        elif stage == "tree":
            feature_prompt = open(f"src/prompt/{self.language}/tree_feature.txt", "r", encoding="utf-8").read()
            analysis_prompt = open(f"src/prompt/{self.language}/tree_analysis.txt", "r", encoding="utf-8").read()
        elif stage == "person":
            feature_prompt = open(f"src/prompt/{self.language}/person_feature.txt", "r", encoding="utf-8").read()
            analysis_prompt = open(f"src/prompt/{self.language}/person_analysis.txt", "r", encoding="utf-8").read()
            
        return feature_prompt, analysis_prompt
    
    def basic_analysis(self, image_path: str, stage: str):
        feature_prompt, analysis_prompt = self.get_prompt(stage)
        
        if self.language == "zh":
            feature_input = "将特征提取结果整理为**清晰明确**的markdown格式。"
            analysis_input = "请结合专业知识和助手提供的图像特征，进行特征分析，结果整理为markdown格式。"
        elif self.language == "en":
            feature_input = "Organize the feature extraction results into a **clear and concise** markdown format."
            analysis_input = "Please analyze the features based on professional knowledge and the image features provided by the assistant, and organize the results in markdown format."
            
        # 判断输入是 base64 还是路径
        if is_base64_or_path(image_path) == "path":
            image_data = encode_image(image_path)
        elif is_base64_or_path(image_path) == "base64":
            image_data = image_path
        else:
            raise ValueError("Invalid image path or base64 string.")
        
        feature_prompt = ChatPromptTemplate.from_messages([
            ("system", feature_prompt),
            (
                "user", 
                [
                    {"type": "image_url", "image_url": {'url': 'data:image/jpeg;base64,{image_data}'}},
                    {"type": "text", "text": feature_input}
                ]
            )]
        )
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", analysis_prompt),
            (
                "user",
                [
                    {"type": "image_url", "image_url": {'url': 'data:image/jpeg;base64,{image_data}'}},
                    {"type": "text", "text": analysis_input}
                ]
            )]
        )
        logger.info(f"{stage} analysis started.")
        with get_openai_callback() as cb:
            chain = feature_prompt | self.multimodal_model
            feature_result = chain.invoke({
                "image_data": image_data
            }).content
            
            chain = analysis_prompt | self.text_model
            analysis_result = chain.invoke({
                "image_data": image_data,
                "FEATURES": feature_result
            }).content
            
            self.update_usage(cb)
            
        logger.info(f"{stage} analysis completed.")
        
        return feature_result, analysis_result
    
    def merge_analysis(self, results: dict):
        logger.info("merge analysis started.")
        merge_prompt = open(f"src/prompt/{self.language}/analysis_merge.txt", "r", encoding="utf-8").read()
        merge_inputs = open(f"src/prompt/{self.language}/merge_format.txt", "r", encoding="utf-8").read()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", merge_prompt),
            (
                "user",
                [
                    {"type": "text", "text": merge_inputs}
                ]
            )]
        )
        with get_openai_callback() as cb:
            chain = prompt | self.text_model
            result = chain.invoke({
                "overall_analysis": results["overall"]["analysis"],
                "house_analysis": results["house"]["analysis"],
                "tree_analysis": results["tree"]["analysis"],
                "person_analysis": results["person"]["analysis"]
            }).content

            self.update_usage(cb)
        
        logger.info("merge analysis completed.")
        return result
    
    def final_analysis(self, results: dict):
        logger.info("final analysis started.")
        final_prompt = open(f"src/prompt/{self.language}/final_result.txt", "r", encoding="utf-8").read()
        
        if self.language == "zh":
            inputs = "综合分析结果: \n{merge_result}\n，输出你的专业HTP测试意见书。"
        else:
            inputs = "Based on the analysis results: \n{merge_result}\n, write your professional HTP test report."
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", final_prompt),
            ("user", inputs)
        ])
        
        with get_openai_callback() as cb:
            chain = prompt | self.text_model
            result = chain.invoke({
                "merge_result": results["merge"]
            }).content

            self.update_usage(cb)
        
        logger.info("final analysis completed.")
        return result
    
    def signal_analysis(self, results: dict):
        logger.info("signal analysis started.")
        signal_prompt = open(f"src/prompt/{self.language}/signal_judge.txt", "r", encoding="utf-8").read()
        inputs = "{final_result}"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", signal_prompt),
            ("user", inputs)
        ])
        
        with get_openai_callback() as cb:
            chain = prompt | self.text_model
            result = chain.invoke({
                "final_result": results["final"]
            }).content

            self.update_usage(cb)
        
        logger.info("signal analysis completed.")
        return result
    
    def result_classification(self, results: dict):
        logger.info("result classification started.")
        classification_prompt = open(f"src/prompt/{self.language}/clf.txt", "r", encoding="utf-8").read()
        inputs = "{result}"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", classification_prompt),
            ("user", inputs + "{format_instructions}")
        ])
        with get_openai_callback() as cb:
            # chain = prompt | self.multimodal_model.with_structured_output(ClfResult)
            from langchain_core.output_parsers import JsonOutputParser
            
            parse = JsonOutputParser(pydantic_object=ClfResult)
            chain = prompt | self.multimodal_model | parse
            result = chain.invoke({
                "result": results["signal"],
                "format_instructions": parse.get_format_instructions()
            })
            
            if type(result) == dict:
                result = result["result"]
            if type(result) == str:
                if result == "true":
                    result = True
                elif result == "false":
                    result = False
            
            self.update_usage(cb)
                
        logger.info(f"result classification completed. Result: {result}")
        if type(result) == bool:
            return result
        else:
            return True
        
    def workflow(self, image_path: str, language: str = "zh"):
        self.refresh_usage()
        # update language
        self.language = language
        
        with ThreadPoolExecutor(max_workers = 4) as executor:
            futures = {
                executor.submit(self.basic_analysis, image_path, stage): stage for stage in ["overall", "house", "tree", "person"]
            }
            
            results = {}
            for future in as_completed(futures):
                stage = futures[future]
                feature_result, analysis_result = future.result()
                results[stage] = {
                    "feature": feature_result,
                    "analysis": analysis_result
                }
            results["usage"] = self.usage
        
        results["merge"] = self.merge_analysis(results)
        results["final"] = self.final_analysis(results)
        results["signal"] = self.signal_analysis(results)
        results["classification"] = self.result_classification(results)
        if results["classification"] == False:
            results["fix_signal"] = FIX_SIGNAL_ZH if self.language == "zh" else FIX_SIGNAL_EN
        else:
            results["fix_signal"] = None
            
        logger.info("HTP analysis workflow completed.")
        
        return results