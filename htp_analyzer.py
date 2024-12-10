import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from PIL import Image, ImageTk
from langchain_openai import ChatOpenAI
from datetime import datetime
import webbrowser
import traceback

from src.model_langchain import HTPModel

class HTPAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("HTP Drawing Analyzer / HTP绘画分析器")
        self.root.geometry("1200x800")
        
        self.output_dir = "./report"
        os.makedirs(self.output_dir, exist_ok=True)
        # 创建样式
        self.setup_styles()
        
        # 语言选择
        self.language = tk.StringVar(value="zh")
        self.texts = self.load_ui_texts()
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, style="Main.TFrame")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建左右两个子框架
        left_frame = ttk.Frame(self.main_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        right_frame = ttk.Frame(self.main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # 创建菜单栏
        self.create_menu()
        
        # 左侧布局
        self.create_language_selector(left_frame)
        self.create_api_config(left_frame)
        self.create_image_upload(left_frame)
        
        # 右侧布局
        self.create_output_config(right_frame)
        self.create_preview_area(right_frame)
        
        # 分析按钮放在右侧底部
        self.analyze_btn = ttk.Button(
            right_frame,
            text="Analyze Drawing / 分析绘画",
            command=self.analyze_image,
            style="Accent.TButton"
        )
        self.analyze_btn.grid(row=2, column=0, pady=10)
        
        # 状态栏放在最底部
        self.create_status_bar()
        
        self.setup_tooltips()
        self.image_path = None
        
        # 配置根窗口的网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 配置主框架的列权重
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def setup_styles(self):
        """设置自定义样式"""
        self.style = ttk.Style()
        self.style.configure("Main.TFrame", padding=15)
        self.style.configure("Accent.TButton", padding=5, font=('Helvetica', 10, 'bold'))
        self.style.configure("Status.TLabel", padding=2, relief="sunken")
        
    def load_ui_texts(self):
        """加载界面文字的多语言支持"""
        return {
            'en': {
                'settings': 'Settings',
                'help': 'Help',
                'about': 'About',
                'status_ready': 'Ready',
                'status_analyzing': 'Analyzing...',
                'preview_title': 'Report Preview',
            },
            'zh': {
                'settings': '设置',
                'help': '帮助',
                'about': '关于',
                'status_ready': '就绪',
                'status_analyzing': '分析中...',
                'preview_title': '报告预览',
            }
        }

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="≡", menu=settings_menu)
        settings_menu.add_command(label="Settings / 设置", command=self.show_settings)
        settings_menu.add_command(label="Help / 帮助", command=self.show_help)
        settings_menu.add_separator()
        settings_menu.add_command(label="About / 关于", command=self.show_about)

    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ttk.Label(
            self.main_frame,
            text="Ready / 就绪",
            style="Status.TLabel",
            anchor=tk.W
        )
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

    def create_preview_area(self, parent):
        """创建报告预览区域"""
        preview_frame = ttk.LabelFrame(
            parent,
            text="Report Preview / 报告预览",
            padding="10"
        )
        preview_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            wrap=tk.WORD,
            height=20,
            width=50
        )
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.preview_text.config(state='disabled')

    def setup_tooltips(self):
        """设置工具提示"""
        self.create_tooltip(self.analyze_btn, 
            "Click to analyze the uploaded image\n点击分析上传的图片")
        self.create_tooltip(self.upload_btn, 
            "Click to select an image file\n点击选择图片文件")
        self.create_tooltip(self.api_key, 
            "Enter your API key here\n在此输入您的API密钥")

    def create_tooltip(self, widget, text):
        """创建工具提示"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, justify='left',
                            background="#ffffe0", relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)

    def show_settings(self):
        """显示设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings / 设置")
        settings_window.geometry("400x300")
        
        # 添加设置选项
        ttk.Label(settings_window, text="Temperature:").pack(pady=5)
        temp_scale = ttk.Scale(settings_window, from_=0, to=1, orient=tk.HORIZONTAL)
        temp_scale.set(0.2)
        temp_scale.pack(pady=5)
        
        ttk.Label(settings_window, text="Top P:").pack(pady=5)
        top_p_scale = ttk.Scale(settings_window, from_=0, to=1, orient=tk.HORIZONTAL)
        top_p_scale.set(0.75)
        top_p_scale.pack(pady=5)

    def show_help(self):
        """显示帮助文档"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help / 帮助")
        help_window.geometry("500x400")
        
        help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        help_content = """
HTP Drawing Analyzer Help / HTP绘画分析器帮助

1. API Configuration / API配置
   - Enter your API credentials / 输入API凭证
   - Base URL is pre-filled / 基础URL已预填

2. Image Upload / 图片上传
   - Click "Upload Image" to select a file / 点击"上传图片"选择文件
   - Supported formats: PNG, JPG, JPEG / 支持的格式：PNG、JPG、JPEG

3. Analysis / 分析
   - Click "Analyze Drawing" to start / 点击"分析绘画"开始
   - Wait for the analysis to complete / 等待分析完成
   - Results will be saved automatically / 结果将自动保存

For more information, visit our website / 更多信息，请访问我们的网站
"""
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')

    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo(
            "About / 关于",
            "HTP Drawing Analyzer v1.0\n"
            "A tool for analyzing House-Tree-Person drawings\n"
            "HTP绘画分析工具 v1.0\n"
            "用于分析房子-树木-人物绘画的工具"
        )

    def update_status(self, message):
        """更新状态栏消息"""
        self.status_bar.config(text=message)
        self.root.update()

    def analyze_image(self):
        """分析图片并更新预览"""
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first! / 请先上传图片！")
            return
            
        if not self.api_key.get():
            messagebox.showerror("Error", "Please enter your API key! / 请输入API密钥！")
            return
            
        try:
            self.update_status("Analyzing... / 分析中...")
            # 创建模型实例
            text_model = ChatOpenAI(
                api_key=self.api_key.get(),
                base_url=self.base_url.get(),
                # model="claude-3-5-sonnet-20241022",
                model="gpt-4o-2024-08-06",
                temperature=0.2,
                top_p=0.75,
                seed=42,
                max_retries=5,
            )
            
            multimodal_model = ChatOpenAI(
                api_key=self.api_key.get(),
                base_url=self.base_url.get(),
                model="gpt-4o-2024-08-06",
                temperature=0.2,
                top_p=0.75,
                seed=42,
                max_retries=5,
            )
            
            model = HTPModel(
                text_model=text_model,
                multimodal_model=multimodal_model,
                language=self.language.get(),  # 使用选择的语言
                use_cache=True
            )
            
            # 分析图片
            result = model.workflow(
                image_path=self.image_path,
                language=self.language.get()  # 使用选择的语言
            )
            
            # 生成报告文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = os.path.join(self.output_dir, f"htp_report_{timestamp}.txt")
            usage = result.get("usage", "")
            # 保存报告
            if result["classification"] is True:
                signal = result.get('signal', '')
                final_report = result.get('final', '').replace("<output>", "").replace("</output>", "")
                disclaimer = "注意：本报告由AI生成，仅供参考。不能替代医学诊断。"
                export_data = f"{disclaimer}\n\n{signal}\n\n{final_report}"
            else:
                signal = result.get('fix_signal', '')
                disclaimer = "注意：本报告由AI生成，仅供参考。不能替代医学诊断。"
                export_data = f"{disclaimer}\n\n{signal}"
                
            with open(report_filename, "w", encoding="utf-8") as f:
                f.write(export_data)
                
            # 更新预览区域
            self.preview_text.config(state='normal')
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', export_data)
            self.preview_text.config(state='disabled')
            
            self.update_status(f"Analysis complete. Saved to: {report_filename} / 分析完成。已保存至：{report_filename}, Usage: {usage}")
            
        except Exception as e:
            self.update_status("Analysis failed / 分析失败")
            error_info = traceback.format_exc()
            messagebox.showerror("Error", f"Analysis failed: {str(e)}\n\n{error_info}")

    def create_language_selector(self, parent):
        lang_frame = ttk.Frame(parent)
        lang_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(
            lang_frame,
            text="中文",
            variable=self.language,
            value="zh"
        ).grid(row=0, column=0, padx=5)
                
        ttk.Radiobutton(
            lang_frame,
            text="English",
            variable=self.language,
            value="en"
        ).grid(row=0, column=1, padx=5)
        


    def create_api_config(self, parent):
        # API配置框架
        api_frame = ttk.LabelFrame(
            parent,
            text="API Configuration / API配置",
            padding="10"
        )
        api_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 添加说明文字
        help_text = "Please enter your API credentials / 请输入您的API凭证"
        ttk.Label(
            api_frame,
            text=help_text,
            wraplength=400,
            justify="left"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Base URL with tooltip
        ttk.Label(api_frame, text="Base URL:").grid(row=1, column=0, sticky=tk.W)
        self.base_url = ttk.Entry(api_frame, width=50)
        self.base_url.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        # self.base_url.insert(0, "https://router.ss.chat/v1")
        
        # API Key with tooltip
        ttk.Label(api_frame, text="API Key:").grid(row=2, column=0, sticky=tk.W)
        self.api_key = ttk.Entry(api_frame, width=50, show="*")  # 密码形式显示
        self.api_key.grid(row=2, column=1, padx=5, sticky=(tk.W, tk.E))

    def create_output_config(self, parent):
        """创建输出配置框架"""
        output_frame = ttk.LabelFrame(
            parent,
            text="Output Configuration / 输出配置",
            padding="10"
        )
        output_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 输出路径选择
        ttk.Label(output_frame, text="Output Directory / 输出目录:").grid(row=0, column=0, sticky=tk.W)
        self.output_path_entry = ttk.Entry(output_frame, width=40)
        self.output_path_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.output_path_entry.insert(0, self.output_dir)
        
        browse_btn = ttk.Button(
            output_frame,
            text="Browse / 浏览",
            command=self.browse_output_dir
        )
        browse_btn.grid(row=0, column=2, padx=5)

    def browse_output_dir(self):
        """浏览并选择输出目录"""
        dir_path = filedialog.askdirectory(initialdir=self.output_dir)
        if dir_path:
            self.output_dir = dir_path
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, dir_path)

    def create_image_upload(self, parent):
        # 图片上传框架
        upload_frame = ttk.LabelFrame(
            parent,
            text="Image Upload / 图片上传",
            padding="10"
        )
        upload_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 添加说明文字
        help_text = "Upload your HTP drawing (house, tree, person) / 上传您的HTP绘画（房子、树木、人物）"
        ttk.Label(
            upload_frame,
            text=help_text,
            wraplength=400,
            justify="left"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # 上传按钮
        self.upload_btn = ttk.Button(
            upload_frame,
            text="Upload Image / 上传图片",
            command=self.upload_image
        )
        self.upload_btn.grid(row=1, column=0, pady=5)
        
        # 图片预览标签
        self.image_label = ttk.Label(upload_frame, text="No image selected / 未选择图片")
        self.image_label.grid(row=2, column=0, pady=5)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.image_path = file_path
            # 显示图片预览
            image = Image.open(file_path)
            image.thumbnail((200, 200))  # 缩放图片
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo
            
def main():
    root = tk.Tk()
    app = HTPAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 